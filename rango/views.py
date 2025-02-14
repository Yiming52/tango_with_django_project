from django.shortcuts import render

def index(request):
    context_dict = {'boldmessage': "Welcome to Rango!"}  
    return render(request, 'rango/index.html', context=context_dict)
