from pathlib import Path

import pymupdf # type: ignore


def extract_text_from_pdf(file_path: str) -> str:
    document = pymupdf.open(file_path)

    try:
        text_parts = []

        for page in document:
            text_parts.append(page.get_text())

        return "\n".join(text_parts).strip()

    finally:
        document.close()


def extract_text_from_document(
    file_path: str,
    file_extension: str,
) -> str | None:
    extension = file_extension.lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    if extension in {".png", ".jpg", ".jpeg"}:
        # Image OCR will be handled by the AI/document service later.
        return None

    raise ValueError(
        f"Unsupported document type: {extension}"
    )