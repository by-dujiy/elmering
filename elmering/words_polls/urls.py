from django.urls import path
from .import views


app_name = "words_polls"
urlpatterns: list = [
    path("",
         views.CollectionListView.as_view(),
         name="index"),
    path("collection/<int:id>",
         views.CollectionDetailView.as_view(),
         name="detail"),
    path("collection/<int:pk>/edit",
         views.CollectionEditView.as_view(),
         name="edit-collection"),
    path("collection-create/",
         views.CollectionCreateView.as_view(),
         name="create-collection"),
    path("collection/<int:pk>/delete",
         views.CollectionDeleteView.as_view(),
         name="delete-collection"),
]
