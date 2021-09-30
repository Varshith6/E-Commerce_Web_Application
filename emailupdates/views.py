from django.contrib import messages
from django.shortcuts import render
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.conf import settings
from .models import Emailupdate
from .forms import SubscribeForm

def email_subscribe(request):
    form = SubscribeForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if Emailupdate.objects.filter(Email = instance.Email).exists():
            messages.warning(request,
                             'Your Email has already been subscribed',
                             'alert alert-warning alert-dismissible')
        else:
            instance.save()
            messages.success(request,
                             'Thank You! You have subscribed and will recieve update about our products and offers',
                             'alert alert-success alert-dismissible')
            subject = 'Thank you for subscribing to our website'
            from_email = 'Saree House <admin@sareehouseonline.com>'
            to_email = [instance.Email]
            with open(settings.BASE_DIR + '/templates/emailupdates/subscription_mail.txt') as f:
                signup_message = f.read()
            message = EmailMultiAlternatives(subject=subject, body=signup_message, from_email= from_email, to=to_email)
            html_template = get_template('emailupdates/subscription_mail.html').render()
            message.attach_alternative(html_template, 'text/html')
            message.send()


    context= {
        'form': form,
    }

    template = "emailupdates/email_subscribe.html"
    return render(request, template, context)

def email_unsubscribe(request):
    form = SubscribeForm(request.POST or None)

    if form.is_valid():
        instance = form.save(commit=False)
        if Emailupdate.objects.filter(Email = instance.Email).exists():
            Emailupdate.objects.filter(Email = instance.Email).delete()
            messages.success(request,
                             'You have unsubscribed and will not receive further updates',
                             'alert alert-success alert-dismissible')
            subject = 'Unsubscribing from SareeHouse'
            from_email = 'Saree House <admin@sareehouseonline.com>'
            to_email = [instance.Email]
            with open(settings.BASE_DIR + '/templates/emailupdates/unsubscription_mail.txt') as f:
                signup_message = f.read()
            message = EmailMultiAlternatives(subject=subject, body=signup_message, from_email=from_email, to=to_email)
            html_template = get_template('emailupdates/unsubscription_mail.html').render()
            message.attach_alternative(html_template, 'text/html')
            message.send()
        else:
            messages.warning(request,
                             'Your email was not subscribed for our updates',
                             'alert alert-warning alert-dismissible')

    template = "emailupdates/email_unsubscribe.html"

    context = {
        'form': form,
    }
    return render(request, template, context)

def voila(request):
    return render(request,'email_subscribe.html')



