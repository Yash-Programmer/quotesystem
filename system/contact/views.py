from django.shortcuts import render
from .models import *

# Create your views here.
def sent(request):
    firstname = request.GET.get("firstName", '')
    lastname = request.GET.get("lastName", '')
    email = request.GET.get("email", '')
    phone = request.GET.get("lastName", '')
    message = request.GET.get("message", '')
    
    instance = Message(firstname=firstname, lastname=lastname, email=email, phone=phone, message=message)
    instance.save()
    
    return render(request, 'sent.html')

def contact(request):
    return render(request, 'contact.html')