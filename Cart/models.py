from django.db import models
from Product.models  import ClientProduct
# from django.contrib.contenttypes.models import ContentType
#
# ClientProduct_type = ContentType.objects.get(app_label='Product', model='clientproduct')
# ClientProduct = ClientProduct_type.model_class()

# Create your models here.

from django.contrib.auth import get_user_model
User = get_user_model()


class CartManager(models.Manager):

    def add_product(self,**kwargs):
        client_product_id = kwargs['client_product_id']
        qs = self.clientproduct.filter(id=client_product_id)
        if qs :
            #increase the qty by one
            client_product_obj.nb += 1
            client_product_obj.save()
        else :
            ClientProduct = kwargs['clientproduct_klass']
            # create new client_product
            client_product_obj = ClientProduct.objects.create(product=product_obj)
            self.products.add(client_product_obj)
            self.save()

    def set_product_qty(self,**kwargs):
        client_product_id = kwargs['client_product_id']
        client_product_obj = self.products.get(id=client_product_id)
        client_product_obj.nb = kwargs['qty']
        client_product_obj.save()

    def drop_product(self,**kwargs):
        client_product_id = kwargs['client_product_id']
        client_product_obj = self.products.get(id=client_product_id)
        self.products.remove(client_product_obj)
        self.save()


class Cart(models.Model):
    user     = models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    products   = models.ManyToManyField(ClientProduct)
    total    = models.DecimalField(max_digits=20,decimal_places=3,blank=True,null=True)

    objects  = CartManager()
    def __str__(self):
        return 'cart for {username}'.format(username=self.user.username)
