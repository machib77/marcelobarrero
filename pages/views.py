from django.contrib import messages
from django.shortcuts import render
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.core.mail import send_mail
from .forms import ContactForm


# Create your views here.
class HomePageView(TemplateView):
    template_name = "pages/home.html"


class AboutPageView(TemplateView):
    template_name = "pages/about.html"


class PortfolioPageView(TemplateView):
    template_name = "pages/portfolio.html"


class ContactView(FormView):
    template_name = "pages/contact.html"
    form_class = ContactForm
    success_url = reverse_lazy("home")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        subject = form.cleaned_data["subject"]
        message = form.cleaned_data["message"]

        # Modify the message to include email as the first line
        formatted_subject = f"MARCELOBARRERO.COM Subject: {subject}"
        formatted_message = f"From: {email}\n\n{message}"

        send_mail(
            formatted_subject,
            formatted_message,
            "marcelobarreroc@gmail.com",
            ["marcelo.barrero@proton.me"],
            fail_silently=False,
        )

        # Save to database
        form.save()

        # Success Message
        messages.success(
            self.request, "Your message has been sent!", extra_tags="success-fadeout"
        )

        return super().form_valid(form)


class RobotsTxtView(TemplateView):
    template_name = "robots.txt"
