import inspect
import re

from collections import OrderedDict
from typing import get_args, Iterator, List, Tuple, Any, Callable, TypeVar, Generic
from tqdm.auto import tqdm

from .interfaces import DeviceAwareModel
from .typing import DeviceType
from .models.coref import CorefResolver

__all__ = (
    "Pipeline",
    "get_default_paragraph_processing_pipeline",
    "get_default_coref_pipeline",
)

T = TypeVar("T")
U = TypeVar("U")


class Pipeline(Generic[T, U], DeviceAwareModel):
    """
    A class to create a processing pipeline for data.
    This class allows for the registration of multiple processing steps,
    each represented by a callable function.
    The pipeline can be executed in sequence, processing the data
    through each registered step.
    """

    def __init__(
        self,
        steps: List[Tuple[str, Callable]] = None,
        use_tqdm=False,
        *,
        device: DeviceType = "cpu",
        **kwargs
    ):
        """
        Initialize the Pipeline with the specified steps and device.

        Args:
            steps (List[Tuple[str, Callable]]): A list of tuples where each tuple contains
                a name (str) and a callable function. The functions will be executed in order.
            use_tqdm (bool): Whether to use tqdm for progress tracking.
            device (DeviceType): Device to load the model on ("cpu" or "cuda").
            **kwargs: Additional keyword arguments for registering steps.
        """
        super().__init__(device=device)
        if steps is None:
            steps = []
        self.use_tqdm = use_tqdm
        self.pipeline: OrderedDict[str, Any] = OrderedDict()

        for name, func in steps:
            self.register(name, func)

        for name, func in kwargs.items():
            self.register(name, func)

    def _func2device(self, func: Callable):
        if hasattr(func, "to"):
            func.to(self.device)
        return func

    def register(self, name: str, func: Callable):
        """
        Register a new step in the pipeline.

        Args:
            name (str): The name of the step.
            func (Callable): The function to be executed in this step.
        """
        if name in self.pipeline:
            raise ValueError(f"Pipeline already contains a step with name '{name}'")
        self.pipeline[name] = func
        self._func2device(func)

    def unregister(self, name: str):
        """
        Unregister a step from the pipeline.

        Args:
            name (str): The name of the step to be removed.
        Raises:
            ValueError: If the step with the specified name does not exist in the pipeline.
        """
        if name not in self.pipeline:
            raise ValueError(f"Pipeline does not contain a step with name '{name}'")
        del self.pipeline[name]

    def to(self, device: DeviceType) -> "Pipeline":
        """
        Move the pipeline to the specified device.

        Args:
            device (DeviceType): The target device ("cpu" or "cuda").
        """
        self._device = device
        for func in self.pipeline.values():
            self._func2device(func)
        return self

    def __call__(self, data: T) -> U:
        """
        Execute the pipeline on the provided data.
        The data is processed through each registered step in the order they were added.

        Args:
            data (Any): The input data to be processed.
        Returns:
            Any: The processed data after passing through the pipeline.
        """
        iterator = tqdm(
            self.pipeline.items(),
            desc="Processing",
            total=len(self.pipeline),
            unit="step",
            disable=not self.use_tqdm,
        )
        for name, func in iterator:
            data = func(data)
        return data

    def __getitem__(self, name: str) -> Callable:
        """
        Get a registered step by its name.
        Args:
            name (str): The name of the step to retrieve.
        Returns:
            Callable: The function associated with the specified step name.
        """
        return self.pipeline[name]

    def __repr__(self):
        return f"Pipeline(l={len(self.pipeline)})"

    def __str__(self) -> str:
        lines = []
        for name, func in self.pipeline.items():
            if inspect.isfunction(func) or inspect.ismethod(func):
                func_str = func.__name__
            else:
                cls_name = func.__class__.__name__
                attrs = [(k, v) for k, v in vars(func).items() if not k.startswith('_')]
                if attrs:
                    attr_lines = [f"{k}={v!r}" for k, v in attrs]
                    attr_str = ",\n\t\t".join(attr_lines)
                    func_str = f"{cls_name}(\n\t\t{attr_str}\n\t)"
                else:
                    func_str = f"{cls_name}()"
            lines.append(f"\t({name}): {func_str}")
        body = "\n".join(lines)

        type_args = None
        orig = getattr(self, "__orig_class__", None)
        if orig:
            type_args = get_args(orig)

        name_t, name_u = "T", "U"

        if type_args and len(type_args) == 2:
            name_t = getattr(type_args[0], "__name__", str(type_args[0]))
            name_u = getattr(type_args[1], "__name__", str(type_args[1]))
        return f"Pipeline<{name_t}, {name_u}>(\n{body}\n)"

    def __len__(self):
        """
        Get the number of steps in the pipeline.
        Returns:
            int: The number of steps in the pipeline.
        """
        return len(self.pipeline)

    def __contains__(self, name: str):
        """
        Check if a step with the specified name exists in the pipeline.

        Args:
            name (str): The name of the step to check.

        Returns:
            bool: True if the step exists, False otherwise.
        """
        return name in self.pipeline

    def __iter__(self) -> Iterator[Tuple[str, Callable]]:
        """
        Iterate over the steps in the pipeline.

        Returns:
            Iterator[Tuple[str, Callable]]: An iterator over the steps in the pipeline.
        """
        return iter(self.pipeline.items())

    def __getattr__(self, item) -> Callable:
        """
        Get a registered step by its name using dot notation.

        Args:
            item (str): The name of the step to retrieve.

        Returns:
            Callable: The function associated with the specified step name.
        """
        for func in self.pipeline.values():
            if hasattr(func, item):
                return getattr(func, item)
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")


def get_default_paragraph_processing_pipeline() -> Pipeline:
    """
    Create a default paragraph processing pipeline.
    This pipeline includes a sentence segmentation step using regex.
    It splits the text into sentences based on punctuation marks.
    The sentences are split using a regex pattern that looks for
    punctuation followed by whitespace.
    The pipeline is initialized with a device set to "cpu".

    Returns:
        Pipeline: The initialized pipeline with sentence segmentation step.
    """
    return Pipeline[str, str](
        sentence_reg=re.compile(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=[.?])\s").split,
        device="cpu"
    )


def get_default_coref_pipeline(*, device: DeviceType = "cuda") -> Pipeline:
    """
    Create a default coreference resolution pipeline.
    This pipeline includes a coreference resolution step using the LingMessCoref model.
    The model is initialized with the specified device.
    The coreference resolution step processes the input text
    and returns a list of resolved sentences.
    The sentences are represented as `SentenceProposal` objects,
    which contain the tokens and their indices.
    The pipeline is initialized with the specified device.

    Args:
        device (DeviceType): The device to load the model on ("cpu" or "cuda").
    Returns:
        Pipeline: The initialized pipeline with coreference resolution step.
    """
    return Pipeline[str, str](
        steps=[
            ("coref", CorefResolver()),
        ],
        device=device
    )
