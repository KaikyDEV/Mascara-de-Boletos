﻿# Mascara-de-Boletos

Este código Python é uma automação para processamento de arquivos PDF. Primeiramente, ele verifica continuamente uma pasta de entrada em busca de novos arquivos PDF. Quando encontra um arquivo, extrai informações específicas do PDF, atualiza um arquivo HTML com esses dados, e realiza um corte específico no PDF. Em seguida, converte partes do PDF em imagens, concatena essas imagens e converte de volta para PDF, usando senhas de proteção extraídas do PDF original. Após o processamento, move os arquivos resultantes para uma pasta separada baseada na data atual.
