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

# Função para gerar documento Word
def gerar_documento(nome, data_avaliacao, email, telefone, data_nasc, idade, sexo, cidade_nasc, estado_nasc,
                     endereco, mao_escrita, idiomas, encaminhamento, queixas, sintomas, condicoes_medicas,
                     cancer_info, psiquiatria_info, outras_condicoes, usa_medicacao, medicacoes,
                     historico_medico, historico_familiar, desenvolvimento_infantil, historico_escolar,
                     emocional_sono, emocional_apetite, emocional_humor, emocional_estresse,
                     uso_neuro, observacoes):
    nome_sanitizado = nome.strip().replace(" ", "_")
    filename = f"avaliacao_{nome_sanitizado}.docx"
    doc = Document()

    doc.add_heading(f"Pré-Avaliação Neuropsicológica: {nome}", level=1)
    doc.add_paragraph(f"Data da Avaliação: {data_avaliacao.strftime('%d/%m/%Y')}")
    doc.add_paragraph(f"E-mail: {email if email else 'Não informado'}")
    doc.add_paragraph(f"Telefone: {telefone if telefone else 'Não informado'}")
    doc.add_paragraph(f"Nascimento: {data_nasc.strftime('%d/%m/%Y')}  (Idade: {idade})")
    doc.add_paragraph(f"Sexo: {sexo}")
    doc.add_paragraph(f"Cidade/Estado de nascimento: {cidade_nasc}/{estado_nasc}")
    doc.add_paragraph(f"Endereço: {endereco if endereco else 'Não informado'}")
    doc.add_paragraph(f"Mão dominante: {mao_escrita}")
    idi_list = [i for i in idiomas if i != "Não"]
    doc.add_paragraph(f"Idiomas: {', '.join(idi_list) if idi_list else 'Nenhum'}")
    doc.add_paragraph(f"Encaminhado por: {encaminhamento if encaminhamento else 'Nenhum'}")

    doc.add_page_break()
    doc.add_heading("2. Queixas Principais", level=2)
    doc.add_paragraph(queixas if queixas else "Nenhuma")

    doc.add_page_break()
    doc.add_heading("3. Sintomas Cognitivos", level=2)
    for pergunta, resposta in sintomas.items():
        doc.add_paragraph(f"{pergunta}: {resposta}")

    doc.add_page_break()
    doc.add_heading("4. Histórico Médico", level=2)
    doc.add_paragraph(f"Condições Médicas: {', '.join(condicoes_medicas) if condicoes_medicas else 'Nenhuma'}")
    if cancer_info: doc.add_paragraph(f"Tipo de câncer: {cancer_info}")
    if psiquiatria_info: doc.add_paragraph(f"Diagnóstico psiquiátrico: {psiquiatria_info}")
    if outras_condicoes: doc.add_paragraph(f"Outras condições: {outras_condicoes}")
    doc.add_paragraph(f"Uso de Medicações: {usa_medicacao} - {medicacoes if medicacoes else 'Nenhum'}")
    doc.add_paragraph(f"Histórico Médico Pessoal: {historico_medico}")
    doc.add_paragraph(f"Histórico Médico Familiar: {historico_familiar}")

    doc.add_page_break()
    doc.add_heading("5. Desenvolvimento Infantil", level=2)
    doc.add_paragraph(desenvolvimento_infantil)

    doc.add_page_break()
    doc.add_heading("6. Desenvolvimento Escolar", level=2)
    doc.add_paragraph(historico_escolar)

    doc.add_page_break()
    doc.add_heading("7. Aspectos Emocionais", level=2)
    doc.add_paragraph(f"Sono: {emocional_sono}")
    doc.add_paragraph(f"Apetite: {emocional_apetite}")
    doc.add_paragraph(f"Humor: {emocional_humor}")
    doc.add_paragraph(f"Estresse: {emocional_estresse}")

    doc.add_page_break()
    doc.add_heading("8. Uso de Neurotecnologias", level=2)
    doc.add_paragraph(uso_neuro)

    doc.add_page_break()
    doc.add_heading("9. Observações Finais", level=2)
    doc.add_paragraph(observacoes)

    doc.save(filename)
    return filename
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
