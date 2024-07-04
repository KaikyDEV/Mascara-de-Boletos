from wand.image import Image
from PyPDF2 import PdfReader, PdfWriter
from ConversorHtml import htmlToPdf
import os

def pdf_to_image(pdf_path, output_path):
    # se não tiver convertido o arquivo html em pdf, executa a função
    if not os.path.exists(pdf_path):
        htmlToPdf("X:/ROBOS/ROBO JEQUITI FASE 4/Arquivos/html/boletoNomeado.html")

    with Image(filename=pdf_path, resolution=300) as img:
        img.format = 'png'
        img.trim()
        img.save(filename=output_path)
    return output_path

def concatenate_images(image1_path, image2_path, output_path, margin=50):
    with Image(filename=image1_path) as img1:
        with Image(filename=image2_path) as img2:
            new_height = img1.height + img2.height + 2 * margin
            new_width = max(img1.width, img2.width) + 2 * margin
            with Image(width=new_width, height=new_height) as img:
                x1 = (new_width - img1.width) // 2
                x2 = (new_width - img2.width) // 2
                y1 = margin
                y2 = img1.height + margin
                img.composite(img1, x1, y1)
                img.composite(img2, x2, y2)
                img.save(filename=output_path)
    return output_path

def image_to_pdf(image_path, output_path):
     with Image(filename=image_path) as img:
        img.format = 'pdf'
        img.save(filename=output_path)

def image_to_pdf(image_path, output_path, password):
    
    # Converter imagem para PDF
    with Image(filename=image_path) as img:
        img.format = 'pdf'
        temp_pdf_path = 'temp_output.pdf'
        img.save(filename=temp_pdf_path)
    
    #Adicionar criptografia ao PDF
    reader = PdfReader(temp_pdf_path)
    writer = PdfWriter()

    for page in reader.pages:
      writer.add_page(page)
    
    # Definir a senha para criptografia
    writer.encrypt(user_password=password, owner_password=password, use_128bit=True)
    
    # # Salvar o PDF criptografado
    with open(output_path, 'wb') as f_out:
         writer.write(f_out)
    
    # Remover o arquivo PDF temporário, se desejado
    os.remove(temp_pdf_path)
    
