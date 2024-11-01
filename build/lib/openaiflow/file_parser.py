#
# with open("written.txt", "w") as file:
#     print("writing")
#     for line in data:
#         file.write(line)
#
#


def extract_text_from_file(file) -> str:
    """
    Extracts text from a file
    """

    if not file:
        raise ValueError("File is required")

    try:
        with open(file, "r") as f:
            data = f.read()
            return data
    except Exception as e:
        raise ValueError(f"Error extracting text from file: {e}")
