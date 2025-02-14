from django.shortcuts import render

def index(request):
    context_dict = {'boldmessage': "Welcome to Rango!"}
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    # Add your name or any additional context if desired
    context_dict = {'yourname': 'Yiming'}  # Replace 'Your Name' with your actual name
    return render(request, 'rango/about.html', context=context_dict)
