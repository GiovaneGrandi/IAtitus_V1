# Imports
from flask import Blueprint, request, jsonify, render_template, redirect, url_for, send_file
import google.generativeai as genai
import os
from dotenv import load_dotenv
import sqlite3
import PyPDF2
import shutil
import io
from podcastfy.client import generate_podcast


# Variáveis Super Globais

DB_IATITUS     = './BDIAtitus.db'

SRC_ENV        = './config.env'
SRC_STATIC     = './static/'

SRC_RECUPERADO = 'arquivo_recuperado.pdf'

load_dotenv(SRC_ENV)
API_KEY_GPT    = os.getenv('GPT_API_KEY ')
API_KEY_GEMINI = os.getenv('GEMINI_API_KEY')
API_KEY_ELEVENLABS = os.getenv('ELEVENLABS_API_KEY')

genai.configure(api_key=API_KEY_GEMINI)
MODEL = genai.GenerativeModel('gemini-pro')


# Funções

def extractTextFromPdf(file_path, PkIdArq=0, flgInDb=False):
    
    if flgInDb:
        
        conn = sqlite3.connect(DB_IATITUS)
        cursor = conn.cursor()
        
        cursor.execute(f'SELECT ConteudoArq FROM TBArquivo WHERE PkIdArq = {PkIdArq}')
        conteudo_binario = cursor.fetchone()[0]

        # Escrever o conteúdo em um novo arquivo
        with open(file_path, 'wb') as file:
            
            file.write(conteudo_binario)
    
    with open(file_path, 'rb') as pdf_file:
        reader = PyPDF2.PdfReader(pdf_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text


def splitTextIntoChunks(text, max_tokens=20000):
    """Divide o texto em pedaços menores de no máximo max_tokens."""
    words = text.split()
    chunks = []
    chunk = []
    current_length = 0
    nChunks = 0

    for word in words:
        current_length += len(word) + 1  # +1 para o espaço
        if current_length <= max_tokens:
            chunk.append(word)
        else:
            nChunks += 1
            print(f"{nChunks}° Chunk...\n\n{chunk}\n\n")
            chunks.append(" ".join(chunk))
            chunk = [word]
            current_length = len(word) + 1

    if chunk:
        chunks.append(" ".join(chunk))

    print(f"Número de Chunks: {len(chunks)}")
    return chunks


def summarizeChunk(chunk):
    
    fullQuestion = f"Você é um assistente que resume textos de forma detalhada. Resuma o seguinte texto: {chunk}"
    
    response = MODEL.generate_content(fullQuestion)
    
    response_text = response.candidates[0].content.parts[0].text
    
    return response_text   


def summarizePdf(full_text):
    chunks = splitTextIntoChunks(full_text)
    summaries = []
    nChunks = 0 
    
    for chunk in chunks:
        summaries.append(summarizeChunk(chunk))
        
        print(f"\n{nChunks+1}° chunk resumido...\n")
        print("_______________________________________________________________________________________")
        print(summaries[nChunks])
        print("_______________________________________________________________________________________\n")
        nChunks += 1
        
    print("Resumo concluído...")
    
    # Combinar os resumos e criar um resumo final
    combined_summary = " ".join(summaries)
    print("Lenght do resumo final: ", len(combined_summary))
    return combined_summary


def askQuestionFromPdf(pdfText, question):

    fullQuestion = f"Você é um professor que responde com base em textos fornecidos. Texto: {pdfText}\n\nPergunta: {question}"
    
    response = MODEL.generate_content(fullQuestion)
    
    response_text = response.candidates[0].content.parts[0].text

    return response_text


def get_pdfs_content(conn, pdf_ids):
    
    pdf_files = []
    path = SRC_STATIC+'tempFiles'
    os.makedirs(path, exist_ok=True)
    cursor = conn.cursor()
    
    for pdf_id in pdf_ids:
        cursor.execute("SELECT ConteudoArq AS content, TituloArq AS title FROM TBArquivo WHERE PkIdArq = ?", (pdf_id,))
        result = cursor.fetchone()
        if result:
            pdf_content, title = result
            file_path = os.path.join(path, f"{title}.pdf")
            with open(file_path, 'wb') as f:
                f.write(pdf_content)
            pdf_files.append(file_path)
    cursor.close()
    
    return pdf_files