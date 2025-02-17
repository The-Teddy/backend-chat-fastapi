from aiosmtplib import SMTP
from email.message import EmailMessage
from os import getenv, path
from jinja2 import Environment, FileSystemLoader
from app.utils import create_access_token
from datetime import timedelta
from app.repositories import UserRepository

class EmailService:
    
    user_repositoty = UserRepository()

    async def send_email(self, subject: str, to_email: str, name: str):

        FROM_EMAIL          = "chatweb@gmail.com"
        HOST_EMAIL          = getenv('HOST_EMAIL')
        PORT_EMAIL          = getenv('PORT_EMAIL')
        USERNAME_MAIL       = getenv("USERNAME_MAIL")
        PASSWORD_EMAIL      = getenv("PASSWORD_EMAIL")
        TOKEN               = await create_access_token({"email": to_email},timedelta(hours=1))
        VERIFICATION_URL    = getenv('VERIFICATION_URL') + TOKEN
        BASE_DIR            = path.dirname(path.abspath(__file__))
        TEMPLATES_DIR       = path.join(BASE_DIR, "../templates")


        env                 = Environment(loader=FileSystemLoader(TEMPLATES_DIR))
        template            = env.get_template("verification_email.html") 
        html_content        = template.render(name=name, verification_url=VERIFICATION_URL, app_name="Chat Web")

        message = EmailMessage()
        message.set_content(f"Este é um email em HTML, mas seu cliente de email não suporta esse formato. link para verificação: {VERIFICATION_URL}")
        message["From"] = FROM_EMAIL
        message['To'] = to_email
        message['Subject'] = subject
        message.add_alternative(html_content, subtype="html")

        try:
            smtp = SMTP (hostname=HOST_EMAIL, port=PORT_EMAIL)
            await smtp.connect()
            await smtp.login(USERNAME_MAIL, PASSWORD_EMAIL)
            await smtp.send_message(message)
            print("E-mail enviado com sucesso")

        except Exception as error:
            print(f"Erro ao enviar e-mail: {error}")
            await self.user_repositoty.delete_user_by_email(to_email)

            raise Exception(error)
            