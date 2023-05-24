from django.shortcuts import render

# Create your views here.
def gallery(request):
    return render(request, 'gallery/gallery.html')

def photo(request):
    return render(request, 'gallery/photo.html')

def ai_gallery(request):
    return render(request, 'gallery/ai_gallery.html')