from pypdf import PdfReader


def extract_text_from_pdf(pdf_path):
    """
    PDF se text extract karta hai.
    Har page ka text alag rakhta hai taake source/page
    reference baad mein show ki ja sake.
    """

    reader = PdfReader(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = page.extract_text() or ""

        if text.strip():
            pages.append({
                "text": text.strip(),
                "page": page_number
            })

    return pages


def create_chunks(pages, chunk_size=1000, chunk_overlap=200):
    """
    Extracted text ko chhote chunks mein divide karta hai.
    """

    chunks = []

    for page in pages:
        text = page["text"]
        page_number = page["page"]

        start = 0

        while start < len(text):
            end = start + chunk_size

            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "text": chunk_text,
                    "page": page_number
                })

            start += chunk_size - chunk_overlap

    return chunks