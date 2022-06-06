from django.urls import path, include
from store import views
# from rest_framework.routers import SimpleRouter
# from pprint import pprint
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

# URLConf

router = routers.DefaultRouter()
router.register("products", views.ProductViewSet, basename="products")
router.register("collections", views.CollectionViewSet)

products_router = routers.NestedDefaultRouter(router, "products", lookup="product")
products_router.register("reviews", views.ReviewViewSet, basename="product-reviews")

urlpatterns = router.urls + products_router.urls

# router.register("collections", views.CollectionViewSet)
# pprint(router.urls)

# urlpatterns = router.urls

# urlpatterns = [
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:pk>/', views.ProductDetail.as_view()),
#     path('collections/', views.CollectionList.as_view()),
#     path('collections/<int:pk>/', views.CollectionDetail.as_view()),
# ]
