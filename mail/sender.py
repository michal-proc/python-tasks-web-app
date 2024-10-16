from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode


def send_activation_email(request, user):
    current_site = get_current_site(request)

    subject = 'Activate Your Account'
    message = 'Please follow the link to activate your account: ...'
    html_message = render_to_string('mail/registration.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    from_email = 'system@example.org'

    print(send_mail(subject, message, from_email, [user.email], html_message=html_message, fail_silently=False))
