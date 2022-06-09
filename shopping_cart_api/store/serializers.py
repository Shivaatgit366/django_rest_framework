from decimal import Decimal
from store.models import CartItem, Product, Collection, Review, Cart
from rest_framework import serializers


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'slug', 'inventory', 'unit_price', 'price_with_tax', 'collection']

    price_with_tax = serializers.SerializerMethodField(
        method_name='calculate_tax')

    def calculate_tax(self, product: Product):
        return product.unit_price * Decimal(1.1)

   
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, **validated_data)


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "title", "unit_price"]


class CartItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name="get_total_price")

    def get_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity", "total_price"]


class CartSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True)
    total_price = serializers.SerializerMethodField(method_name="get_total_price")

    def get_total_price(self, cart: Cart):
        return sum([item.quantity * item.product.unit_price  for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ["id", "items", "total_price"]


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    # checking whether the product with the given input "value" exists or not. If the object exists, then keep the value.
    # this is helpful if somebody gives "product_id=0" in the input. There is no product with the id equal to zero.
    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError("No product with the given ID")
        return value

    # this is the in-built save method present in the model serializer. We should customize it.
    # to post the "product_id" and "quantity", we can use "validated_data" dictionary.
    def save(self, **kwargs):
        # "cart_id" which is present in the url, will be taken using context dictionary.
        cart_id = self.context["cart_id"]

        product_id = self.validated_data["product_id"]
        quantity = self.validated_data["quantity"]

        # now, try to grab that object using both the "product_id" and "cart_id".
        # if we don't have any object, then create it.
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity = quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            # new_cart_item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
            # we can create the object using "create" method. Use the "validated_data" dictionary for the input.
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
        
        return self.instance

    class Meta:
        model = CartItem
        fields = ["product_id", "quantity"]


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]
