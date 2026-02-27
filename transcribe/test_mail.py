import os
from transcribe_cli.mailer import SmtpSettings, send_mail_text

smtp = SmtpSettings(
    host="smtp.gmail.com",
    port=465,
    use_ssl=True,
    user=os.environ["SMTP_USER"],
    app_password=os.environ["SMTP_APP_PASSWORD"],
    from_name="Spracherkennung CLI",
)

send_mail_text(
    smtp=smtp,
    to_addr=os.environ["SMTP_USER"],
    subject="[Transkript] Test",
    text_content="Hallo Welt – das ist ein Test.",
)

print("mail ok")
