import io
import logging

logger = logging.getLogger(__name__)


def _extract_with_pymupdf(file_content: bytes) -> str:
    import fitz

    doc = fitz.open(stream=file_content, filetype="pdf")
    try:
        return "".join(page.get_text() for page in doc)
    finally:
        doc.close()


def _extract_with_pypdf(file_content: bytes) -> str:
    from pypdf import PdfReader

    reader = PdfReader(io.BytesIO(file_content))
    chunks = []
    for page in reader.pages:
        chunks.append(page.extract_text() or "")
    return "".join(chunks)


async def extract_text_from_pdf(file_content: bytes) -> str:
    """Extract text from PDF bytes, preferring PyMuPDF and falling back to pypdf."""
    try:
        text = _extract_with_pymupdf(file_content)
    except Exception:
        text = _extract_with_pypdf(file_content)

    if not text.strip():
        raise ValueError("The PDF contains no extractable text.")

    return text
