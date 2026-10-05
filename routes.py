from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ai_core.gemini_generator import GeminiDocumentGenerator


router = APIRouter()

generator = GeminiDocumentGenerator()


class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    dates: str


@router.post("/generate")
def generate_document(request: DocumentRequest):

    try:
        document = generator.generate_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            dates=request.dates
        )

        return {
            "success": True,
            "document": document
        }

    except Exception as e:

        print("GEMINI ERROR:", repr(e))

        raise HTTPException(
            status_code=500,
            detail=f"Gemini error: {str(e)}"
        )