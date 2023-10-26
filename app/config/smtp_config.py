import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

class smtp_config:
    load_dotenv()
    
    def __init__(self):
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.smtp_user = os.getenv("USER_GMAIL")
        self.smtp_password = os.getenv("PASSWORD_GMAIL")

    def send_user(self, user_mail,token):
        url_service = os.getenv("URL_SERVICE_WEB")
        smtp = smtplib.SMTP(self.smtp_server, self.smtp_port)
        smtp.starttls()
        smtp.login(self.smtp_user, self.smtp_password)

        mensaje = MIMEMultipart()
        mensaje['From'] = self.smtp_user
        mensaje['To'] = user_mail
        mensaje['Subject'] = "Bienvenido es hora de tu registro"
        content_html = f"""
<html>
<head>
<title>Activación de Cuenta</title>
<style>
/* Estilos para el cuerpo del correo */
body {{
    font-family: Arial, sans-serif;
    background-color: #f0f0f0;
    margin: 0;
    padding: 0;
}}

/* Contenedor principal */
.container {{
    width: 100%;
    max-width: 600px;
    margin: 0 auto;
    background-color: #ffffff;
    padding: 20px;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}}

/* Encabezado */
.header {{
    text-align: center;
    padding: 20px 0;
}}

/* Título */
.title {{
    font-size: 24px;
    color: #333;
}}

/* Enlace de activación */
.activation-link {{
    display: block;
    text-align: center;
    margin-top: 20px;
}}

/* Estilos para el botón */
.activation-button {{
    display: inline-block;
    background-color: #007BFF;
    color: #fff;
    padding: 10px 20px;
    text-decoration: none;
    border-radius: 5px;
}}

/* Pie de página */
.footer {{
    text-align: center;
    padding: 20px 0;
    color: #777;
}}
</style>
</head>
<body>
<div class="container">
    <div class="header">
        <h1 class="title">Activación de Cuenta</h1>
    </div>
    <p>Hola,</p>
    <p>¡Gracias por registrarte! Para activar tu cuenta, por favor haz clic en el enlace de abajo:</p>
    <a class="activation-link" href="http://{url_service}/api/v1/check-email/{token}">Activar Cuenta</a>
    <div class="footer">
        <p>Atentamente,</p>
        <p>Tu Equipo de Soporte de Saturnina</p>
    </div>
</div>
</body>
</html>
"""

        
        mensaje.attach(MIMEText(content_html, 'html'))

        smtp.sendmail(self.smtp_user, user_mail, mensaje.as_string())
        smtp.quit()
    
