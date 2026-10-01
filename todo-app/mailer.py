import os
import smtplib
from email.message import EmailMessage

def send_reset_email(to_email, link):
    host = os.getenv("SMTP_HOST")
    if not host:
        # no SMTP configured: print the link so you can still test locally
        print(f"[DEV] Password reset link for {to_email}: {link}")
        return

    msg = EmailMessage()
    msg["Subject"] = "Reset your password"
    msg["From"] = os.getenv("SMTP_USER")
    msg["To"] = to_email
    msg.set_content(
        f"Use this link to reset your password (valid for 30 minutes):\n\n{link}\n\n"
        "If you didn't ask for this, ignore this email."
    )

    try:
        port = int(os.getenv("SMTP_PORT", 587))
        print(f"[MAIL] Connecting to {host}:{port}")
        with smtplib.SMTP(host, port, timeout=15) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            s.login(os.getenv("SMTP_USER"), os.getenv("SMTP_PASSWORD"))
            s.send_message(msg)
        print(f"[MAIL] Sent reset email to {to_email}")
    except Exception as e:
        print(f"[MAIL ERROR] {type(e).__name__}: {e}")
        print(f"[DEV] Reset link for {to_email}: {link}")