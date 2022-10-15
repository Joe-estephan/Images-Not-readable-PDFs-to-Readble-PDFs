import io
import os

import fitz
from PIL import ImageFilter, ImageEnhance, Image
from PyPDF2 import PdfFileReader, PdfFileWriter
from pytesseract import pytesseract

path_to_tesseract = r"Tesseract-OCR/tesseract.exe"


def get_readable_pdf_from_image(image):
    pytesseract.tesseract_cmd = path_to_tesseract
    # im = Image.open(image)
    # width, height = im.size
    # im = im.filter(ImageFilter.MedianFilter())
    # enhancer = ImageEnhance.Contrast(im)
    # im = enhancer.enhance(2)
    # im = im.convert('1')
    # im = im.resize((width,height))
    result_image_name = os.path.splitext(os.path.basename(image))[0] + '.png'
    # im.save(result_image_name)
    new_pdf = pytesseract.image_to_pdf_or_hocr(result_image_name, extension='pdf')
    return new_pdf


def create_pdf_from_pages(list_pages, result_name):
    pdf_writer = PdfFileWriter()
    for page in list_pages:
        pdf = PdfFileReader(io.BytesIO(page))
        pdf_writer.addPage(pdf.getPage(0))
    result_file_name = os.path.splitext(os.path.basename(result_name))[0] + '.pdf'
    file = open(result_file_name, "w+b")
    pdf_writer.write(file)
    file.close()
    return result_file_name


def filter_input_file(file: [list, str]):
    """
    Converts list of images to single readable pdf, or single image to readable pdf, or not readable pdf to readable pdf
    :param file: can be list of image with multiple types support:png jpg and jpeg
                or single image with multiple types support
                or single pdf file
    :return: result pdf file
    """
    if isinstance(file, list):
        images_list = [x for x in file if x.endswith((".jpg", ".jpeg", ".png"))]
        list_pages = []
        result_file_name = os.path.splitext(os.path.basename(file[0]))[0] + '.pdf'
        for single_image in images_list:
            list_pages.append(get_readable_pdf_from_image(single_image))
        return create_pdf_from_pages(list_pages, result_file_name)
    elif isinstance(file, str):
        if file.endswith((".jpg", ".jpeg", ".png")):
            pdf_writer = PdfFileWriter()
            page = get_readable_pdf_from_image(file)
            pdf = PdfFileReader(io.BytesIO(page))
            pdf_writer.addPage(pdf.getPage(0))
            result_file_name = os.path.splitext(os.path.basename(file))[0] + '.pdf'
            file = open(result_file_name, "w+b")
            pdf_writer.write(file)
            file.close()
            return result_file_name
        elif file.endswith('.pdf'):
            doc = fitz.open(file)
            mat = fitz.Matrix(5, 5)
            images_list = []
            for page in doc:
                pix = page.get_pixmap(matrix=mat)
                img_filename = str(page) + ".png"
                images_list.append(img_filename)
                pix.pil_save(img_filename, format="TIFF", dpi=(300, 300))
            list_pages = []
            result_file_name = os.path.splitext(os.path.basename(file))[0] + '.pdf'
            for single_image in images_list:
                list_pages.append(get_readable_pdf_from_image(single_image))
            for image in images_list:
                os.remove(image)
            return create_pdf_from_pages(list_pages, result_file_name)


filter_input_file("RSA COM Renewal.pdf")
