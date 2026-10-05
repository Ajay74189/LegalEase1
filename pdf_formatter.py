from fpdf import FPDF


def create_pdf(document_text: str, document_type: str) -> bytes:
    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4"
    )

    pdf.set_margins(
        left=15,
        top=15,
        right=15
    )

    pdf.set_auto_page_break(
        auto=True,
        margin=15
    )

    pdf.add_page()

    # --------------------------------------------------
    # TITLE
    # --------------------------------------------------

    pdf.set_font("Arial", "B", 16)

    safe_title = document_type.encode(
        "latin-1",
        "replace"
    ).decode("latin-1")

    pdf.cell(
        w=0,
        h=10,
        text=safe_title,
        border=0,
        ln=1,
        align="C"
    )

    pdf.ln(8)

    # --------------------------------------------------
    # DOCUMENT TEXT
    # --------------------------------------------------

    pdf.set_font(
        "Arial",
        "",
        11
    )

    # Standard Arial in FPDF does not support
    # every Unicode character.
    safe_text = document_text.encode(
        "latin-1",
        "replace"
    ).decode("latin-1")

    # Normalize line endings.
    safe_text = safe_text.replace(
        "\r\n",
        "\n"
    )

    safe_text = safe_text.replace(
        "\r",
        "\n"
    )

    # Available writing width.
    page_width = pdf.w

    left_margin = pdf.l_margin
    right_margin = pdf.r_margin

    available_width = (
        page_width
        - left_margin
        - right_margin
    )

    line_height = 7

    # --------------------------------------------------
    # MANUAL TEXT WRAPPING
    # --------------------------------------------------

    for paragraph in safe_text.split("\n"):

        # Empty line
        if not paragraph.strip():
            pdf.ln(line_height)
            continue

        words = paragraph.split(" ")

        current_line = ""

        for word in words:

            if not word:
                continue

            # ------------------------------------------
            # Handle extremely long words
            # ------------------------------------------

            remaining_word = word

            while remaining_word:

                # Check whether the whole word fits.
                test_text = (
                    remaining_word
                    if not current_line
                    else current_line
                    + " "
                    + remaining_word
                )

                test_width = pdf.get_string_width(
                    test_text
                )

                if test_width <= available_width:

                    current_line = test_text
                    remaining_word = ""
                    continue

                # --------------------------------------
                # If current line already has text,
                # print it first.
                # --------------------------------------

                if current_line:

                    pdf.cell(
                        w=available_width,
                        h=line_height,
                        text=current_line,
                        border=0,
                        ln=1
                    )

                    current_line = ""

                    continue

                # --------------------------------------
                # The individual word itself is too long.
                # Break it character-by-character.
                # --------------------------------------

                chunk = ""

                for character in remaining_word:

                    test_chunk = chunk + character

                    if (
                        pdf.get_string_width(
                            test_chunk
                        )
                        <= available_width
                    ):
                        chunk = test_chunk

                    else:

                        if chunk:

                            pdf.cell(
                                w=available_width,
                                h=line_height,
                                text=chunk,
                                border=0,
                                ln=1
                            )

                        chunk = character

                if chunk:
                    current_line = chunk

                remaining_word = ""

        # Print whatever remains on the line.
        if current_line:

            pdf.cell(
                w=available_width,
                h=line_height,
                text=current_line,
                border=0,
                ln=1
            )

    # --------------------------------------------------
    # RETURN PDF
    # --------------------------------------------------

    output = pdf.output()

    return bytes(output)