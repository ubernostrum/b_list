from django.urls import include, path

from blog import views


app_name = "blog"


urlpatterns = [
    path("", views.CategoryList.as_view(), name="index"),
    path("<slug:slug>/", views.CategoryDetail.as_view(), name="category"),
]
