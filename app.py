import os
import streamlit as st
from datetime import datetime
from docx import Document
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import json
import logging

# Define o caminho base do aplicativo
BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# Carrega variáveis de ambiente
@st.cache_data
def carregar_configuracoes():
    """
    Carrega as configurações do arquivo .env
    Retorna um dicionário com as configurações de email
    """
    load_dotenv(os.path.join(BASE_PATH, '.env'))
    return {
        "EMAIL_USER": os.getenv("EMAIL_USER"),
        "EMAIL_PASS": os.getenv("EMAIL_PASS"),
        "EMAIL_SMTP": os.getenv("EMAIL_SMTP"),
        "EMAIL_PORT": int(os.getenv("EMAIL_PORT", 587))
    }

# Configuração de logging
logging.basicConfig(
    filename=os.path.join(BASE_PATH, 'form_log.txt'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Cria diretório para arquivos se não existir
ARQUIVOS_DIR = os.path.join(BASE_PATH, 'arquivos')
os.makedirs(ARQUIVOS_DIR, exist_ok=True)

# Configuração da página
st.set_page_config(
    page_title="Formulário de Pré-Avaliação Neuropsicológica",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Título e instruções iniciais
st.title("Formulário de Pré-Avaliação Neuropsicológica")

st.markdown("""
Este formulário tem como objetivo coletar informações iniciais para sua avaliação neuropsicológica.  
Os dados serão mantidos sob sigilo e utilizados apenas para fins clínicos, conforme o Código de Ética Profissional do Psicólogo (CFP) e a Resolução CFP nº 11/2018.
""") 