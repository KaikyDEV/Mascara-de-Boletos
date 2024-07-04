import pdfkit
import PyPDF2
from pathlib import Path
import re
import os

# Convertendo a página HTML para PDF usando pdfkit
def htmlToPdf(arquivo_html):
    try:
        pdfkit.from_file(arquivo_html, 'X:/ROBOS/ROBO JEQUITI FASE 4/Arquivos/header.pdf')
        print("Arquivo HTML Convertido com sucesso!")
    except Exception as e:
        print(f"Não foi possível converter o HTML em PDF. Erro: {e}")

def extrair_cpf_pdf(pdf_path):  
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            texto_completo = ""
            for page in reader.pages:
                texto_completo += page.extract_text()

            # Padrão para encontrar o CPF no formato CPF/CNPJ: XXXXXXXXXXX
            padrao_cpf = r'CPF/CNPJ:\s*(\d+)'
            match = re.search(padrao_cpf, texto_completo)
            if match:
                cpf = match.group(1)
                print(cpf)
                return cpf
            else:
                print("CPF não encontrado no texto do PDF.")
                
    except ValueError:
        print("Por favor, insira um valor inteiro.")
        
        
def extrair_codigo_barras(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)

            codigo_barras = None

            # Itera pelas páginas do PDF
            for page_num in range(len(reader.pages)):
                page = reader.pages[page_num]
                text = page.extract_text()

                # Expressão regular para capturar o código de barras no formato específico
                padrao_cod_barra = r'(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d\s+\d{13,14})'
                match_cod_barra = re.search(padrao_cod_barra, text)

                if match_cod_barra:
                    codigo_barras = match_cod_barra.group(1).strip()
                    break  # Para a busca após encontrar o primeiro código de barras válido

            if codigo_barras:
                print(codigo_barras)
                return codigo_barras
            else:
                print("Código de barras não encontrado no PDF.")
                return None

    except Exception as e:
        print(f"Erro ao extrair código de barras do PDF: {e}")
        return None

        
def extrair_dados_pdf(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            texto_completo = ""
            for page in reader.pages:
                texto_completo += page.extract_text()

            linhas = texto_completo.split('\n')
            
            # Inicializar dados
            dados = {
                'nome': None,
                'cod_barra': None,
                'data': None,
                'n_doc': None,
                'especie': None,
                'aceite': None,
                'dt_proc': None,
                'nnum': None,
                'ref' : None,
                'valor': None
            }
            
            
            # Definir as linhas específicas a serem extraídas
            linha_nome = linhas[15] if len(linhas) > 15 else ''
            linha_cod_barra = extrair_codigo_barras(pdf_path)
            linha_data = linhas[13] if len(linhas) > 13 else ''
            linha_n_doc = linhas[3] if len(linhas) > 3 else ''
            linha_especie = linhas[13] if len(linhas) > 13 else ''
            linha_aceite = linhas[4] if len(linhas) > 4 else ''
            linha_dt_proc = linhas[18] if len(linhas) > 18 else ''
            linha_nnum = linhas[20] if len(linhas) > 20 else ''
            linha_ref = linhas[21] if len(linhas) > 21 else ''
            linha_valor = linhas[13] if len(linhas) > 13 else ''
            
            ###### Extrair e ajustar os dados ######
            
            # Nome
            padrao_nome = r'^(.*?)(?=Nosso Número)'
            match_nome = re.search(padrao_nome, linha_nome)
            if match_nome:
                nome = match_nome.group(1).strip()
                nome = ' '.join(nome.split())
                dados['nome'] = nome
                
                
            #Código de barras     
            padrao_cod_barra = r'(\d{5}\.\d{5}\s+\d{5}\.\d{6}\s+\d{5}\.\d{6}\s+\d\s+\d{13,14})'
            match_cod_barra = re.search(padrao_cod_barra, linha_cod_barra)
            if match_cod_barra:
                dados['cod_barra'] = match_cod_barra.group(1).strip()
                
            # Data do Documento
            padrao_data = r'\d{1,2}/\d{1,2}/\d{2,4}'  # Ajuste da expressão regular para capturar a data
            match_data = re.search(padrao_data, linha_data)
            if match_data:
                data = match_data.group(0)
                dados['data'] = data
                
            # Especie
            padrao_especie = r'\bDM\b'
            match_especie = re.search(padrao_especie, linha_especie)
            if match_especie:
                especie = match_especie.group()
                dados['especie'] = especie
                
            # Numero Documento
            padrao_n_doc = r'^(.*?)(?=\s*(?:Espécie|Doc|Aceite))'
            match_n_doc = re.search(padrao_n_doc, linha_n_doc)
            if match_n_doc:
                n_doc = match_n_doc.group(1).strip()
                dados['n_doc'] = n_doc

            # Valor
            padrao_valor = r'\b(\d+,\d+)\b'  # Ajuste da expressão regular para capturar o valor numérico
            match_valor = re.search(padrao_valor, linha_valor)
            if match_valor:
                valor = match_valor.group(1)
                dados['valor'] = valor
                
            # Aceite 
            padrao_aceite = r'(\S)\s*Data do Processamento'
            match_aceite = re.search(padrao_aceite, linha_aceite)
            if match_aceite:
                aceite = match_aceite.group(1).strip()
                dados['aceite'] = aceite
                
            # Data do Processamento
            padrao_dt_proc = r'(\d{2}/\d{2}/\d{4})'  # Ajuste da expressão regular para capturar a data
            match_dt_proc = re.search(padrao_dt_proc, linha_dt_proc)
            if match_dt_proc:
                dt_proc = match_dt_proc.group(1)
                dados['dt_proc'] = dt_proc
                
                
            padrao_nnum = r':(\d{11}-\d{1})'
            match_nnum = re.search(padrao_nnum, linha_nnum)
            if match_nnum:
                nnum = match_nnum.group(1)
                dados['nnum'] = nnum
            
            #REF
            padrao_ref = re.compile(r'.+')
            match_ref = padrao_ref.match(linha_ref)
            if match_ref:
                ref = match_ref.group()
                dados['ref'] = ref
                
            # print(dados['n_doc'])
            # print(dados['aceite'])
            # print(dados['data'])
            # print(dados['especie'])
            # print(dados['valor'])
            # print(dados['nome'])
            # print(dados['dt_proc'])
            # print(dados['nnum'])
            # print(dados['ref'])
            print(dados)
            return dados 
        
    except Exception as e:
        print(f"Erro ao extrair dados do PDF: {e}")
        return None
    
    
def replace_dados_no_html(html_path, dados, novo_html_path):
    try:
        with open(html_path, 'r', encoding='utf-8') as file:
            content = file.read()
            substituicoes = {
                '{NOME}': dados.get('nome', ''),
                '{COD_BARRA}': dados.get('cod_barra', ''),
                '{DATA}': dados.get('data', ''),
                '{NDOC}': dados.get('n_doc', ''),
                '{ESP}': dados.get('especie', ''),
                '{ACEITE}': dados.get('aceite', ''),
                '{DATAPROC}': dados.get('dt_proc', ''),
                '{NNUM}': dados.get('nnum', ''),
                '{NVALOR}' : dados.get('valor', '')
            }
            for placeholder, valor in substituicoes.items():
                content = content.replace(placeholder, valor)
            
            with open(novo_html_path, 'w', encoding='utf-8') as new_file:
                new_file.write(content)
        print(f"Substituição realizada com sucesso! Novo arquivo: {novo_html_path}")
    except Exception as e:
        print(f"Não foi possível alterar os dados no documento HTML. Erro: {e}")

def atualizar_html_com_dados_do_boleto(boleto_pdf_path, html_path):
    dados_extraidos = extrair_dados_pdf(boleto_pdf_path)
    
    if dados_extraidos:
        novo_html_path = os.path.join(os.path.dirname(html_path), "boletoNomeado.html")
        replace_dados_no_html(html_path, dados_extraidos, novo_html_path)
    else:
        print("Não foi possível extrair os dados do boleto PDF.")
        
def renomear_versao_final_pdf(pdf_path):
    dados = extrair_dados_pdf(pdf_path)
    try:
        nome_cliente = dados.get('nome', 'boleto').replace(' ', '_')  # Substituir espaços por underscores
        novo_caminho = os.path.join(os.path.dirname(pdf_path), f"{nome_cliente}.pdf")
        os.rename(pdf_path, novo_caminho)
        print(f"Arquivo PDF renomeado para: {novo_caminho}")
    except Exception as e:
        print(f"Erro ao renomear o arquivo PDF: {e}")
        
    return Path (f'{novo_caminho}')

# html = 'L:/ROBOS/ROBO BOLETO UZE/Arquivos/html/boletoUze.html'
pdf = 'L:/ROBOS/Robô Boleto Jequiti Fase 2 e 3/Entrada/MICHELE PEREIRA DA SILVA OLIVEIRA.pdf'
# html = 'L:/ROBOS/ROBO BOLETO JEQUITI/Arquivos/images/header.png'
# renomear_versao_final_pdf(pdf)
# atualizar_html_com_nome_loja(html, pdf)
# extrair_dados_pdf(pdf)
# # atualizar_html_com_dados_do_boleto(pdf, html)

def extrair_linha(pdf_path):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            texto_completo = ""
            for page in reader.pages:
                texto_completo += page.extract_text()

            linhas = texto_completo.split('\n')  # Divide o texto completo em linhas
            linha = linhas[18]  # O índice 26 corresponde à linha 27 (Python começa a contar do zero)
                       
            while True:
                valor = input('Insira o valor: ')
                valor = int(valor)

                print('\n')
                print(linhas[valor])
                print('\n')

                # Padrão para encontrar o CPF no formato XXX.XXX.XXX-XX
                padrao_cpf = r'\b\d{3}\.\d{3}\.\d{3}-\d{2}\b'
                linha = linhas[valor]  # Suponho que você tenha uma lista de linhas
                match = re.search(padrao_cpf, linha)
                #print(dados)        
            
    except ValueError:
        print("Por favor, insira um valor inteiro.")




#extrair_cpf_pdf(pdf)
#extrair_codigo_barras(pdf)
#extrair_dados_pdf(pdf)
#extrair_linha(pdf)