from django.shortcuts import render, HttpResponse

# Create your views here.
def home(index):
    return HttpResponse('This is home')

def blog(index):
    return HttpResponse('This is blog')