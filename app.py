# Versão aprimorada do Formulário de Pré-Avaliação Neuropsicológica
import os
import streamlit as st
from docx import Document
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")
EMAIL_SMTP = os.getenv("EMAIL_SMTP")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))

st.set_page_config(page_title="Avaliação Neuropsicológica", layout="wide")
st.title("Formulário de Pré-Avaliação Neuropsicológica")

st.markdown("""
Este formulário tem como objetivo coletar informações iniciais para sua avaliação neuropsicológica. Os dados serão mantidos sob sigilo e utilizados apenas para fins clínicos, conforme o Código de Ética Profissional do Psicólogo (CFP).
""")

# Consentimento
consentimento = st.checkbox("Declaro que li e concordo com o uso das informações acima para fins de avaliação psicológica.")

if consentimento:
    with st.form(key="form_anamnese"):
        st.header("1. Dados Pessoais")
        nome = st.text_input("Nome completo", max_chars=100)
        email = st.text_input("E-mail para contato")
        telefone = st.text_input("Telefone")
        data_avaliacao = st.date_input("Data da avaliação", datetime.today())
        data_nasc = st.date_input("Data de Nascimento")
        idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
        sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Outro"])
        cidade_nasc = st.text_input("Cidade de nascimento")
        estado_nasc = st.text_input("Estado de nascimento")
        endereco = st.text_input("Endereço completo")
        mao_escrita = st.radio("Mão que usa para escrever", ["Direita", "Esquerda", "Ambidestro"])
        idiomas = st.multiselect("Fala outro(s) idioma(s)?", ["Inglês", "Espanhol", "Francês", "Outro"])
        encaminhamento = st.text_input("Encaminhado por")

        st.header("2. Queixas Principais")
        queixas = st.text_area("Descreva brevemente o motivo da avaliação")

        st.header("3. Sintomas Cognitivos")
        cog_memoria = st.radio("Apresenta dificuldades de memória?", ["Sim", "Não"])
        cog_atencao = st.radio("Apresenta dificuldade de atenção/concentração?", ["Sim", "Não"])
        cog_planejamento = st.radio("Tem dificuldades com organização e planejamento?", ["Sim", "Não"])

        st.header("4. Histórico Médico e Familiar")
        historico_medico = st.text_area("Histórico médico (doenças, internações, medicações)")
        historico_familiar = st.text_area("Histórico familiar (doenças neurológicas, psiquiátricas, etc.)")

        st.header("5. Desenvolvimento e Escolarização")
        desenvolvimento = st.text_area("Relate como foi o desenvolvimento na infância (fala, andar, etc.)")
        historico_escolar = st.text_area("Histórico escolar (repetições, dificuldades, apoio pedagógico)")

        st.header("6. Aspectos Emocionais")
        emocional_sono = st.radio("Alterações de sono?", ["Sim", "Não"])
        emocional_apetite = st.radio("Alterações de apetite?", ["Sim", "Não"])
        emocional_humor = st.radio("Oscilações de humor ou tristeza frequente?", ["Sim", "Não"])

        st.header("7. Observações Finais")
        observacoes = st.text_area("Informações adicionais relevantes")

        submit_button = st.form_submit_button(label="Enviar Avaliação")

        if submit_button:
            filename = f"avaliacao_{nome.strip().replace(' ', '_')}.docx"
            doc = Document()
            doc.add_heading(f"Pré-Avaliação Neuropsicológica: {nome}", level=1)
            doc.add_paragraph(f"Data da Avaliação: {data_avaliacao.strftime('%d/%m/%Y')}")
            doc.add_paragraph(f"E-mail: {email}")
            doc.add_paragraph(f"Telefone: {telefone}")
            doc.add_paragraph(f"Nascimento: {data_nasc.strftime('%d/%m/%Y')} (Idade: {idade})")
            doc.add_paragraph(f"Sexo: {sexo}")
            doc.add_paragraph(f"Cidade/Estado de nascimento: {cidade_nasc}/{estado_nasc}")
            doc.add_paragraph(f"Endereço: {endereco}")
            doc.add_paragraph(f"Mão dominante: {mao_escrita}")
            doc.add_paragraph(f"Idiomas: {', '.join(idiomas) if idiomas else 'Nenhum'}")
            doc.add_paragraph(f"Encaminhado por: {encaminhamento}")
            doc.add_heading("Queixas Principais", level=2)
            doc.add_paragraph(queixas)
            doc.add_heading("Histórico Médico e Familiar", level=2)
            doc.add_paragraph(f"Médico: {historico_medico}")
            doc.add_paragraph(f"Familiar: {historico_familiar}")
            doc.add_heading("Desenvolvimento e Escolarização", level=2)
            doc.add_paragraph(desenvolvimento)
            doc.add_paragraph(historico_escolar)
            doc.add_heading("Aspectos Emocionais", level=2)
            doc.add_paragraph(f"Sono: {emocional_sono}, Apetite: {emocional_apetite}, Humor: {emocional_humor}")
            doc.add_heading("Observações Finais", level=2)
            doc.add_paragraph(observacoes if observacoes else "Nenhuma.")
            doc.save(filename)
            st.success(f"Arquivo `{filename}` gerado com sucesso.")

            try:
                msg = MIMEMultipart()
                msg["From"] = EMAIL_USER
                msg["To"] = email or EMAIL_USER
                msg["Subject"] = f"Avaliação de {nome} – {data_avaliacao.strftime('%d/%m/%Y')}"
                with open(filename, "rb") as attachment:
                    part = MIMEBase("application", "vnd.openxmlformats-officedocument.wordprocessingml.document")
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
                    msg.attach(part)
                server = smtplib.SMTP(EMAIL_SMTP, EMAIL_PORT)
                server.starttls()
                server.login(EMAIL_USER, EMAIL_PASS)
                server.sendmail(EMAIL_USER, email or EMAIL_USER, msg.as_string())
                server.quit()
                st.success("E-mail enviado com sucesso.")
            except Exception as e:
                st.error(f"Erro ao enviar e-mail: {e}")
