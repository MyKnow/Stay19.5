from django.shortcuts import render

# Create your views here.
def main(request):
    return render(request, 'common/main.html')

def login(request):
    return render(request, 'common/login.html')

def info(request):
    return render(request, 'common/info.html')