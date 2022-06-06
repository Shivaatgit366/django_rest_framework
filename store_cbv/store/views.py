from django.db.models.aggregates import Count
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from store.models import Collection, OrderItem, Product, Review
from store.serializers import CollectionSerializer, ProductSerializer, ReviewSerializer
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from store.filters import ProductFilter
from rest_framework.filters import SearchFilter
from rest_framework.filters import OrderingFilter
from store.pagination import DefaultPagination


# --------------------------------------------------------------------------------------------------------------

class ProductListCreate(APIView):
    def get(self, request):
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)
    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductRetrieveUpdateDelete(APIView):
    def get(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)
    def put(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductSerializer(product, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response({"error": "Product can not be deleted because it is associated with order item."}, status=status.status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ---------------------------------------------------------------------------------------------------------------

class CollectionListCreate(APIView):
    def get(self, request):
        queryset = Collection.objects.annotate(products_count=Count('products')).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    def post(self, request):
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CollectionRetrieveUpdateDelete(APIView):
    def get(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)
    def put(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
        serializer = CollectionSerializer(collection, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def delete(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ---------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------
# ---------------------------------------------------------------------------------------------------------------

class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # lookup_field = "id"    --> this step can be used to set the url from "pk" to "id". By default, django searches for "pk" in the url.

    def delete(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        if product.orderitems.count() > 0:
            return Response({"error": "Product can not be deleted because it is associated with order item."}, status=status.status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# --------------------------------------------------------------------------------------------------------------

class CollectionList(generics.ListCreateAPIView):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializer


class CollectionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializer

    def delete(self, request, pk):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=pk)
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# -------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------
# -------------------------------------------------------------------------------------------------------------

# viewsets are used to create all the views in a single class(like list, create, detail, update, delete views).
# "ReadOnlyModelViewSet" is used to create views such as "list view" and "detail view" only. Other views will not come under this class.
# viewset endpoints are written using the "routers".

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


    # to get the "search box" in the query, we can have "search filter by rest_framework".
    # add "SearchFilter" class in the "filter_backends" list.
    # to sort the searched items, we use "OrderingFilter".
    # add "OrderingFilter" class in the "filter_backends" list.


    # we are filtering the queryset using third party library called "django_filters".
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # we should specify which fields we want to filter.
    filterset_class = ProductFilter
    
    # to search and order the search items, we should add the fields as below.
    search_fields = ["title", "description"]
    ordering_fields = ["unit_price", "last_update"]

    # import "PageNumberPagination" from rest_framework. Set the pagination class for this "products" model/table.
    # to have pagination for all the tables/models, we should add the "PageNumberPagination" in settings.py file.
    pagination_class = DefaultPagination


    ###########################################################################################################
    # queryset = Product.objects.all()    --> this queryset should be customized in the case of other customized queries.

    # to have customized queries, we should overwrite the "get_queryset" function.
    # def get_queryset(self):
        # queryset = Product.objects.all()
        # collection_id = self.request.query_params.get("collection_id")  # .get function returns "None" if there is no value for the key.
        # self.request.query_params["collection_id"]  --> we should not use it since it does not return "None" if there is no value for the key.
        # if collection_id is not None:
            # queryset = queryset.filter(collection_id=collection_id)
        # return queryset
    ###########################################################################################################


    # since we use "viewset" class, we should customize the "destroy" function.
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs["pk"]).count() > 0:
            return Response({"error": "Product can not be deleted because it is associated with order item."}, status=status.status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

# ----------------------------------------------------------------------------------------------------------------

class CollectionViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count("products")).all()
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        collection = get_object_or_404(Collection.objects.annotate(products_count=Count('products')), pk=kwargs["pk"])
        if collection.products.count() > 0:
            return Response({'error': 'Collection cannot be deleted because it includes one or more products.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# ----------------------------------------------------------------------------------------------------------------

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    # queryset = Review.objects.all()    --> we should not use this queryset because customization is required.

    # to get the customized query, we should overwrite the "get_queryset" function.
    # if we don't overwrite the "get_queryset" function, we get all the product objects for any query.
    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_pk"])
