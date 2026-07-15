from pypdf import PdfReader, PdfWriter
from watermark import create_watermark

def encrypt_pdf(input_pdf,
                output_pdf,
                password,
                name,
                email):

    reader = PdfReader(input_pdf)
    writer = PdfWriter()

    watermark_pdf = PdfReader(create_watermark(name,email))

    watermark_page = watermark_pdf.pages[0]

    for page in reader.pages:

        page.merge_page(watermark_page)

        writer.add_page(page)

    writer.encrypt(password)

    with open(output_pdf,"wb") as f:
        writer.write(f)