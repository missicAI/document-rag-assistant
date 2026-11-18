import argparse
import json
from pathlib import Path

from ragdesk.documents import chunk_documents, read_document
from ragdesk.retrieval import Retriever

ROOT = Path(__file__).resolve().parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--backend", choices=["tfidf", "semantic"], default="tfidf")
    args = parser.parse_args()
    docs = []
    for path in sorted((ROOT / "data/handbook").glob("*.md")):
        docs.extend(read_document(path.name, path.read_bytes()))
    retriever = Retriever(chunk_documents(docs), args.backend)
    rows = []
    for case in json.loads((ROOT / "data/questions.json").read_text(encoding="utf-8")):
        hits = retriever.search(case["question"], top_k=3, min_score=0)
        sources = [h.chunk.source for h in hits]
        rows.append(
            {
                **case,
                "retrieved": sources,
                "top1_correct": bool(sources and sources[0] == case["source"]),
                "recall_at_3": case["source"] in sources,
            }
        )
    report = {
        "backend": args.backend,
        "questions": len(rows),
        "top1_accuracy": sum(r["top1_correct"] for r in rows) / len(rows),
        "recall_at_3": sum(r["recall_at_3"] for r in rows) / len(rows),
        "note": "Small hand-written development set on five sample documents. Retrieval only; does not measure LLM answer correctness or abstention.",
        "cases": rows,
    }
    path = ROOT / f"reports/retrieval_{args.backend}.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in report.items() if k != "cases"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
