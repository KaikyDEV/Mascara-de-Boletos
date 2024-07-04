import os
import re
from pathlib import Path
import shutil
from datetime import datetime
from PyPDF2 import PdfFileReader, PdfFileWriter
from Conversor import pdf_to_image, concatenate_images, image_to_pdf
from CortePdf import cortar_pdf
from ConversorHtml import htmlToPdf, atualizar_html_com_dados_do_boleto, extrair_cpf_pdf
import time

# Função para criar diretório se não existir
def criar_diretorio_se_nao_existir(diretorio): 
    if not diretorio.exists():
        diretorio.mkdir(parents=True)

# Caminho dos arquivos
html_path_header = r'X:/ROBOS/ROBO JEQUITI FASE 4/Arquivos/html/index.html'
header_path = r'X:/ROBOS/ROBO JEQUITI FASE 4/Arquivos/header.pdf' # arquivo header
ponto_corte = 1.90  # Ajuste este valor conforme necessário
boletoEntrada_path = Path(r'S:/2024/ROBÔ BOLETOS/JEQUITI FASE 4/ENTRADA')
output_folder_path = Path(r'S:/2024/ROBÔ BOLETOS/JEQUITI FASE 4/SAIDA') # Pasta saída
arquivos_folder_path = Path(r'S:/2024/ROBÔ BOLETOS/JEQUITI FASE 4/BOLETOS GERADOS')

# Cria os diretórios se não existirem
criar_diretorio_se_nao_existir(boletoEntrada_path)
criar_diretorio_se_nao_existir(output_folder_path)

while True:
    # Lista todos os arquivos na pasta de entrada com extensão .pdf
    pdf_files = list(boletoEntrada_path.glob("*.pdf"))

    if not pdf_files:
        print("Nenhum arquivo PDF encontrado na pasta de entrada. Aguardando 1 minuto...")
        time.sleep(60)  # Aguarda 1 minuto antes de verificar novamente
        continue

    print(f"Arquivos PDF encontrados na pasta de entrada: {pdf_files}")

    # Itera sobre todos os arquivos na pasta de entrada
    for file_path in pdf_files:
        # Define o caminho de saída com base no nome do arquivo
        output_file_path = arquivos_folder_path / f"boleto_cortado"

        print(f"Processando arquivo: {file_path}")

        try:
            senhaChaveamento = extrair_cpf_pdf(file_path)
            
            atualizar_html_com_dados_do_boleto(file_path, html_path_header)
            htmlToPdf("X:/ROBOS/ROBO JEQUITI FASE 4/Arquivos/html/boletoNomeado.html")

            # Corta o PDF
            cortar_pdf(file_path, output_file_path)

            # Transformar PDFs em imagens
            image1_path = pdf_to_image(header_path, 'X:/ROBOS/ROBO JEQUITI FASE 4/Arquivos/images/header.png')
            image2_path = pdf_to_image(output_file_path, 'X:/ROBOS/ROBO JEQUITI FASE 4/Arquivos/images/boleto.png')

            # Concatenar imagens
            concatenated_image_path = concatenate_images(image1_path, image2_path, 'X:/ROBOS/ROBO JEQUITI FASE 4/Arquivos/images/concatenated.png')

            # Transformar imagem concatenada em PDF
            concatenated_pdf_path = output_folder_path / f"{file_path.stem}.pdf"
            image_to_pdf(concatenated_image_path, concatenated_pdf_path, senhaChaveamento[:3])

            print(f"Arquivo {file_path.name} processado e salvo em {concatenated_pdf_path}")

            # Exclui o arquivo original após o processamento
            os.remove(file_path)
            print(f"Arquivo original {file_path.name} excluído.")

        except Exception as e:
            print(f"Erro ao processar o arquivo {file_path.name}: {e}")

    # Verifica se a pasta de saída contém arquivos
    output_files = list(output_folder_path.glob("*.pdf"))
    if output_files:
        print("Arquivos processados com sucesso. Verifique a pasta de saída.")
    else:
        print("Nenhum arquivo foi processado ou salvo. Verifique se há algum problema.")

    # Aguarda 1 minuto antes de verificar novamente
    print("Aguardando 1 minuto...")
    time.sleep(60)

# Função para criar pasta do dia atual
def criar_pasta_dia_atual(diretorio_base):
    data_atual = datetime.now()
    nome_pasta = data_atual.strftime("%d-%m-%Y")
    caminho_pasta = os.path.join(diretorio_base, nome_pasta)
    if not os.path.exists(caminho_pasta):
        os.mkdir(caminho_pasta)
    return caminho_pasta

# Função para mover arquivos
def mover_arquivos(origem, destino):
    arquivos = os.listdir(origem)
    for arquivo in arquivos:
        caminho_origem = os.path.join(origem, arquivo)
        shutil.copy(caminho_origem, destino)

if __name__ == "__main__":
    diretorio_base = r"S:/2024/ROBÔ BOLETOS/JEQUITI FASE 4/BOLETOS GERADOS"
    pasta_dia_atual = criar_pasta_dia_atual(diretorio_base)
    pasta_origem = r"S:/2024/ROBÔ BOLETOS/JEQUITI FASE 4/SAIDA"
    mover_arquivos(pasta_origem, pasta_dia_atual)

print("PDF unido com sucesso.")
