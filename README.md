# Formulário de Pré-Avaliação Neuropsicológica

## Descrição

Este projeto implementa um formulário online de avaliação neuropsicológica que gera um arquivo Word (.docx) e o envia por e-mail ao responsável. A interface foi construída com Streamlit para permitir preenchimento remoto e coleta segura dos dados.

## Pré-requisitos

* Python 3.11 ou superior
* Conta de e-mail com senha de app (para envio SMTP)
* Git (opcional, para controle de versão)
* Acesso à internet (apenas para deploy)

## Instalação e Configuração

1. Clone o repositório:
```bash
git clone https://github.com/luangwl0125/pre_avaliacao.git
cd pre_avaliacao
```

2. Crie e ative um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Configure as variáveis de ambiente:
Crie um arquivo `.env` na raiz do projeto com:
```
EMAIL_USER=seu_email@exemplo.com
EMAIL_PASS=sua_senha_de_app
EMAIL_SMTP=smtp.gmail.com
EMAIL_PORT=587
```

## Uso

1. Execute o aplicativo:
```bash
streamlit run app.py
```

2. Acesse o formulário no navegador (geralmente http://localhost:8501)

## Estrutura do Projeto

```
pre_avaliacao/
├── .env                # Configurações de email (não versionado)
├── .venv/              # Ambiente virtual Python
├── app.py             # Aplicativo principal
├── requirements.txt   # Dependências do projeto
├── form_log.txt      # Logs do sistema
└── arquivos/         # Documentos gerados
```

## Segurança e Conformidade

Os dados dos pacientes são tratados conforme o Código de Ética Profissional do Psicólogo e a Resolução CFP nº 11/2018.

## Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes. 