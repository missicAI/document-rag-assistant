from dataclasses import dataclass
from functools import lru_cache

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

from ragdesk.documents import Chunk


@dataclass(frozen=True)
class Hit:
    chunk: Chunk
    score: float


@lru_cache(maxsize=1)
def load_embedding_model(name):
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        raise ValueError("Cài requirements-semantic.txt trước khi dùng semantic search.") from None
    return SentenceTransformer(name)


class Retriever:
    def __init__(
        self,
        chunks: list[Chunk],
        backend: str = "tfidf",
        model_name: str = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
    ):
        if not chunks:
            raise ValueError("Không có đoạn tài liệu.")
        self.chunks = chunks
        self.backend = backend
        if backend == "tfidf":
            self.vectorizer = TfidfVectorizer(
                analyzer="char_wb", ngram_range=(3, 5), max_features=40000, sublinear_tf=True
            )
            self.matrix = self.vectorizer.fit_transform([c.text for c in chunks])
        elif backend == "semantic":
            self.model = load_embedding_model(model_name)
            self.matrix = self.model.encode([c.text for c in chunks], normalize_embeddings=True)
        else:
            raise ValueError("Backend phải là tfidf hoặc semantic.")

    def search(self, question: str, top_k: int = 3, min_score: float = 0.10) -> list[Hit]:
        if not question.strip() or len(question) > 3000:
            raise ValueError("Câu hỏi cần từ 1 đến 3.000 ký tự.")
        if top_k < 1 or not 0 <= min_score <= 1:
            raise ValueError("top_k phải dương và min_score nằm trong [0, 1].")
        if self.backend == "tfidf":
            query = self.vectorizer.transform([question])
            scores = (self.matrix @ query.T).toarray().ravel()
        else:
            query = self.model.encode([question], normalize_embeddings=True)[0]
            scores = self.matrix @ query
        ranked = np.argsort(-scores, kind="stable")[:top_k]
        return [
            Hit(self.chunks[i], float(scores[i])) for i in ranked if scores[i] > 0 and scores[i] >= min_score
        ]
