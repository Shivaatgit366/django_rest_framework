from django.urls import path
from store import views


app_name = "store"


# URLConf
urlpatterns = [
    path("products/", views.product_list_or_create),
    path("products/<int:id>/", views.product_detail_update_delete),
    path("collections/", views.collection_list_or_create),
    path("collections/<int:pk>/", views.collection_detail_update_delete)
]
