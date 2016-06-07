from django.conf.urls import url
from django.contrib import admin
import search.views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^indexing_view/', search.views.index_url),
    url(r'^known_urls_view/', search.views.known_urls),
    #url(r'^results_view/', search.views.results),
    url(r'^home_view/',search.views.home_page),
    url(r'^$', search.views.home_page)

]
