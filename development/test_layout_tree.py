from readers.pdf_reader import PDFReader


def print_layout_tree(document):

    print("\n")
    print("=" * 100)
    print("DOCUMENT")
    print("=" * 100)

    print(document.summary())

    for page in document.pages:

        print("\n")
        print("=" * 100)
        print(f"PAGE {page.page_number}")
        print("=" * 100)

        print(page.summary())

        print()

        for block in page.layout_blocks:

            print("-" * 80)

            print(

                f"BLOCK {block.block_number}"

            )

            print(

                f"Lines      : {block.line_count}"

            )

            print(

                f"Spans      : {block.span_count}"

            )

            print(

                f"Font Size  : {block.average_font_size}"

            )

            print(

                f"Bold       : {block.has_bold_text}"

            )

            print(

                f"BBox       : {block.bbox}"

            )

            print()

            # -----------------------------------------
            # Lines
            # -----------------------------------------

            for line_no, line in enumerate(

                block.lines,

                start=1

            ):

                print(

                    f"   Line {line_no}"

                )

                print(

                    f"      Text : {line.text}"

                )

                print(

                    f"      Avg Font : {line.average_font_size}"

                )

                print(

                    f"      Bold : {line.has_bold_text}"

                )

                print()

                # -------------------------------------
                # Spans
                # -------------------------------------

                for span_no, span in enumerate(

                    line.spans,

                    start=1

                ):

                    print(

                        f"         Span {span_no}"

                    )

                    print(

                        f"            Text : {span.text}"

                    )

                    print(

                        f"            Font : {span.font}"

                    )

                    print(

                        f"            Size : {span.font_size}"

                    )

                    print(

                        f"            Bold : {span.is_bold}"

                    )

                    print(

                        f"            BBox : {span.bbox}"

                    )

                    print()

        print("=" * 100)


if __name__ == "__main__":

    import glob

    pdf_files = glob.glob(

        "test_documents/*.pdf"

    )

    if not pdf_files:

        raise FileNotFoundError(

            "No PDF found inside test_documents"

        )

    reader = PDFReader()

    with open(

        pdf_files[0],

        "rb"

    ) as file:

        document = reader.read(

            file

        )

    print_layout_tree(

        document

    )