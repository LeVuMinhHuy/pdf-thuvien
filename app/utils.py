import PyPDF2
from PyPDF2 import PdfWriter, PdfReader
from PyPDF2.generic import RectangleObject
import zipfile
import io
import os

def process_pdf_file(uploaded_file):
    if uploaded_file.name.endswith('.zip'):
        return process_zip_file(uploaded_file)
    elif uploaded_file.name.endswith('.pdf'):
        return process_single_pdf(uploaded_file)
    else:
        return None  # Handle unsupported file types

def process_single_pdf(uploaded_file):
    if uploaded_file.name.endswith('.pdf'):
        reader = PdfReader(uploaded_file)
        writer = PdfWriter()

        num_pages = len(reader.pages)

        output_filename = f"processed_{uploaded_file.name}"
        output_path = os.path.join('media', output_filename)  # Adjust path as needed

        for page_num in range(num_pages):
            page = reader.pages[page_num]
        
            width = page.mediabox.right
            height = page.mediabox.top
        
            left_half = page
            left_half.mediabox = RectangleObject([0, 0, width / 2, height])
            writer.add_page(left_half)
        
            right_half = reader.pages[page_num]
            right_half.mediabox = RectangleObject([width / 2, 0, width, height])
            writer.add_page(right_half)

            print(f"Processed page {page_num + 1}}/{num_pages}")

        with open(output_path, "wb") as fp:
            writer.write(fp)
        
        return output_filename

def process_zip_file(uploaded_file):
    output_zip = io.BytesIO()
    with zipfile.ZipFile(output_zip, 'w') as output_zip_file, zipfile.ZipFile(uploaded_file, 'r') as zip_ref:
        for file_name in zip_ref.namelist():
            if file_name.endswith('.pdf'):
                with zip_ref.open(file_name) as pdf_file:
                    processed_pdf = process_single_pdf(pdf_file)
                    output_zip_file.writestr(file_name.replace('.pdf', '_processed.pdf'), processed_pdf)

    output_zip.seek(0)
    return output_zip.read()
