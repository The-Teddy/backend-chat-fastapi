from os import getenv
import sys

REQUIRED_ENV_VARS = [
    'FAST_API_HOST',
    'FAST_API_PORT',
    'MONGO_URI',
    'MONGO_DB',
    'SECRET_KEY',
    'FROM_EMAIL',
    'HOST_EMAIL',
    'PORT_EMAIL',
    'USERNAME_MAIL',
    'PASSWORD_MAIL',
    'VERIFICATION_URL'
]

def check_env_vars():
    missing_vars = [var for var in REQUIRED_ENV_VARS if not getenv(var)]

    if missing_vars:
        print(f"❌ ERRO: As seguintes variáveis de ambiente estão ausentes: {', '.join(missing_vars)}")
        sys.exit(1)
