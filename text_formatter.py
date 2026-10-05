def create_txt(document_text: str) -> bytes:
    """
    Convert generated document text into a downloadable TXT file.
    """

    return document_text.encode("utf-8")