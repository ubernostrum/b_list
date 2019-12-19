from django.urls import include, path

from blog import views


app_name = "blog"


urlpatterns = [
    path("", views.EntryArchiveIndex.as_view(), name="index"),
    path("<int:year>/", views.EntryArchiveYear.as_view(), name="year"),
    path("<int:year>/<str:month>/", views.EntryArchiveMonth.as_view(), name="month"),
    path(
        "<int:year>/<str:month>/<int:day>/", views.EntryArchiveDay.as_view(), name="day"
    ),
    path(
        "<int:year>/<str:month>/<int:day>/<slug:slug>/",
        views.EntryDetail.as_view(),
        name="entry",
    ),
]
