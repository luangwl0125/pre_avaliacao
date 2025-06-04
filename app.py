import os
import streamlit as st
from datetime import datetime
from docx import Document
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import logging

# Configuração de logging
logging.basicConfig(
    filename='form_log.txt',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Função para carregar variáveis de ambiente
def carregar_configuracoes():
    load_dotenv()
    return {
        "EMAIL_USER": os.getenv("EMAIL_USER"),
        "EMAIL_PASS": os.getenv("EMAIL_PASS"),
        "EMAIL_SMTP": os.getenv("EMAIL_SMTP"),
        "EMAIL_PORT": int(os.getenv("EMAIL_PORT", 587))
    }

# Função para gerar documento Word (mantida como está)
# Função para envio de e-mail (mantida como está)

# UI Streamlit
def main():
    st.set_page_config(page_title="Formulário de Pré-Avaliação", layout="wide")
    st.title("Formulário de Pré-Avaliação Neuropsicológica")
    st.markdown("Este formulário coleta dados iniciais para avaliação neuropsicológica.")

    if st.checkbox("Concordo com o uso das informações para fins de avaliação psicológica."):
        with st.form("form_avaliacao"):
            st.subheader("1. Dados Pessoais")
            col1, col2, col3 = st.columns(3)
            with col1:
                nome = st.text_input("Nome completo")
            with col2:
                email = st.text_input("E-mail")
            with col3:
                telefone = st.text_input("Telefone")

            col4, col5, col6 = st.columns(3)
            with col4:
                data_avaliacao = st.date_input("Data da Avaliação", datetime.today())
            with col5:
                data_nasc = st.date_input("Data de Nascimento", min_value=datetime(1900,1,1), max_value=datetime.today())
            with col6:
                idade = st.number_input("Idade", min_value=0, max_value=120)

            col7, col8, col9 = st.columns(3)
            with col7:
                sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Outro"])
            with col8:
                cidade_nasc = st.text_input("Cidade de nascimento")
            with col9:
                estado_nasc = st.text_input("Estado de nascimento")

            endereco = st.text_input("Endereço completo")
            mao_escrita = st.radio("Mão dominante", ["Direita", "Esquerda", "Ambidestro"])
            idiomas = st.multiselect("Idiomas falados", ["Não", "Inglês", "Espanhol", "Francês", "Outro"])
            encaminhamento = st.text_input("Encaminhado por")

            st.subheader("2. Queixas Principais")
            queixas = st.text_area("Descreva brevemente o motivo da avaliação")

            st.subheader("3. Sintomas Cognitivos")
            sintomas = {}
            for pergunta in [
                "Dificuldade de concentração",
                "Esquecimento frequente",
                "Lentidão no raciocínio",
                "Perda de objetos",
                "Repetição de perguntas",
                "Dificuldade de foco",
                "Sensação de desorientação",
                "Dificuldade para resolver problemas",
                "Necessidade de lembretes",
                "Cansaço mental excessivo",
                "Troca de palavras",
                "Anomia"]:
                sintomas[pergunta] = st.radio(pergunta, ["Sim", "Não"], key=pergunta)

            with st.expander("📌 Histórico Médico"):
                condicoes_medicas = st.multiselect("Condições médicas", [
                    "Hipertensão arterial", "Diabetes", "Doenças cardíacas", "Doenças neurológicas",
                    "Doenças psiquiátricas", "Câncer", "Outra(s) condição(ões) relevante(s)"])

                cancer_info = st.text_input("Tipo de câncer") if "Câncer" in condicoes_medicas else ""
                psiquiatria_info = st.text_input("Diagnóstico psiquiátrico") if "Doenças psiquiátricas" in condicoes_medicas else ""
                outras_condicoes = st.text_input("Outras condições") if "Outra(s) condição(ões) relevante(s)" in condicoes_medicas else ""
                usa_medicacao = st.radio("Uso de medicação?", ["Sim", "Não"])
                medicacoes = st.text_area("Informações sobre medicamentos")
                historico_medico = st.text_area("Histórico médico atual e passado")
                historico_familiar = st.text_area("Histórico médico familiar")

            with st.expander("🧠 Desenvolvimento e Escolaridade"):
                desenvolvimento_infantil = st.text_area("Desenvolvimento infantil")
                historico_escolar = st.text_area("Desenvolvimento escolar")

            st.subheader("7. Aspectos Emocionais")
            emocional_sono = st.radio("Alterações de sono", ["Sim", "Não"])
            emocional_apetite = st.radio("Alterações de apetite", ["Sim", "Não"])
            emocional_humor = st.radio("Oscilações de humor", ["Sim", "Não"])
            emocional_estresse = st.radio("Nível de estresse", ["Baixo", "Moderado", "Alto"])

            uso_neuro = st.text_area("Uso de neurotecnologias")
            observacoes = st.text_area("Observações finais")

            enviado = st.form_submit_button("Enviar Avaliação")

            if enviado:
                if not nome.strip():
                    st.warning("O campo 'Nome completo' é obrigatório.")
                    st.stop()
                if not email.strip():
                    st.warning("O campo 'E-mail' é obrigatório.")
                    st.stop()

                try:
                    arquivo = gerar_documento(
                        nome, data_avaliacao, email, telefone, data_nasc, idade, sexo, cidade_nasc, estado_nasc,
                        endereco, mao_escrita, idiomas, encaminhamento, queixas, sintomas, condicoes_medicas,
                        cancer_info, psiquiatria_info, outras_condicoes, usa_medicacao, medicacoes,
                        historico_medico, historico_familiar, desenvolvimento_infantil, historico_escolar,
                        emocional_sono, emocional_apetite, emocional_humor, emocional_estresse,
                        uso_neuro, observacoes)

                    st.success(f"Arquivo '{arquivo}' gerado com sucesso!")
                    with open(arquivo, "rb") as f:
                        st.download_button("📄 Baixar Avaliação", f, file_name=arquivo)

                    if email:
                        try:
                            enviar_email(email, f"Avaliação de {nome} – {data_avaliacao.strftime('%d/%m/%Y')}", arquivo)
                            st.success("E-mail enviado com sucesso!")
                        except Exception as e:
                            st.warning(f"Não foi possível enviar o e-mail: {e}")

                except Exception as e:
                    st.error(f"Erro ao processar o formulário: {e}")

if __name__ == "__main__":
    main()
