from rest_framework import status
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from store import serializers
from store.serializers import ProductSerializer, CollectionSerializer
from store.models import Product, Collection
from django.db.models import Count


# Create your views here.


# ---------------------------------------------------------------------------------------------------------------

@api_view(["GET", "POST"])
def product_list_or_create(request):
    if request.method == "GET":
        # we take the queryset and convert them into the serializer. We should mention "many=True".
        queryset = Product.objects.select_related("collection").all()
        serializer = ProductSerializer(queryset, many=True, context={"request": request})
        return Response(serializer.data)

    elif request.method == "POST":
        # for the "POST" request, this class works in the reverse way. This serializer classes "deserializes" the request object.
        serializer = ProductSerializer(data=request.data)

        # old style of validating the object.
        # if serializer.is_valid():
            # return Response("ok")
        # else:
            # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # new style of validating the object.
        serializer.is_valid(raise_exception=True)
        # print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def product_detail_update_delete(request, id):
    # old style of writing, here we use the try catch method.
    # try:
    #     product = Product.objects.get(pk=id)
    #     serializer = ProductSerializer(product)
    #     return Response(serializer.data)
    # except Product.DoesNotExist:
        # response status no.404 is for "object not found". We should mention it.
        # return Response(status=status.HTTP_404_NOT_FOUND)
    

    # Here we use django shortcut method for getting the object.
    product = get_object_or_404(Product, pk=id)

    if request.method == "GET":
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    elif request.method == "PUT":
        updated_product = ProductSerializer(product, request.data)
        updated_product.is_valid(raise_exception=True)
        updated_product.save()
        return Response(updated_product.data, status=status.HTTP_202_ACCEPTED)

    elif request.method == "DELETE":
        if product.orderitems.count() > 0:
            return Response({"error message": "product can not be deleted because it is associated with an order item"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# --------------------------------------------------------------------------------------------------------------


@api_view(["GET", "POST"])
def collection_list_or_create(request):

    if request.method == "GET":
        queryset = Collection.objects.annotate(products_count=Count("products")).all()
        serializer = CollectionSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CollectionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET", "PUT", "DELETE"])
def collection_detail_update_delete(request, pk):
    collection = get_object_or_404(Collection.objects.annotate(products_count=Count("products")).all(),
                                    pk=pk)

    if request.method == "GET":
        serializer = CollectionSerializer(collection)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = CollectionSerializer(collection, request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    elif request.method == "DELETE":
        if collection.products.count() > 0:
            return Response({"error": "collection can not be deleted because one or more product is associated with it"},
                            status=status.HTTP_405_METHOD_NOT_ALLOWED)
        collection.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# --------------------------------------------------------------------------------------------------------------
