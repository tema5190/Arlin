from django.http import HttpResponse
from django.shortcuts import render
from crawler import Crawler
from thread import start_new_thread
from indexer import Indexer

# Create your views here.
def home_page(request):

    context = {}
    search_query = request.GET.get("input")

    if not search_query == None:
        indexer = Indexer()
        print(indexer.search_query_result(search_query))
        context['urls'] = indexer.search_query_result(search_query)

    return render(request,'home.html', context)

def index_url(request):
    context = {}

    #try:
    if(request.method=='GET'):
        data = request.GET

        if data.items():
            url = data.get('url')
            width = int(data.get('width'))
            depth = int(data.get('depth'))

            # print(width)
            # print(depth)
            # print(url)

            start_new_thread(Crawler().run, (url, width, depth,))

    #except Exception as e:
    #    print(e.message)



    #crawler.run(url,width,depth)

    return render(request,'index_url.html', context)

def known_urls(request):
    return render(request,'known_urls.html')
