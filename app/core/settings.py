from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    SECRET: str
    ALGORITHM: str
    DATABASE_URL: str

    model_config = SettingsConfigDict(env_file='.env', extra='ignore')


settings = Settings()


tags_metadata = [
    {
        'name': 'auth',
        'description': 'Operação de Atenticação'
    },
    {
        'name': 'accounts',
        'description': 'Registros de Contas Bancárias'
    },
    {
        'name': 'transactions',
        'description': 'Registros de Transações Bancárias'
    },

]

description = """
API BANCÁRIA

Desafio do Bootcamp LuizaLabs pela DIO

## auth
Para realização autenticação básica da API

## accounts
* **List Accounts** - Lista contas bancárias cadastradas
* **Create Account** - Cadastra conta bancária
* **List Account by ID** - Lista conta bancária por ID
* **Update Account** - Atualiza dados de conta cadastrada \
    (apenas o nome do titular)
* **Delete Account** - Deleta registro conta bancária

## transactions
* **Make Deposit** - Realiza depósito
* **Make Withdrawal** - Realiza saque
* **Get Statement** - Visualiza Extrato
"""

api_metadata = {
    'title': 'API BANCÁRIA',
    'summary': 'Desafio API Bancária com FastAPI',
    'description': description,
    'version': '1.0.0',
    'openapi_url': '/api/v1/openapi.json',
    'openapi_tags': tags_metadata,
    'docs_url': '/api/v1/docs',
    'redoc_url': '/api/v1/redoc',
    'contact': {
        'name': 'Ciro Bezerra',
        'url': 'https://cirobezerradev.github.io/resume/',
        'email': 'cirobezerradev@gmail.com'
    }
}
