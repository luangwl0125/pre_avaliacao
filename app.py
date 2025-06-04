import os
import streamlit as st
from datetime import datetime
from docx import Document
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

# Configuração da página
st.set_page_config(page_title="Formulário de Pré-Avaliação Neuropsicológica", layout="wide")

# Título e instruções iniciais
st.title("Formulário de Pré-Avaliação Neuropsicológica")

st.markdown("""
Este formulário tem como objetivo coletar informações iniciais para sua avaliação neuropsicológica.  
Os dados serão mantidos sob sigilo e utilizados apenas para fins clínicos, conforme o Código de Ética Profissional do Psicólogo (CFP).
""")

# Checkbox de consentimento
consentimento = st.checkbox("Declaro que li e concordo com o uso das informações acima para fins de avaliação psicológica.")

# Exibe formulário somente se o consentimento for marcado
if consentimento:
    with st.form(key="form_anamnese"):
        # === DADOS PESSOAIS ===
        st.header("Dados Pessoais")
        nome = st.text_input("Nome completo", max_chars=100)
        email = st.text_input("E-mail")
        telefone = st.text_input("Telefone")
        data_nasc = st.date_input("Data de Nascimento")
        idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
        sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Outro"])
        cidade_estado = st.text_input("Cidade/Estado de nascimento")
        endereco = st.text_input("Endereço completo")
        mao_escrita = st.selectbox("Mão dominante", ["Direita", "Esquerda", "Ambidestro"])
        idiomas = st.multiselect("Idiomas falados", ["Inglês", "Espanhol", "Francês", "Outro"])
        encaminhamento = st.text_input("Encaminhado por")

        st.markdown("---")
        # === QUEIXAS PRINCIPAIS ===
        st.header("Queixas Principais")
        queixas = st.text_area("Descreva as queixas principais", height=80)

        st.markdown("---")
        # === HISTÓRICO MÉDICO E FAMILIAR ===
        st.header("Histórico Médico e Familiar")
        hx_medico = st.text_area("Histórico médico (diagnósticos, datas, intervenções)", height=80)
        hx_familiar = st.text_area("Histórico familiar (neurológico/psiquiátrico)", height=80)
        medicacoes = st.text_area("Medicações em uso atualmente", height=60)

        st.markdown("---")
        # === DESENVOLVIMENTO E ESCOLARIZAÇÃO ===
        st.header("Desenvolvimento e Escolarização")
        desenvolvimento_infantil = st.text_area(
            "Relato do desenvolvimento infantil (marcos motores, fala, etc.)", height=100
        )
        hx_escolar = st.text_area("Histórico escolar (escolas, repetências, desempenho)", height=80)

        st.markdown("---")
        # === ASPECTOS EMOCIONAIS E COMPORTAMENTAIS ===
        st.header("Aspectos Emocionais e Comportamentais")
        sono = st.selectbox("Qualidade do sono", ["Adequado", "Insônia", "Excesso de sono", "Outro"])
        apetite = st.selectbox("Apetite", ["Adequado", "Aumentado", "Reduzido", "Outro"])
        humor = st.selectbox("Humor geral", ["Estável", "Irritável", "Triste", "Ansioso", "Outro"])
        estresse = st.selectbox("Nível de estresse", ["Baixo", "Moderado", "Alto", "Outro"])

        st.markdown("---")
        # === USO DE NEUROTECNOLOGIAS (OPCIONAL) ===
        st.header("Uso de Neurotecnologias")
        uso_neuro = st.text_area(
            "Informe se já utiliza Neurofeedback, tDCS, Hipnose, BrainTap, Muse ou outros", height=60
        )

        st.markdown("---")
        # === OBSERVAÇÕES FINAIS ===
        st.header("Observações Finais")
        observacoes = st.text_area("Informações adicionais", height=80)

        submit_button = st.form_submit_button(label="Enviar Avaliação")

        if submit_button:
            # 1. Geração do arquivo Word
            nome_sanitizado = nome.strip().replace(" ", "_")
            filename = f"avaliacao_{nome_sanitizado}.docx"
            doc = Document()

            # Cabeçalho
            doc.add_heading(f"Pré-Avaliação Neuropsicológica: {nome}", level=1)

            doc.add_paragraph(f"E-mail: {email}")
            doc.add_paragraph(f"Telefone: {telefone}")
            doc.add_paragraph(f"Nascimento: {data_nasc.strftime('%d/%m/%Y')}  (Idade: {idade})")
            doc.add_paragraph(f"Sexo: {sexo}")
            doc.add_paragraph(f"Cidade/Estado de nascimento: {cidade_estado}")
            doc.add_paragraph(f"Endereço: {endereco}")
            doc.add_paragraph(f"Mão dominante: {mao_escrita}")
            doc.add_paragraph(f"Idiomas: {', '.join(idiomas) if idiomas else 'Nenhum'}")
            doc.add_paragraph(f"Encaminhado por: {encaminhamento}")

            # Queixas Principais
            doc.add_page_break()
            doc.add_heading("Queixas Principais", level=2)
            doc.add_paragraph(queixas if queixas else "Nenhuma")

            # Histórico Médico e Familiar
            doc.add_page_break()
            doc.add_heading("Histórico Médico e Familiar", level=2)
            doc.add_paragraph(f"Histórico Médico: {hx_medico if hx_medico else 'Nenhum registrado'}")
            doc.add_paragraph(f"Histórico Familiar: {hx_familiar if hx_familiar else 'Nenhum registrado'}")
            doc.add_paragraph(f"Medicações: {medicacoes if medicacoes else 'Nenhuma'}")

            # Desenvolvimento e Escolarização
            doc.add_page_break()
            doc.add_heading("Desenvolvimento e Escolarização", level=2)





            doc.add_paragraph(
                f"Desenvolvimento Infantil: {desenvolvimento_infantil if desenvolvimento_infantil else 'Não descrito'}"
            )
            doc.add_paragraph(f"Histórico Escolar: {hx_escolar if hx_escolar else 'Não descrito'}")

            # Aspectos Emocionais e Comportamentais
            doc.add_page_break()
            doc.add_heading("Aspectos Emocionais e Comportamentais", level=2)
            doc.add_paragraph(f"Sono: {sono}")
            doc.add_paragraph(f"Apetite: {apetite}")
            doc.add_paragraph(f"Humor: {humor}")
            doc.add_paragraph(f"Nível de estresse: {estresse}")

            # Uso de Neurotecnologias
            doc.add_page_break()
            doc.add_heading("Uso de Neurotecnologias", level=2)
            doc.add_paragraph(uso_neuro if uso_neuro else "Nenhum uso informado")

            # Observações Finais
            doc.add_page_break()
            doc.add_heading("Observações Finais", level=2)
            doc.add_paragraph(observacoes if observacoes else "Nenhuma observação adicional")


            doc.save(filename)
            st.success(f"Arquivo `{filename}` gerado com sucesso.")

            # 2. Enviar por e-mail
            try:
                msg = MIMEMultipart()
                msg["From"] = EMAIL_USER
                msg["To"] = EMAIL_USER
                msg["Subject"] = f"Avaliação de {nome} – {data_nasc.strftime('%d/%m/%Y')}"

                with open(filename, "rb") as attachment:
                    part = MIMEBase(
                        "application",
                        "vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f'attachment; filename="{filename}"',
                    )
                    msg.attach(part)

                server = smtplib.SMTP(EMAIL_SMTP, EMAIL_PORT)
                server.starttls()
                server.login(EMAIL_USER, EMAIL_PASS)
                server.sendmail(EMAIL_USER, EMAIL_USER, msg.as_string())
                server.quit()

                st.success("E-mail enviado com sucesso para o seu endereço.")
                st.info(f"Verifique sua caixa de entrada: {EMAIL_USER}")

            except Exception as e:
                st.error(f"Falha ao enviar e-mail: {e}")
