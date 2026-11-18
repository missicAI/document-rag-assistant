from pathlib import Path
from types import SimpleNamespace

from streamlit.testing.v1 import AppTest


def test_missing_document_has_vietnamese_message():
    at = AppTest.from_file(Path(__file__).resolve().parents[1] / "app.py", default_timeout=15).run()
    at.button[0].click().run()
    assert not at.exception
    assert "chọn tài liệu" in at.info[0].value


def test_vietnamese_document_and_question(monkeypatch):
    import openai
    import streamlit

    text = "Ứng viên cần chạy thử dự án trước buổi phỏng vấn."
    monkeypatch.setattr(
        streamlit,
        "file_uploader",
        lambda *args, **kwargs: SimpleNamespace(size=len(text.encode()), getvalue=lambda: text.encode()),
    )
    received = []

    class Client:
        def __init__(self, **kwargs):
            self.chat = SimpleNamespace(completions=self)

        def create(self, **kwargs):
            received.append(kwargs)
            return SimpleNamespace(
                choices=[SimpleNamespace(message=SimpleNamespace(content="Ứng viên cần chạy thử dự án."))]
            )

    monkeypatch.setattr(openai, "OpenAI", Client)
    at = AppTest.from_file(Path(__file__).resolve().parents[1] / "app.py", default_timeout=15).run()
    field = next(item for item in at.text_input if item.label == "Bạn muốn biết điều gì?")
    field.set_value("Cần làm gì trước buổi phỏng vấn?")
    at.button[0].click().run()
    assert not at.exception
    assert text in received[0]["messages"][-1]["content"]
    assert any("Ứng viên cần chạy thử" in item.value for item in at.markdown)
