import json

import pytest

from ragdesk.documents import Chunk, Document, chunk_documents, read_document
from ragdesk.generation import answer_question
from ragdesk.retrieval import Hit, Retriever


def test_chunks_keep_overlap_source_and_page():
    chunks = chunk_documents([Document("guide.pdf", 7, "one two three four five six seven")], 4, 2)
    assert [c.text for c in chunks] == ["one two three four", "three four five six", "five six seven"]
    assert all(c.source == "guide.pdf" and c.page == 7 for c in chunks)


def test_empty_or_invalid_documents():
    with pytest.raises(ValueError):
        chunk_documents([])
    with pytest.raises(ValueError):
        chunk_documents([Document("x", 1, "hello")], 4, 4)
    with pytest.raises(ValueError):
        read_document("x.txt", b" ")
    with pytest.raises(ValueError):
        read_document("x.exe", b"hello")


def test_retrieval_ranks_relevant_text_and_rejects_no_overlap():
    chunks = [
        Chunk("S1", "git.md", 1, "git branch commit pull request"),
        Chunk("S2", "api.md", 1, "FastAPI predict endpoint server"),
    ]
    retriever = Retriever(chunks)
    assert retriever.search("git commit", min_score=0)[0].chunk.id == "S1"
    assert retriever.search("zzzzzzzzzzz") == []


def test_no_hits_does_not_call_model():
    answer = answer_question("unknown?", [], None)
    assert answer.insufficient_context and not answer.source_ids


class StubClient:
    def __init__(self, payload):
        self.payload = payload

    def generate(self, *args):
        return json.dumps(self.payload)


@pytest.mark.parametrize("ids", [["S99"], []])
def test_hallucinated_or_missing_citations_are_rejected(ids):
    hit = Hit(Chunk("S1", "x.md", 1, "Use git commit."), 0.9)
    with pytest.raises(ValueError):
        answer_question(
            "How?",
            [hit],
            StubClient({"answer": "Use git commit.", "source_ids": ids, "insufficient_context": False}),
        )


def test_supported_citation():
    hit = Hit(Chunk("S1", "x.md", 1, "Use git commit."), 0.9)
    answer = answer_question(
        "How?",
        [hit],
        StubClient({"answer": "Use git commit.", "source_ids": ["S1"], "insufficient_context": False}),
    )
    assert answer.source_ids == ["S1"]
