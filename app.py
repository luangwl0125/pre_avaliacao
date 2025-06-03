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
        nome = st.text_input("Nome completo:", max_chars=100)
        email = st.text_input("E-mail para contato:")
        telefone = st.text_input("Telefone:")
        data_avaliacao = st.date_input(
            "Data da avaliação:",
            datetime.today(),
            format="DD/MM/YYYY"
        )
        data_nasc = st.date_input(
            "Data de Nascimento",
            format="DD/MM/YYYY",
            min_value=datetime(1900, 1, 1),
            max_value=datetime.today()
        )
        idade = st.number_input("Idade:", min_value=0, max_value=120, step=1)
        sexo = st.selectbox("Sexo:", ["Masculino", "Feminino", "Outro"])
        cidade_nasc = st.text_input("Cidade de nascimento:")
        estado_nasc = st.text_input("Estado de nascimento:")
        endereco = st.text_input("Endereço completo:")
        mao_escrita = st.radio("Mão que usa para escrever:", ["Direita", "Esquerda", "Ambidestro"])
        idiomas = st.multiselect("Fala outro(s) idioma(s)?", ["Não", "Inglês", "Espanhol", "Francês", "Outro"])
        encaminhamento = st.text_input("Se você foi encaminhado(a) por algum profissional de saúde, por favor informar aqui:")

        st.header("2. Queixas Principais")
        queixas = st.text_area("Descreva brevemente o motivo para a avaliação")

        st.header("3. Sintomas Cognitivos")  
        cog_memoria = st.radio("Apresenta dificuldade de concentração?", ["Sim", "Não"])
        cog_memoria = st.radio("Apresenta esquecimento frequente de compromissos ou informações recentes?", ["Sim", "Não"])
        cog_memoria = st.radio("Apresenta lentidão no raciocínio?", ["Sim", "Não"])
        cog_memoria = st.radio("Apresenta confusão mental?", ["Sim", "Não"])
        cog_memoria = st.radio("Apresenta dificuldade para tomar decisões?", ["Sim", "Não"])
        cog_memoria = st.radio("Apresenta desatenção a detalhes?", ["Sim", "Não"])
        cog_memoria = st.radio("Apresenta dificuldade em planejar ou organizar tarefas?", ["Sim", "Não"])
        cog_memoria = st.radio("Apresenta sensação de "mente vazia" ou "travada"?", ["Sim", "Não"])
        cog_memoria = st.radio("Apresenta problemas para compreender instruções?", ["Sim", "Não"])
        cog_memoria = st.radio("Apresenta perda de objetos com frequência?", ["Sim", "Não"])
        cog_memoria = st.radio("Apresenta repetição de perguntas ou frases?", ["Sim", "Não"])
        cog_memoria = st.radio("Apresenta dificuldade em manter o foco durante conversas?", ["Sim", "Não"])
        cog_memoria = st.radio("Apresenta sensação de desorientação - tempo, espaço, pessoas?", ["Sim", "Não"])
        cog_memoria = st.radio("Apresenta dificuldade para resolver problemas cotidianos?", ["Sim", "Não"])
        cog_memoria = st.radio("Apresenta necessidade constante de listas ou lembretes?", ["Sim", "Não"])
        cog_memoria = st.radio("Apresenta sensação de cansaço mental excessivo após esforço intelectual?", ["Sim", "Não"])
        cog_memoria = st.radio("Apresenta troca ou inversão de palavras ao falar ou escrever?", ["Sim", "Não"])
        cog_memoria = st.radio("Apresenta dificuldade para encontrar palavras durante a fala - anomia?", ["Sim", "Não"])

st.header("4. Histórico Médico - Preencha conforme sua situação atual e passada:")
# 1. Condições médicas
st.subheader("1. Você possui ou já teve alguma das seguintes condições médicas?")
condicoes_medicas = st.multiselect(
    "Marque as que se aplicam:",
    [
        "Hipertensão arterial",
        "Diabetes",
        "Problemas cardíacos",
        "Doenças respiratórias crônicas (ex: asma, DPOC)",
        "Doenças neurológicas (ex: epilepsia, AVC, Parkinson)",
        "Doenças autoimunes (ex: lúpus, artrite reumatoide)",
        "Câncer",
        "Doenças psiquiátricas",
        "Outra(s) condição(ões) relevante(s)"
    ]
)

if "Câncer" in condicoes_medicas:
    cancer_info = st.text_input("Especifique o tipo de câncer e a data do diagnóstico:")

if "Doenças psiquiátricas" in condicoes_medicas:
    psiquiatria_info = st.text_input("Especifique o diagnóstico psiquiátrico:")

if "Outra(s) condição(ões) relevante(s)" in condicoes_medicas:
    outras_condicoes = st.text_input("Descreva outras condições médicas relevantes:")

# 2. Internações
st.subheader("2. Já foi internado(a)?")
internado = st.radio("Selecione uma opção:", ["Não", "Sim"])
if internado == "Sim":
    detalhes_internacao = st.text_area("Descreva motivo(s), local(is) e data(s) das internações:")

# 3. Medicações
st.subheader("3. Faz uso contínuo ou recente de medicações?")
usa_medicacao = st.radio("Selecione uma opção:", ["Não", "Sim"])
medicacoes = []
if usa_medicacao == "Sim":
    num_meds = st.number_input("Quantos medicamentos deseja informar?", min_value=1, max_value=10, step=1)
    for i in range(int(num_meds)):
        st.markdown(f"**Medicação {i+1}**")
        nome = st.text_input(f"Nome do medicamento:", key=f"nome_{i}")
        dose = st.text_input("Dose diária:", key=f"dose_{i}")
        motivo = st.text_input("Motivo do uso:", key=f"motivo_{i}")
        prescrito_por = st.text_input("Prescrito por (profissional):", key=f"prof_{i}")
        medicacoes.append({
            "Nome": nome,
            "Dose": dose,
            "Motivo": motivo,
            "Prescrito por": prescrito_por
        })

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
