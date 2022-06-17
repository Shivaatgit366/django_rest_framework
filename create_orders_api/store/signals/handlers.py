# signals means notifications.
# it is to make sure that when the user object is created, new customer also gets created.

from django.conf import settings
from ..models import Customer
from django.dispatch import receiver
from django.db.models.signals import post_save

# below "signal handler" function creates a new "customer" object when the new "user" object is created.
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_customer_for_new_user(sender, **kwargs):
    # sender means the object which sends the notification. It is "user" object in this case.
    # In **kwargs, there is a key called "created" which has boolean value "True/False" in its value.
    # In **kwargs, we have a key called "instance" which gives the "created instance/object" as its value.
    if kwargs["created"]:
        Customer.objects.create(user=kwargs["instance"])
