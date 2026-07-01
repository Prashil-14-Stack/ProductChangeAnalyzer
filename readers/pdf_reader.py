import fitz


class PDFReader:

    def read(self, file_path):

        document = fitz.open(file_path)

        data = {}

        current_parameter = None
        description = []

        for page in document:

            text = page.get_text()

            for line in text.split("\n"):

                line = line.strip()

                if not line:
                    continue

                # Parameter lines usually end with ":"
                if line.endswith(":"):

                    if current_parameter:

                        data[current_parameter] = "\n".join(description).strip()

                    current_parameter = line[:-1].strip()
                    description = []

                else:

                    if current_parameter:
                        description.append(line)

        if current_parameter:

            data[current_parameter] = "\n".join(description).strip()

        document.close()

        return data