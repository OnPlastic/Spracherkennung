from __future__ import annotations

import logging
from dataclasses import dataclass
import smtplib
from email.message import EmailMessage


log = logging.getLogger(__name__)


@dataclass(frozen=True)
class SmtpSettings:
    host: str
    port: int
    use_ssl: bool
    user: str
    app_password: str
    from_name: str


def send_mail_text(
    *,
    smtp: SmtpSettings,
    to_addr: str,
    subject: str,
    text_content: str,
) -> None:

    msg = EmailMessage()
    msg["From"] = f"{smtp.from_name} <{smtp.user}>"
    msg["To"] = to_addr
    msg["Subject"] = subject

    body = f"""Erfasster Text:
---
{text_content}
---
"""
    msg.set_content(body)

    log.info("Sending mail to=%s subject=%s", to_addr, subject)
             
    if smtp.use_ssl:
        with smtplib.SMTP_SSL(smtp.host, smtp.port) as server:
            server.login(smtp.user, smtp.app_password)
            server.send_message(msg)
    else:
        with smtplib.SMTP(smtp.host, smtp.port) as server:
            server.starttls()
            server.login(smtp.user, smtp.app_password)
            server.send_message(msg)

    log.info("Mail sent to %s", to_addr)
