import os
import time

from dotenv import load_dotenv
from google import genai


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")


# ============================================================
# GEMINI DOCUMENT GENERATOR
# ============================================================

class GeminiDocumentGenerator:

    def __init__(self):

        # Check API key
        if not API_KEY:
            raise ValueError(
                "GEMINI_API_KEY is missing. "
                "Please add your Gemini API key to the .env file."
            )

        # Create Gemini client
        self.client = genai.Client(
            api_key=API_KEY
        )

        # Gemini model
        self.model = "gemini-3.6-flash"


    # ========================================================
    # GENERATE LEGAL DOCUMENT
    # ========================================================

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        dates: str
    ) -> str:

        prompt = f"""
You are LegalEase AI, an AI assistant for generating
professional legal document drafts.

Create a professional and well-structured draft for the
following legal document.

DOCUMENT TYPE:
{document_type}

PARTIES INVOLVED:
{parties}

IMPORTANT DATES:
{dates}

TERMS AND CONDITIONS:
{terms}


IMPORTANT INSTRUCTIONS:

1. Create a clear and professional legal document.

2. Use appropriate headings and sections.

3. Include the names and roles of the parties where
   appropriate.

4. Include the dates provided by the user.

5. Include the terms and conditions provided by the user.

6. Do not invent important facts that were not provided.

7. Use formal and professional legal language.

8. Make the document easy to understand and read.

9. Include appropriate clauses based on the information
   provided.

10. Include signature sections where appropriate.

11. Do not provide false claims that the document is
    legally binding.

12. Clearly treat the result as an AI-generated draft.

13. Return ONLY the legal document.

Do not add explanations before or after the document.
"""

        # ====================================================
        # TRY GEMINI
        # ====================================================

        for attempt in range(4):

            try:

                print(
                    f"Sending request to Gemini "
                    f"(attempt {attempt + 1}/4)..."
                )

                response = self.client.models.generate_content(
                    model=self.model,
                    contents=prompt
                )

                # Check response
                if not response.text:
                    raise Exception(
                        "Gemini returned an empty response."
                    )

                print(
                    "Gemini document generated successfully."
                )

                return response.text


            except Exception as e:

                error_message = str(e)

                print(
                    f"Gemini attempt {attempt + 1} failed:"
                )

                print(error_message)


                # =================================================
                # RETRY ONLY TEMPORARY 503 ERRORS
                # =================================================

                if (
                    "503" not in error_message
                    and "UNAVAILABLE" not in error_message
                ):

                    raise


                # Retry if attempts remain
                if attempt < 3:

                    wait_time = 2 ** attempt

                    print(
                        "Gemini is temporarily unavailable."
                    )

                    print(
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)


                # =================================================
                # FINAL FAILURE
                # =================================================

                else:

                    raise Exception(
                        "Gemini API is temporarily unavailable.\n\n"
                        "The LegalEase application itself is "
                        "working correctly, but Google's Gemini "
                        "API returned a 503 UNAVAILABLE error.\n\n"
                        f"Last error: {error_message}"
                    )