from backend.formatters.text_formatter import create_txt
from backend.formatters.docx_formatter import create_docx
from backend.formatters.pdf_formatter import create_pdf


def test_create_txt():
    text = "This is a test legal document."

    result = create_txt(text)

    assert isinstance(result, bytes)
    assert result.decode("utf-8") == text


def test_create_docx():
    text = "This is a test legal document."

    result = create_docx(text, "Test Agreement")

    assert isinstance(result, bytes)
    assert len(result) > 0


def test_create_pdf():
    text = "This is a test legal document."

    result = create_pdf(text, "Test Agreement")

    assert isinstance(result, bytes)
    assert len(result) > 0