import yagmail

def send_email_with_pdf(recipient_email, subject, body_text, pdf_data, filename, sender_email, sender_password):
    try:
        yag = yagmail.SMTP(sender_email, sender_password)
        yag.send(
            to=recipient_email,
            subject=subject,
            contents=body_text,
            attachments=[filename]
        )
        return True, "Email sent successfully!"
    except Exception as e:
        return False, str(e)
