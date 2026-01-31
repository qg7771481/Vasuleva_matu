from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import render_to_string

from .forms import RegisterForm
from django.core.mail import BadHeaderError, EmailMessage, send_mail
from django.conf import settings


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get('username')
            try:
                send_mail(
                    subject='Welcome to Narniya',
                    message=f"User with {email} created",
                    from_email=None,
                    recipient_list=[settings.ADMIN_EMAIL],
                    html_message=f"User with {email} created",
                )
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            try:
                email_message = EmailMessage(
                    subject=f"{username} Welcome to Narniya with {email}",
                    body=render_to_string(
                        "users/email.html", context={"username": username}
                    ),
                    from_email=None,
                    to=[email],
                    headers={"Reply-To": email},
                    cc=["kopohef433@emaxasp.com"],
                    bcc=["olive8612@airsworld.net"],
                )
                email_message.content_subtype = "html"
                email_message.send(fail_silently=False)
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
    else:
        form = RegisterForm()

    return render(request, "users/register.html", context={"form": form})






