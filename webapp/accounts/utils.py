import os
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from webapp import settings
import hashlib
import secrets

def send_html_mail(
    template_name,
    context,
    subject,
    to_mail,
    pdf_full_path=None,
    pdf_list=None,
    remove_pdf=True,
):
    """
    Using this function we can send a html email to given email address, It also has optional way to attach an pdf file. By default the pdf file will be deleted after sending mail, we can override this step.

    """
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)
    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=to_mail,
    )
    email.attach_alternative(html_content, "text/html")

    if pdf_full_path:
        email.attach_file(pdf_full_path)
    if isinstance(pdf_list, list):
        for pdf in pdf_list:
            email.attach_file(pdf)

    email.send()

    if pdf_full_path and remove_pdf:
        os.remove(pdf_full_path)
        

def random_hashkey():
    random_bytes = secrets.token_bytes(20)
    random_hex = random_bytes.hex()
    hash_key = hashlib.sha1(random_hex.encode()).hexdigest()
    return hash_key