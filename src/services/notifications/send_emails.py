import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.config import settings

# Настройки почты
sender_email = settings.SMTP_USER  # Ваша почта
sender_password = settings.SMTP_PASS  # Пароль приложения


def send_email(to, subject, body):
    msg = MIMEMultipart()

    msg["From"] = settings.MAIL_FROM
    msg["To"] = to
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))
    try:
        # Безопасное подключение через SSL
        server = smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT)
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

    except Exception as e:
        print(f"Ошибка: {e}")
