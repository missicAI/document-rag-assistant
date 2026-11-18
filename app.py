from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from pydantic import ValidationError

from ragdesk.documents import chunk_documents, read_document
from ragdesk.generation import answer_question
from ragdesk.llm import LLMClient, LLMError
from ragdesk.retrieval import Retriever

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
st.set_page_config(page_title="RAG Desk · Document Assistant", page_icon="📚", layout="wide")
st.title("📚 RAG Desk — Hỏi đáp tài liệu")
st.caption("Xem đoạn nguồn trước · Tạo câu trả lời khi đã kết nối LLM")
with st.sidebar:
    mode = st.radio("Cách chạy", ["Tìm đoạn tài liệu", "Hỏi đáp bằng LLM"])
    st.caption("Tìm đoạn tài liệu chạy độc lập, không tạo câu trả lời bằng LLM.")
    use_sample = st.checkbox("Dùng sổ tay thực tập mẫu", value=True)
    backend = st.selectbox(
        "Tìm kiếm",
        ["tfidf", "semantic"],
        format_func=lambda x: "TF-IDF — chạy nhẹ" if x == "tfidf" else "Semantic — cần tải mô hình",
    )
    threshold = st.slider("Ngưỡng tương đồng", 0.0, 1.0, 0.10 if backend == "tfidf" else 0.35, 0.01)
    top_k = st.slider("Số đoạn lấy ra", 1, 5, 3)
    st.caption("Điểm tương đồng không phải xác suất câu trả lời đúng.")
uploads = st.file_uploader(
    "Tải PDF có văn bản, TXT hoặc MD", type=["pdf", "txt", "md"], accept_multiple_files=True
)
st.caption("Tối đa 5 tệp, 10 MB/tệp, 100 trang/PDF. Tắt tài liệu mẫu để chỉ hỏi trên tệp của bạn.")
question = st.text_input("Câu hỏi", "Thực tập sinh cần tạo nhánh Git như thế nào?")
if st.button("Tìm đoạn nguồn" if mode == "Tìm đoạn tài liệu" else "Trả lời", type="primary"):
    try:
        if len(uploads) > 5:
            raise ValueError("Chỉ tải tối đa 5 tệp mỗi lần.")
        docs = []
        if use_sample:
            for path in sorted((ROOT / "data/handbook").glob("*.md")):
                docs.extend(read_document(path.name, path.read_bytes()))
        for upload in uploads:
            docs.extend(read_document(upload.name, upload.getvalue()))
        with st.spinner("Đang tìm trong tài liệu..."):
            chunks = chunk_documents(docs)
            retriever = Retriever(chunks, backend)
            hits = retriever.search(question, top_k, threshold)
        st.caption(f"Đã tạo {len(chunks)} đoạn · Tìm thấy {len(hits)} đoạn vượt ngưỡng")
        if mode == "Hỏi đáp bằng LLM":
            with st.spinner("Đang tạo câu trả lời dựa trên nguồn..."):
                answer = answer_question(question, hits, LLMClient.from_env())
            if answer.insufficient_context:
                st.warning(answer.answer)
            else:
                st.write(answer.answer)
                st.caption("Nguồn được LLM sử dụng: " + ", ".join(answer.source_ids))
            st.download_button(
                "Tải câu trả lời JSON", answer.model_dump_json(indent=2), "answer.json", "application/json"
            )
        elif not hits:
            st.warning("Không tìm thấy đoạn phù hợp. Thử diễn đạt lại câu hỏi.")
        else:
            st.info("Đây là các đoạn tìm thấy, chưa phải câu trả lời do LLM tạo.")
        for hit in hits:
            with st.expander(
                f"[{hit.chunk.id}] {hit.chunk.source} · trang {hit.chunk.page} · điểm {hit.score:.3f}",
                expanded=True,
            ):
                st.write(hit.chunk.text)
    except (ValueError, LLMError, ValidationError, OSError) as exc:
        st.error(str(exc))
