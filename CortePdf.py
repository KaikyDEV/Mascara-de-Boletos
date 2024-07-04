import PyPDF2
import os

def cortar_pdf(input_path, output_path):
    # Verificar se o arquivo de entrada existe
    if not os.path.isfile(input_path):
        print(f"O arquivo {input_path} não foi encontrado.")
        return

    # Abrir o arquivo PDF original
    with open(input_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        writer = PyPDF2.PdfWriter()

        # Iterar sobre todas as páginas, exceto a primeira
        for page_num in range(1, len(reader.pages)):
            page = reader.pages[page_num]
            writer.add_page(page)

        # Salvar o novo PDF sem a primeira página
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

# input_path = r'L:/ROBOS/Robô Boleto Jequiti Fase 2 e 3/Entrada/MICHELE PEREIRA DA SILVA OLIVEIRA.pdf'
# output_path = r'L:/ROBOS/Robô Boleto Jequiti Fase 2 e 3/Saida/MICHELE PEREIRA DA SILVA OLIVEIRA.pdf'

# cortar_pdf(input_path, output_path) 