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

# Carrega variáveis de ambiente
@st.cache_data
def carregar_configuracoes():
    load_dotenv()
    return {
        "EMAIL_USER": os.getenv("EMAIL_USER"),
        "EMAIL_PASS": os.getenv("EMAIL_PASS"),
        "EMAIL_SMTP": os.getenv("EMAIL_SMTP"),
        "EMAIL_PORT": int(os.getenv("EMAIL_PORT", 587))
    }

# Configuração da página
st.set_page_config(page_title="Formulário de Pré-Avaliação Neuropsicológica", layout="wide")

# Título e instruções iniciais
st.title("Formulário de Pré-Avaliação Neuropsicológica")
st.markdown("Este formulário tem como objetivo coletar informações iniciais para sua avaliação neuropsicológica.")

# Checkbox de consentimento
consentimento = st.checkbox("Declaro que li e concordo com o uso das informações para fins de avaliação psicológica.")

if consentimento:
    with st.form("form_avaliacao"):
        # == 1. Dados Pessoais ==
        st.header("1. Dados Pessoais")
        nome = st.text_input("Nome completo:")
        email = st.text_input("E-mail para contato:")
        telefone = st.text_input("Telefone:")
        data_nasc = st.date_input("Data de Nascimento:", min_value=datetime(1900, 1, 1))
        idade = st.number_input("Idade:", min_value=0, max_value=120)
        sexo = st.selectbox("Sexo:", ["Masculino", "Feminino", "Outro"])

        # == 2. Queixas Principais ==
        st.header("2. Queixas Principais")
        queixas = st.text_area("Descreva brevemente o motivo para a avaliação:")

        # == 3. Sintomas Cognitivos ==
        st.header("3. Sintomas Cognitivos")
        cog_concentracao = st.radio("Apresenta dificuldade de concentração?", ["Sim", "Não"])
        cog_memoria = st.radio("Apresenta problemas de memória?", ["Sim", "Não"])

        # == 4. Histórico Médico ==
        st.header("4. Histórico Médico")
        historico = st.text_area("Descreva seu histórico médico relevante:")
        medicamentos = st.text_area("Lista de medicamentos em uso:")

        # == 5. Observações ==
        st.header("5. Observações")
        observacoes = st.text_area("Informações adicionais que considere importantes:")

        # Botão de envio
        enviado = st.form_submit_button("Enviar Avaliação")

        if enviado:
            try:
                # Criar documento Word
                doc = Document()
                doc.add_heading("Pré-Avaliação Neuropsicológica", 0)
                
                # Adicionar informações ao documento
                doc.add_heading("1. Dados Pessoais", 1)
                doc.add_paragraph(f"Nome: {nome}")
                doc.add_paragraph(f"Email: {email}")
                doc.add_paragraph(f"Telefone: {telefone}")
                doc.add_paragraph(f"Data de Nascimento: {data_nasc}")
                doc.add_paragraph(f"Idade: {idade}")
                doc.add_paragraph(f"Sexo: {sexo}")

                doc.add_heading("2. Queixas Principais", 1)
                doc.add_paragraph(queixas)

                doc.add_heading("3. Sintomas Cognitivos", 1)
                doc.add_paragraph(f"Dificuldade de concentração: {cog_concentracao}")
                doc.add_paragraph(f"Problemas de memória: {cog_memoria}")

                doc.add_heading("4. Histórico Médico", 1)
                doc.add_paragraph(f"Histórico: {historico}")
                doc.add_paragraph(f"Medicamentos: {medicamentos}")

                doc.add_heading("5. Observações", 1)
                doc.add_paragraph(observacoes)

                # Salvar documento
                nome_arquivo = f"avaliacao_{nome.strip().replace(' ', '_')}.docx"
                doc.save(nome_arquivo)
                
                st.success(f"Avaliação salva com sucesso no arquivo {nome_arquivo}")
                
            except Exception as e:
                st.error(f"Erro ao processar o formulário: {str(e)}")

def salvar_backup(dados):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_{timestamp}.json"
    with open(backup_file, 'w') as f:
        json.dump(dados, f)

logging.basicConfig(
    filename='form_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
