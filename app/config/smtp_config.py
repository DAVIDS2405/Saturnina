import socket
from fastapi import HTTPException, status
from fastapi.templating import Jinja2Templates
from jinja2.exceptions import TemplateNotFound
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config.envs import settings
from logger.logger import logger
from datetime import datetime
import smtplib


templates = Jinja2Templates(directory="app/templates")


def send_email(name, token):

    smtp_server = settings.EMAIL_HOST
    smtp_port = int(settings.EMAIL_HOST_PORT)
    smtp_username = settings.EMAIL_HOST_USER
    smtp_password = settings.EMAIL_HOST_PASSWORD

    msg = MIMEMultipart()
    msg['From'] = "Acme <onboarding@resend.dev>"
    msg['To'] = "delivered@resend.dev"
    msg['Subject'] = "¡Bienvenido completa tu registro!"

    try:
        template = templates.get_template("email-send.html")

        html_content = template.render(
            name=name, year=datetime.year, token=token)

        msg.attach(MIMEText(html_content, 'html'))

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
            server.close()
            logger.info('Send Mail ok')

        return HTTPException(
            status_code=status.HTTP_201_CREATED, detail="Check you email to confirm your acount")

    except socket.timeout as error:
        logger.error(f"Connection timed out: {error}")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="The connection to the email server timed out. Please try again later."
        )
    except TemplateNotFound as error:
        logger.error(f"Template not found: {error}")
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail=f"The template {error.message} not found"
        )

    except Exception as e:
        logger.info(f'Send mail error{e}')
        return HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="SMTP have a error")


def send_email_reset_password(name, id):

    smtp_server = settings.EMAIL_HOST
    smtp_port = int(settings.EMAIL_PORT)
    smtp_username = settings.EMAIL_HOST_USER
    smtp_password = settings.EMAIL_HOST_PASSWORD

    msg = MIMEMultipart()
    msg['From'] = "Acme <onboarding@resend.dev>"
    msg['To'] = "delivered@resend.dev"
    msg['Subject'] = "Recupera tu contraseña"

    template = templates.get_template("recover-password.html")

    html_content = template.render(name=name, year=datetime.year, id=id)

    msg.attach(MIMEText(html_content, 'html'))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
            server.close()
            logger.info('Send Mail ok')
        raise HTTPException(
            status_code=status.HTTP_201_CREATED, detail="Check you email to change your password")
    except Exception as e:
        logger.info(f'Send mail error{e}')
