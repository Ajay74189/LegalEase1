import sys
import os

# Add the project root to Python's path
PROJECT_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import requests
import streamlit as st

from backend.formatters.text_formatter import create_txt
from backend.formatters.docx_formatter import create_docx
from backend.formatters.pdf_formatter import create_pdf


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="LegalEase AI",
    page_icon="⚖️",
    layout="wide"
)


# --------------------------------------------------
# BACKEND URL
# --------------------------------------------------

BACKEND_URL = "http://127.0.0.1:8000/generate"


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "generated_document" not in st.session_state:
    st.session_state.generated_document = ""


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 42px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .subtitle {
        text-align: center;
        font-size: 18px;
        color: #666666;
        margin-bottom: 30px;
    }

    .section-title {
        font-size: 24px;
        font-weight: 600;
        margin-top: 20px;
        margin-bottom: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">⚖️ LegalEase AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-Powered Legal Document Generator'
    '</div>',
    unsafe_allow_html=True
)


# --------------------------------------------------
# DOCUMENT INFORMATION
# --------------------------------------------------

st.markdown(
    '<div class="section-title">📄 Document Information</div>',
    unsafe_allow_html=True
)

document_type = st.selectbox(
    "Document Type",
    [
        "Rental Agreement",
        "Employment Agreement",
        "Non-Disclosure Agreement",
        "Service Agreement",
        "Partnership Agreement",
        "Sale Agreement",
        "Lease Agreement",
        "Affidavit",
        "Other"
    ]
)


# --------------------------------------------------
# IMPORTANT DATES
# --------------------------------------------------

st.markdown(
    '<div class="section-title">📅 Important Dates</div>',
    unsafe_allow_html=True
)

dates = st.text_area(
    "Enter important dates",
    placeholder=(
        "Example:\n"
        "Agreement Start Date: 1 October 2026\n"
        "Agreement End Date: 30 September 2027"
    ),
    height=120
)


# --------------------------------------------------
# PARTIES
# --------------------------------------------------

st.markdown(
    '<div class="section-title">👥 Parties Involved</div>',
    unsafe_allow_html=True
)

parties = st.text_area(
    "Enter the parties involved",
    placeholder=(
        "Example:\n"
        "Landlord: Arun Kumar\n"
        "Tenant: Rahul Sharma\n"
        "Property Address: 25 Anna Nagar, Chennai"
    ),
    height=140
)


# --------------------------------------------------
# TERMS AND CONDITIONS
# --------------------------------------------------

st.markdown(
    '<div class="section-title">📋 Terms & Conditions</div>',
    unsafe_allow_html=True
)

terms = st.text_area(
    "Enter the terms and conditions",
    placeholder=(
        "Example:\n"
        "Monthly rent is ₹15,000.\n"
        "Security deposit is ₹30,000.\n"
        "Rent must be paid before the 5th of every month.\n"
        "The tenant must maintain the property properly."
    ),
    height=200
)


# --------------------------------------------------
# GENERATE BUTTON
# --------------------------------------------------

st.markdown("---")

st.markdown(
    "### ✨ Generate Your Legal Document"
)

generate_button = st.button(
    "✨ Generate Document",
    type="primary",
    use_container_width=True
)


# --------------------------------------------------
# GENERATE DOCUMENT
# --------------------------------------------------

if generate_button:

    if not parties.strip():

        st.warning(
            "⚠️ Please enter the parties involved."
        )

    elif not terms.strip():

        st.warning(
            "⚠️ Please enter the terms and conditions."
        )

    else:

        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "dates": dates
        }

        with st.spinner(
            "🤖 Generating your legal document..."
        ):

            try:

                response = requests.post(
                    BACKEND_URL,
                    json=payload,
                    timeout=120
                )

                # ------------------------------------------
                # SUCCESS
                # ------------------------------------------

                if response.status_code == 200:

                    data = response.json()

                    if data.get("success"):

                        generated_document = data.get(
                            "document",
                            ""
                        )

                        if generated_document:

                            st.session_state.generated_document = (
                                generated_document
                            )

                            st.success(
                                "✅ Document generated successfully!"
                            )

                        else:

                            st.error(
                                "❌ Gemini returned an empty document."
                            )

                    else:

                        st.error(
                            "❌ The document could not be generated."
                        )


                # ------------------------------------------
                # DIRECT 429
                # ------------------------------------------

                elif response.status_code == 429:

                    st.warning(
                        "⚠️ Gemini API quota reached.\n\n"
                        "The free Gemini API request limit "
                        "has been reached for this project.\n\n"
                        "Please wait for the quota to reset "
                        "and try again later."
                    )


                # ------------------------------------------
                # SERVER ERRORS
                # ------------------------------------------

                elif response.status_code >= 500:

                    try:

                        error_data = response.json()

                        detail = str(
                            error_data.get(
                                "detail",
                                ""
                            )
                        )

                    except Exception:

                        detail = ""


                    # Gemini quota

                    if (
                        "429" in detail
                        or "RESOURCE_EXHAUSTED" in detail
                        or "quota" in detail.lower()
                    ):

                        st.warning(
                            "⚠️ Gemini API quota reached.\n\n"
                            "The free Gemini API request limit "
                            "has been reached for this project.\n\n"
                            "Please wait for the quota to reset "
                            "and try again later."
                        )


                    # Gemini temporary unavailable

                    elif (
                        "503" in detail
                        or "UNAVAILABLE" in detail
                    ):

                        st.warning(
                            "⚠️ Gemini is temporarily unavailable.\n\n"
                            "Google's Gemini service is currently "
                            "busy. Please wait a moment and try again."
                        )


                    # Other backend error

                    else:

                        st.error(
                            "❌ The document could not be generated "
                            "right now.\n\n"
                            "Please try again later."
                        )


                # ------------------------------------------
                # OTHER HTTP ERRORS
                # ------------------------------------------

                else:

                    st.error(
                        f"❌ Request failed "
                        f"(HTTP {response.status_code}).\n\n"
                        "Please try again later."
                    )


            # ----------------------------------------------
            # CONNECTION ERROR
            # ----------------------------------------------

            except requests.exceptions.ConnectionError:

                st.error(
                    "🔌 Could not connect to the LegalEase backend.\n\n"
                    "Please make sure the FastAPI backend is running."
                )


            # ----------------------------------------------
            # TIMEOUT
            # ----------------------------------------------

            except requests.exceptions.Timeout:

                st.warning(
                    "⏳ The request took too long.\n\n"
                    "Gemini may be busy. Please wait a moment "
                    "and try again."
                )


            # ----------------------------------------------
            # NETWORK ERROR
            # ----------------------------------------------

            except requests.exceptions.RequestException:

                st.error(
                    "❌ A network error occurred while contacting "
                    "the backend.\n\n"
                    "Please try again later."
                )


            # ----------------------------------------------
            # UNKNOWN ERROR
            # ----------------------------------------------

            except Exception as e:

                st.error(
                    "❌ Something went wrong while generating "
                    "the document."
                )

                st.code(
                    str(e)
                )


# --------------------------------------------------
# GENERATED DOCUMENT
# --------------------------------------------------

if st.session_state.generated_document:

    st.markdown("---")

    st.markdown(
        '<div class="section-title">'
        '📝 Generated Document'
        '</div>',
        unsafe_allow_html=True
    )

    st.info(
        "You can edit the generated document below "
        "before downloading it."
    )


    # ----------------------------------------------
    # EDITABLE DOCUMENT
    # ----------------------------------------------

    edited_document = st.text_area(
        "Document Preview / Editor",
        value=st.session_state.generated_document,
        height=500
    )

    st.session_state.generated_document = edited_document


    # ----------------------------------------------
    # DOWNLOAD SECTION
    # ----------------------------------------------

    st.markdown(
        "### 📥 Download Document"
    )

    col1, col2, col3 = st.columns(3)


    # ----------------------------------------------
    # TXT
    # ----------------------------------------------

    with col1:

        try:

            txt_file = create_txt(
                edited_document
            )

            st.download_button(
                label="📄 Download TXT",
                data=txt_file,
                file_name="LegalEase_Document.txt",
                mime="text/plain",
                use_container_width=True
            )

        except Exception as e:

            st.error(
                "❌ Unable to create the TXT file."
            )

            st.code(
                str(e)
            )


    # ----------------------------------------------
    # DOCX
    # ----------------------------------------------

    with col2:

        try:

            docx_file = create_docx(
                edited_document,
                document_type
            )

            st.download_button(
                label="📝 Download DOCX",
                data=docx_file,
                file_name="LegalEase_Document.docx",
                mime=(
                    "application/vnd.openxmlformats-"
                    "officedocument.wordprocessingml.document"
                ),
                use_container_width=True
            )

        except Exception as e:

            st.error(
                "❌ Unable to create the DOCX file."
            )

            st.code(
                str(e)
            )


    # ----------------------------------------------
    # PDF
    # ----------------------------------------------

    with col3:

        try:

            pdf_file = create_pdf(
                edited_document,
                document_type
            )

            st.download_button(
                label="📕 Download PDF",
                data=pdf_file,
                file_name="LegalEase_Document.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        except Exception as e:

            # IMPORTANT:
            # Show the real error instead of hiding it.

            st.error(
                "❌ Unable to create the PDF file."
            )

            st.code(
                str(e)
            )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "⚖️ LegalEase AI — AI-generated legal document drafts. "
    "Please have generated documents reviewed by a qualified "
    "legal professional before legal use."
)