import spacy
import os

from functools import lru_cache
from distutils.util import strtobool
from typing import cast, Literal
from sentence_transformers import SentenceTransformer

from AI_services.ai_services.vector_storage import VectorStorage
from AI_services.ai_services.models.fact_checker import FactCheckerPipeline
from AI_services.ai_services.preprocessing import Pipeline
from AI_services.ai_services.utils import disable_fastcoref_progress_bar
from AI_services.ai_services.models.coref import CorefResolver

def setup_fact_checker_model() -> FactCheckerPipeline:
    spacy.prefer_gpu()
    disable_fastcoref_progress_bar()
    _device = cast(Literal["cpu", "cuda"], os.getenv("DEVICE", "cpu"))
    _encoder = SentenceTransformer(
        os.getenv("SENTENCE_TRANSFORMER_MODEL"),
        device=_device
    )
    _nlp = spacy.load(os.getenv("SPACY_CORE"))


    @lru_cache(maxsize=None)
    def _get_sentence_embeddings(text: str, **kwargs):
        return _encoder.encode(text, **kwargs)


    _storage = VectorStorage(
        dim=_encoder.get_sentence_embedding_dimension(),
        embedder=_get_sentence_embeddings,
    )
    _storage.load(os.getenv("STORAGE_PATH"))
    _coref_pipeline = Pipeline(
        coref=CorefResolver(
            sentence_splitter=os.getenv("SPACY_CORE"),
            device=_device
        ),
        device=_device
    )

    model = FactCheckerPipeline(
        vector_storage=_storage,
        processing_pipeline=_coref_pipeline,
        processing_device=os.getenv("PROCESSING_DEVICE"),
        device=_device,
        get_explanation=bool(strtobool(os.getenv("ENABLE_LLM", "false"))),
        storage_search_k=int(os.getenv("STORAGE_SEARCH_K")),
        storage_search_threshold=float(os.getenv("STORAGE_SEARCH_THRESHOLD")),
        automatic_contextualisation=bool(strtobool(os.getenv("AUTOMATIC_CONTEXTUALIZATION"))),
        ner_corpus=os.getenv("NER_CORPUS"),
        model_name=os.getenv("MODEL_NAME"),
        enable_ner=bool(strtobool(os.getenv("ENABLE_NER")))
    )
    return model
