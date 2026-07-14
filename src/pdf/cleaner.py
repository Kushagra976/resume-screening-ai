import re


class TextCleaner:
    """
    Cleans raw text extracted from PDF files.
    """

    def clean(self, text: str) -> str:
        """
        Clean extracted PDF text.

        Args:
            text: Raw extracted text.

        Returns:
            Cleaned text.
        """

        # Convert tabs to spaces
        text = text.replace("\t", " ")

        # Remove trailing spaces
        text = re.sub(r"[ \t]+", " ", text)

        # Collapse multiple blank lines into one
        text = re.sub(r"\n\s*\n+", "\n\n", text)

        # Remove leading/trailing whitespace
        text = text.strip()

        return text