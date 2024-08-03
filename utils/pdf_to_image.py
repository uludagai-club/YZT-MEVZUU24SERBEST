from pdf2image import convert_from_path
from PIL import Image


class Pdf_to_image:
    def __init__(self,pdf_path) -> None:
        self.file_path = pdf_path

    def get_pages(self):
        pages = convert_from_path(self.file_path)
        return pages
