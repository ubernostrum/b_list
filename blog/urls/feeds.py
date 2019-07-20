from django.urls import path

from blog.feeds import CategoryFeed, EntriesFeed


app_name = 'blog'


urlpatterns = [
    path('entries/',
        EntriesFeed(),
        name='entries'),
    path('categories/<slug:slug>/',
        CategoryFeed(),
        name='category'),
]
