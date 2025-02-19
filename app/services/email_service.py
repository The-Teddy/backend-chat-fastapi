from aiosmtplib import SMTP
from os import getenv, path
from jinja2 import Environment, FileSystemLoader
from app.repositories import UserRepository
from app.utils import set_message_to_email

class EmailService:
    
    def __init__(self,):
        from app.repositories import TokenRepository

        self.user_repositoty    = UserRepository()
        self.token_repository   = TokenRepository()
        self.from_email         = getenv("FROM_EMAIL")
        self.host_email         = getenv('HOST_EMAIL')
        self.port_email         = getenv('PORT_EMAIL')
        self.username_mail      = getenv("USERNAME_MAIL")
        self.password_mail      = getenv("PASSWORD_MAIL") 
        self.verification_url   = getenv('VERIFICATION_URL')
        self.base_dir           = path.dirname(path.abspath(__file__))
        self.templates_dir      = path.join(self.base_dir, "../templates")

    async def send_email(self, typeEmail: str, subject: str, to_email: str, user_name: str, token: str, update: bool):

        

        try:

            VERIFICATION_URL    = self.verification_url + token
            env                 = Environment(loader=FileSystemLoader(self.templates_dir))
            template            = env.get_template("verification_email.html") 
            html_content        = template.render(typeEmail=typeEmail,name=user_name, verification_url=VERIFICATION_URL, app_name="Chat Web")
            message             = set_message_to_email(self.from_email, to_email, subject, html_content, VERIFICATION_URL)
            smtp                = SMTP (hostname=self.host_email, port=self.port_email)

            await smtp.connect()
            await smtp.login(self.username_mail, self.password_mail)
            await smtp.send_message(message)

            print("E-mail enviado com sucesso")

        except Exception as error:
            print(f"Erro ao enviar e-mail: {error}")

            if not update:
                await self.user_repositoty.delete_user_by_email(to_email)
                await self.token_repository.delete_one_by_email(to_email)

            raise Exception(error)
            