import streamlit as st
from docx import Document
from datetime import datetime

st.set_page_config(page_title="Avaliação Neuropsicológica", layout="wide")
st.title("Formulário de Avaliação Neuropsicológica")

with st.form(key="form_anamnese"):
    # Dados Pessoais
    st.header("Dados Pessoais")
    nome = st.text_input("Nome completo", max_chars=100)
    data_avaliacao = st.date_input("Data da avaliação", datetime.today())
    telefone = st.text_input("Telefone")
    data_nasc = st.date_input("Data de Nascimento")
    idade = st.number_input("Idade", min_value=0, max_value=120, step=1)
    sexo = st.selectbox("Sexo", ["Masculino", "Feminino", "Outro"])
    endereco = st.text_input("Endereço completo")
    cidade_estado = st.text_input("Cidade e Estado de nascimento")
    mao_escrita = st.radio("Mão que usa para escrever", ["Direita", "Esquerda", "Ambidestro"])
    idiomas = st.multiselect("Fala outro(s) idioma(s)?", ["Inglês", "Espanhol", "Francês", "Outro"])
    diagnosticos = st.text_area("Diagnóstico(s) médico(s)", help="Liste diagnósticos prévios, se houver")
    encaminhamento = st.text_input("Encaminhado por")

    st.markdown("---")
    # Sintomas Físicos (exemplo)
    st.header("Sintomas Físicos")
    dor_cabeca = st.checkbox("Dor de cabeça")
    if dor_cabeca:
        dt_dor = st.date_input("   Data de início da dor de cabeça", key="dt_dor_cabeca")
    tontura = st.checkbox("Tontura/vertigem")
    if tontura:
        dt_tontura = st.date_input("   Data de início da tontura", key="dt_tontura")
    # (Continue conforme PDF)

    st.markdown("---")
    # Aspectos Sensórios (exemplo)
    st.header("Aspectos Sensórios")
    perda_sensacao = st.checkbox("Perda de sensação/entorpecimento")
    if perda_sensacao:
        lado_sens = st.selectbox("   Lado afetado", ["Esquerdo", "Direito", "Ambos"], key="lado_sens")
        dt_perda_sens = st.date_input("   Data de início", key="dt_perda_sens")
    formigamento = st.checkbox("Formigamento")
    if formigamento:
        lado_formig = st.selectbox("   Lado afetado", ["Esquerdo", "Direito", "Ambos"], key="lado_formig")
        dt_formig = st.date_input("   Data de início", key="dt_formig")
    # (Continue conforme PDF)

    st.markdown("---")
    # Funções Cognitivas (exemplo)
    st.header("Funções Cognitivas")
    cog_novas = st.radio("Dificuldade em aprender novas tarefas?", ["Sim", "Não"], key="cog_novas")
    if cog_novas == "Sim":
        dt_cog_novas = st.date_input("   Data do início", key="dt_cog_novas")
    cog_problemas = st.radio("Dificuldade em resolver problemas cotidianos?", ["Sim", "Não"], key="cog_problemas")
    if cog_problemas == "Sim":
        dt_cog_problemas = st.date_input("   Data do início", key="dt_cog_problemas")
    # (Continue conforme PDF)

    st.markdown("---")
    # Linguagem e Matemática (exemplo)
    st.header("Linguagem e Habilidades Matemáticas")
    lang_palavras = st.radio("Dificuldade em encontrar palavras?", ["Sim", "Não"], key="lang_palavras")
    if lang_palavras == "Sim":
        dt_lang_palavras = st.date_input("   Data do início", key="dt_lang_palavras")
    lang_compreende = st.radio("Dificuldade em compreender fala alheia?", ["Sim", "Não"], key="lang_compreende")
    if lang_compreende == "Sim":
        dt_lang_compreende = st.date_input("   Data do início", key="dt_lang_compreende")
    math_dificuldade = st.radio("Dificuldade com matemática?", ["Sim", "Não"], key="math_dificuldade")
    if math_dificuldade == "Sim":
        dt_math = st.date_input("   Data do início", key="dt_math")
    # (Continue conforme PDF)

    st.markdown("---")
    # Humor, Comportamento e Personalidade (exemplo)
    st.header("Humor, Comportamento e Personalidade")
    tristeza = st.selectbox("Tristeza ou depressão", ["Nenhuma", "Leve", "Moderada", "Severa"], key="tristeza")
    if tristeza != "Nenhuma":
        dt_tristeza = st.date_input("   Data do início", key="dt_tristeza")
    ansiedade = st.selectbox("Ansiedade ou nervosismo", ["Nenhuma", "Leve", "Moderada", "Severa"], key="ansiedade")
    if ansiedade != "Nenhuma":
        dt_ansiedade = st.date_input("   Data do início", key="dt_ansiedade")
    # (Continue conforme PDF)

    st.markdown("---")
    # Histórico Médico e Outras Seções (exemplo)
    st.header("Histórico Médico e Pessoal")
    historico_medico = st.text_area("Histórico médico relevante", height=120)
    historico_familiar = st.text_area("Histórico familiar de doenças neurológicas/psiquiátricas", height=120)
    historico_escolar = st.text_area("Histórico escolar (desempenho, repetições etc.)", height=120)
    # (Continue conforme PDF)

    st.markdown("---")
    st.header("Observações Finais")
    observacoes = st.text_area("Informações adicionais", height=100)

    submit_button = st.form_submit_button(label="Enviar Avaliação")

    if submit_button:
        # Exemplo de geração de relatório Word (opcional):
        doc = Document()
        doc.add_heading(f"Avaliação de {nome}", level=1)
        doc.add_paragraph(f"Data da Avaliação: {data_avaliacao.strftime('%d/%m/%Y')}")
        doc.add_paragraph(f"Telefone: {telefone}")
        doc.add_paragraph(f"Data de Nascimento: {data_nasc.strftime('%d/%m/%Y')} (Idade: {idade})")
        # (Adicione outros campos conforme necessidade)
        filename = f"avaliacao_{nome.replace(' ', '_')}.docx"
        doc.save(filename)
        st.success(f"Avaliação salva como `{filename}`.")  
        st.info("Encaminhe o arquivo Word por e-mail ou WhatsApp para o paciente.")  
