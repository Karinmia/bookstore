import os
import uuid
from secrets import token_urlsafe

from django.core.mail import EmailMessage
from django.template.loader import get_template


def generate_token(length=16):
    return token_urlsafe(length)


def get_file_path(instance, filename):
    """
    Rename images
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join(instance.__class__.__name__.lower(), filename)


def send_email(subject, user, template, content, from_email, attachments=[]):
    if type(user) is list:
        to = user
    else:
        to = [user]
    ctx = {
        'content': content,
    }
    message = get_template(template).render(ctx)
    msg = EmailMessage(subject, message, from_email=from_email, bcc=to)
    for index, attachment in enumerate(attachments):
        attachment_name = "attachment-{}.{}".format(index, attachment['content_type'])
        msg.attach(attachment_name, attachment['file'])
    msg.content_subtype = 'html'
    msg.send()
