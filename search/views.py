from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home_page(request):

    search_query = request.GET.get("input")

    print(search_query)

    return render(request,'home.html')

def index_url(request):
    return render(request,'index_url.html')

def known_urls(request):
    return render(request,'known_urls.html')