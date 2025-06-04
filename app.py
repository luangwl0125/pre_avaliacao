import streamlit as st
from docx import Document
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.utils import parseaddr

# Carrega credenciais do Streamlit Secrets
EMAIL_SMTP = st.secrets["email"]["smtp"]
EMAIL_PORT = st.secrets["email"]["port"]
EMAIL_USER = st.secrets["email"]["user"]
EMAIL_PASS = st.secrets["email"]["pass"]

st.set_page_config(page_title="Avaliação Neuropsicológica", layout="wide")
st.title("Formulário de Pré-Avaliação Neuropsicológica")

st.markdown("""
Este formulário tem como objetivo coletar informações iniciais para sua avaliação neuropsicológica.  
Os dados serão mantidos sob sigilo e utilizados apenas para fins clínicos, conforme o Código de Ética Profissional do Psicólogo (CFP).
""")

# Consentimento
consentimento = st.checkbox("Declaro que li e concordo com o uso das informações acima para fins de avaliação psicológica.")

if consentimento:
    with st.form(key="form_anamnese"):
        # == 1. Dados Pessoais ==
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
            "Data de Nascimento:",
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
        idiomas = st.multiselect(
            "Fala outro(s) idioma(s)?",
            ["Não", "Inglês", "Espanhol", "Francês", "Outro"]
        )
        encaminhamento = st.text_input("Se você foi encaminhado(a) por algum profissional de saúde, informe aqui:")

        # == 2. Queixas Principais ==
        st.header("2. Queixas Principais")
        queixas = st.text_area("Descreva brevemente o motivo para a avaliação:")

        # == 3. Sintomas Cognitivos ==
        st.header("3. Sintomas Cognitivos")
        cog_concentracao = st.radio("Apresenta dificuldade de concentração?", ["Sim", "Não"])
        cog_esquecimento = st.radio("Apresenta esquecimento frequente de compromissos ou informações recentes?", ["Sim", "Não"])
        cog_raciocinio = st.radio("Apresenta lentidão no raciocínio?", ["Sim", "Não"])
        cog_confusao = st.radio("Apresenta confusão mental?", ["Sim", "Não"])
        cog_decisoes = st.radio("Apresenta dificuldade para tomar decisões?", ["Sim", "Não"])
        cog_desatencao = st.radio("Apresenta desatenção a detalhes?", ["Sim", "Não"])
        cog_planejamento = st.radio("Apresenta dificuldade em planejar ou organizar tarefas?", ["Sim", "Não"])
        cog_mente_vazia = st.radio('Apresenta sensação de "mente vazia" ou "travada"?', ["Sim", "Não"])
        cog_instrucoes = st.radio("Apresenta problemas para compreender instruções?", ["Sim", "Não"])
        cog_perda_objetos = st.radio("Apresenta perda de objetos com frequência?", ["Sim", "Não"])
        cog_repeticao = st.radio("Apresenta repetição de perguntas ou frases?", ["Sim", "Não"])
        cog_foco = st.radio("Apresenta dificuldade em manter o foco durante conversas?", ["Sim", "Não"])
        cog_desorientacao = st.radio("Apresenta sensação de desorientação (tempo, espaço, pessoas)?", ["Sim", "Não"])
        cog_problemas = st.radio("Apresenta dificuldade para resolver problemas cotidianos?", ["Sim", "Não"])
        cog_lembretes = st.radio("Apresenta necessidade constante de listas ou lembretes?", ["Sim", "Não"])
        cog_cansaco = st.radio("Apresenta sensação de cansaço mental excessivo após esforço intelectual?", ["Sim", "Não"])
        cog_palavras = st.radio("Apresenta troca ou inversão de palavras ao falar ou escrever?", ["Sim", "Não"])
        cog_anomia = st.radio("Apresenta dificuldade para encontrar palavras durante a fala (anomia)?", ["Sim", "Não"])

        # == 4. Histórico Médico: Situação atual e passada ==
        st.header("4. Histórico Médico: Situação atual e passada")
        condicoes_medicas = st.multiselect(
            "Marque as condições médicas que se aplicam:",
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

        st.subheader("Uso de Medicações")
        usa_medicacao = st.radio("Faz uso contínuo ou recente de medicações?", ["Não", "Sim"], key="usa_medicacao")
        medicacoes = st.text_area(
            "Nome do(s) medicamento(s) – Dosagem – Motivo – Por quem foi prescrito:"
        )

        historico_medico = st.text_area("Descreva seu histórico médico atual e passado:")
        historico_familiar = st.text_area("Descreva histórico médico familiar:")

        # == 5. Aspectos do Desenvolvimento Infantil ==
        st.header("5. Aspectos do Desenvolvimento Infantil")
        st.markdown("""
        **Como foi o desenvolvimento na infância? Indique se você teve alguma dificuldade em algum dos aspectos a seguir:**
        
        - **Desenvolvimento motor grosso:** Sentar-se sem apoio, engatinhar, andar sozinho, correr, pular e subir escadas.  
        - **Desenvolvimento motor fino:** Agilidade para segurar objetos pequenos com precisão, usar talheres, lápis ou tesoura, vestir-se e despir-se de forma autônoma.  
        - **Desenvolvimento da fala e linguagem:** Emissão de sons na idade esperada, formação de palavras e frases, compreensão de comandos e clareza na articulação.  
        - **Desenvolvimento cognitivo:** Resolver problemas simples, reconhecimento de formas, cores e números, memória e raciocínio.  
        - **Desenvolvimento emocional:** Expressão adequada de sentimentos (alegria, frustração, medo), controle emocional em situações desafiadoras, vinculação afetiva com cuidadores.  
        - **Desenvolvimento social:** Interação com adultos e outras crianças, partilha de brinquedos, participação em atividades em grupo, seguir regras simples.  
        - **Autonomia:** Higiene pessoal (lavar as mãos, escovar os dentes), controle de esfíncteres, alimentação independente.  
        - **Aquisição de hábitos e rotinas:** Sono regular, alimentação equilibrada, adaptação ao ambiente escolar.
        """)

        # == 6. Aspectos do Desenvolvimento Escolar ==
        st.header("6. Aspectos do Desenvolvimento Escolar")
        historico_escolar = st.text_area(
            "Descreva como foi a escolarização (repetições, dificuldades, apoio pedagógico):"
        )

        # == 7. Aspectos Emocionais ==
        st.header("7. Aspectos Emocionais")
        emocional_sono = st.radio("Alterações de sono?", ["Sim", "Não"])
        emocional_apetite = st.radio("Alterações de apetite?", ["Sim", "Não"])
        emocional_humor = st.radio("Oscilações de humor ou tristeza frequente?", ["Sim", "Não"])

        # == 8. Observações Finais ==
        st.header("8. Observações Finais")
        observacoes = st.text_area("Informações adicionais relevantes:")

        submit_button = st.form_submit_button(label="Enviar Avaliação")

        if submit_button:
            # Define nome do arquivo Word
            filename = f"avaliacao_{nome.strip().replace(' ', '_')}.docx"
            doc = Document()

            # Cabeçalho
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

            # Queixas
            doc.add_heading("Queixas Principais", level=2)
            doc.add_paragraph(queixas)

            # Histórico Médico e Familiar
            doc.add_heading("Histórico Médico e Familiar", level=2)
            doc.add_paragraph(f"Médico: {historico_medico}")
            doc.add_paragraph(f"Familiar: {historico_familiar}")
            doc.add_paragraph(f"Medicações: {medicacoes}")

            # Desenvolvimento e Escolarização
            doc.add_heading("Desenvolvimento e Escolarização", level=2)
            doc.add_paragraph("Relato do desenvolvimento infantil conforme informações acima.")
            doc.add_paragraph(f"Histórico Escolar: {historico_escolar}")

            # Aspectos Emocionais
            doc.add_heading("Aspectos Emocionais", level=2)
            doc.add_paragraph(
                f"Sono: {emocional_sono}, Apetite: {emocional_apetite}, Humor: {emocional_humor}"
            )

            # Observações Finais
            doc.add_heading("Observações Finais", level=2)
            doc.add_paragraph(observacoes if observacoes else "Nenhuma.")

            # Salva o arquivo
            doc.save(filename)
            st.success(f"Arquivo `{filename}` gerado com sucesso.")

            # Validação do e-mail antes de enviar
            destinatario = email.strip()
            if not destinatario or "@" not in parseaddr(destinatario)[1]:
                destinatario = EMAIL_USER  # envia para seu próprio e-mail caso o usuário não informe corretamente

            # Envio por e-mail com EHLO + STARTTLS + validação de destinatário
            try:
                msg = MIMEMultipart()
                msg["From"] = EMAIL_USER
                msg["To"] = destinatario
                msg["Subject"] = f"Avaliação de {nome} – {data_avaliacao.strftime('%d/%m/%Y')}"

                with open(filename, "rb") as attachment:
                    part = MIMEBase(
                        "application",
                        "vnd.openxmlformats-officedocument.wordprocessingml.document"
                    )
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        "Content-Disposition",
                        f'attachment; filename="{filename}"'
                    )
                    msg.attach(part)

                server = smtplib.SMTP(EMAIL_SMTP, EMAIL_PORT)
                server.ehlo()                 # Identifica-se ao servidor
                server.starttls()             # Inicia criptografia TLS
                server.ehlo()                 # Reenvia identificação após TLS
                server.login(EMAIL_USER, EMAIL_PASS)
                server.sendmail(EMAIL_USER, destinatario, msg.as_string())
                server.quit()
                st.success("E-mail enviado com sucesso.")
            except Exception as e:
                st.error(f"Erro ao enviar e-mail: {e}")
