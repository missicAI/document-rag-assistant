from dataclasses import dataclass
from io import BytesIO
from pathlib import Path

from pypdf import PdfReader


@dataclass(frozen=True)
class Document:
    source: str
    page: int
    text: str


@dataclass(frozen=True)
class Chunk:
    id: str
    source: str
    page: int
    text: str


def read_document(name: str, content: bytes) -> list[Document]:
    if len(content) > 10 * 1024 * 1024:
        raise ValueError("Mỗi tài liệu tối đa 10 MB.")
    suffix = Path(name).suffix.lower()
    if suffix == ".pdf":
        try:
            reader = PdfReader(BytesIO(content))
            if reader.is_encrypted:
                raise ValueError("Hãy dùng PDF không có mật khẩu.")
            if len(reader.pages) > 100:
                raise ValueError("Mỗi PDF tối đa 100 trang.")
            docs = [Document(name, i + 1, page.extract_text() or "") for i, page in enumerate(reader.pages)]
        except ValueError:
            raise
        except Exception as exc:
            raise ValueError("Không đọc được PDF; hãy kiểm tra lại tệp.") from exc
    elif suffix in {".txt", ".md"}:
        try:
            docs = [Document(name, 1, content.decode("utf-8-sig"))]
        except UnicodeDecodeError:
            raise ValueError("Tệp văn bản cần mã hóa UTF-8.") from None
    else:
        raise ValueError("Chỉ hỗ trợ PDF có văn bản, TXT và Markdown.")
    if not any(doc.text.strip() for doc in docs):
        raise ValueError("Tài liệu không có văn bản đọc được. PDF scan cần OCR trước.")
    if sum(len(doc.text) for doc in docs) > 500000:
        raise ValueError("Nội dung trích xuất tối đa 500.000 ký tự mỗi tệp.")
    return docs


def chunk_documents(documents: list[Document], chunk_words: int = 160, overlap: int = 30) -> list[Chunk]:
    if chunk_words < 1 or not 0 <= overlap < chunk_words:
        raise ValueError("Cần chunk_words > overlap >= 0.")
    chunks = []
    for document in documents:
        words = document.text.split()
        for start in range(0, len(words), chunk_words - overlap):
            text = " ".join(words[start : start + chunk_words])
            chunks.append(Chunk(f"S{len(chunks) + 1}", document.source, document.page, text))
            if start + chunk_words >= len(words):
                break
    if not chunks:
        raise ValueError("Chưa có văn bản để tạo chỉ mục.")
    if len(chunks) > 10000:
        raise ValueError("Bản demo hỗ trợ tối đa 10.000 đoạn.")
    return chunks
