# we are not using new method of ModelSerializer. We are doing old method using just "serializers" class.

from rest_framework import serializers
from store.models import Product, Collection
from decimal import Decimal


class CollectionSerializer(serializers.ModelSerializer):

    products_count = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Collection
        fields = ['id', 'title', "products_count"]


# ---------------------------------------------------------------------------------------------------------------
# this is the conventional method of writing the serializer class. Specify each and everything just like model.
# class ProductSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     title = serializers.CharField(max_length=255)

    # remember:- if the "field name" is different from the "model field name", then no problem.
    # "field name" can be differently defined in serializer class. For consistency, we keep the same name.
    # To change the field name, just use keyword argument "source" as shown below.
    # price = serializers.DecimalField(max_digits=6, decimal_places=2, source="unit_price")

    # we can have completely different "field names" in API object.
    # Database table fields can be different from API object fields.
    # price_including_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    # to serialize the "relationship field", we should provide queryset argument.
    # "Primarykeyrelatedfield" provides the primary key of the collection.
    # collection = serializers.PrimaryKeyRelatedField(
        # queryset = Collection.objects.all()
    # )


    # "Stringrelatedfield" provides string representation of the collection object.
    # collection = serializers.StringRelatedField()


    # we can directly write a "CollectionSerializer" class so that we get a nested dictionary.
    # collection = CollectionSerializer()


    # we can give hyperlink for the "related field". When we click on the link, it takes us to the object detail page.
    # collection = serializers.HyperlinkedRelatedField(
        # queryset = Collection.objects.all(),
        # view_name="collection-detail"
    # )

    # write a function which returns the value for the "price_including_tax" field.
    # def calculate_tax(self, product: Product):
        # "Decimal" converts float value into decimal value.
        # return product.unit_price * Decimal(1.1)
# --------------------------------------------------------------------------------------------------------------


class ProductSerializer(serializers.ModelSerializer):

    # collection = serializers.HyperlinkedRelatedField(
    #     queryset = Collection.objects.all(),
    #     view_name="collection-detail",
    #     lookup_field='id'
    # )

    # collection = CollectionSerializer()

    # by default, this "collection" field is created using collection_id field.
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source="unit_price")
    price_including_tax = serializers.SerializerMethodField(method_name="calculate_tax")

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)
    

    class Meta:
        model = Product
        fields = ["id", "title", "slug", "description", "price", "inventory", "price_including_tax", "collection"]


    # In case of creating a customized create function, we should over write the "create function" as below.
    # def create(self, validated_data: dict):
    #     product = Product(**validated_data)
    #     product.other = 1
    #     product.save()
    #     return product


    # In case of updating a customized update function, we should over write the "update function" as below.
    # def update(self, instance, validated_data: dict):
    #     instance.unit_price = validated_data.get("unit_price")
    #     instance.save()
    #     return instance
