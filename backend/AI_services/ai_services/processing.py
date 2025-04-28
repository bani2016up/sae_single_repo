import inspect
import re

from collections import OrderedDict
from typing import List, Tuple, Any, Callable
from tqdm.auto import tqdm

from .interfaces import DeviceAwareModel
from .typing import DeviceType
from .models.coref import CorefResolver

__all__ = (
    "Pipeline",
    "get_default_paragraph_processing_pipeline"
)


class Pipeline(DeviceAwareModel):
    def __init__(
        self,
        steps: List[Tuple[str, Callable]] = None,
        use_tqdm=False,
        *,
        device: DeviceType = "cpu",
        **kwargs
    ):
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
        if name in self.pipeline:
            raise ValueError(f"Pipeline already contains a step with name '{name}'")
        self.pipeline[name] = func
        self._func2device(func)

    def unregister(self, name: str):
        if name not in self.pipeline:
            raise ValueError(f"Pipeline does not contain a step with name '{name}'")
        del self.pipeline[name]

    def to(self, device: DeviceType) -> "Pipeline":
        self._device = device
        for func in self.pipeline.values():
            self._func2device(func)
        return self

    def __call__(self, data: Any, **kwargs) -> Any:
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

    def __getitem__(self, name: str):
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
        return f"Pipeline(\n{body}\n)"

    def __len__(self):
        return len(self.pipeline)

    def __contains__(self, name: str):
        return name in self.pipeline

    def __iter__(self):
        return iter(self.pipeline.items())

    def __getattr__(self, item):
        if item in self.pipeline:
            return self.pipeline[item]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{item}'")


def get_default_paragraph_processing_pipeline() -> Pipeline:
    return Pipeline(
        sentence_reg=re.compile(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=[.?])\s").split,
        device="cpu"
    )


def get_default_coref_pipeline(*, device: DeviceType = "cuda") -> Pipeline:
    return Pipeline(
        steps=[
            ("coref", CorefResolver()),
        ],
        device=device
    )
