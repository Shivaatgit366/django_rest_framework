from store.signals import order_created
from django.dispatch import receiver


@receiver(order_created)
# this is the receiver or the handler function. It takes action when the order object gets created.
def on_order_created(sender, **kwargs):
    # keyword argument "order" is created when the signal is fired.
    # print the newly created order object.
    print(kwargs["order_object"])    # Order object (18)
