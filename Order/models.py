from django.db import models
from Cart.models import Cart
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
User = get_user_model()

# Create your models here.


class GuestUserForm(models.Model):
    name = models.CharField(max_length=255)
    email   = models.EmailField()
    address = models.CharField(max_length=255)
    phone   = models.CharField(max_length=20)
    def __str__(self):
        return 'email : {email} / address : {address} / phone : {phone}'

# COD OR PAYME
# class OrderManger(models.Manager):
#     def attach_shipping_info(self,**kwargs):
#         shipping_info = kwargs['shipping_info']
#         shipping_info_obj = ShippingInfo.objects.create(**shipping_info)
#         self.shipping_info = shipping_info_obj
#         self.save()
#     def add_event(self,**kwargs):
#         order_history_obj = OrderHistory.objects.get(event=kwargs['eve,t'])
#         self.history.add(order_history_obj)
#         self.save()

class Order(models.Model):
    # PAYMENT_TYPE_CHOICES = (
    # ('cod','COD'),
    # ('payme','Payme')
    # )
    ORDER_MODE_CHOICES = (
    ('runing','Runing'),
    ('shipped','Shipped')
    )
    cart          = models.OneToOneField(Cart,on_delete=models.CASCADE,blank=True,null=True)
    guestuserform = models.ForeignKey(GuestUserForm,on_delete=models.CASCADE,blank=True,null=True)
    created_on = models.DateTimeField(auto_now_add=True,blank=True,null=True)
    status     = models.CharField(max_length=50,choices=ORDER_MODE_CHOICES,default='Runing')
    # history       = models.ManyToManyField('OrderHistory')

    # objects       = OrderManger()
#
# class OrderHistory(models.Model):
#     EVENTS = (
#        ('ordered','Just Ordered'), # order created
#        ('payed payme','Payed with payme'), # client payed on the intered => order.payed == True
#        ('payed cod','Payed with cod'), # client payed on delivery => order.model == shipped
#     )
#
#     event = models.CharField(max_length=50,choices=EVENTS)
#
#     def __str__(self):
#         return '{event} on the {time}'.format(event=self.event,time=self.time)


@receiver(post_save, sender=Order)
def calculate_cart_total(sender, instance, created, **kwargs):
    if created :
        qs = instance.cart.products.all()
        total = 0
        for cp in qs :
            total += cp.qty * cp.product.price
        cart_obj = instance.cart
        cart_obj.total = total
        cart_obj.save()
