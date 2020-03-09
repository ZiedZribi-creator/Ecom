from django.db import models
# from django.contrib.contenttypes.models import ContentType
#
# ClientProduct_type = ContentType.objects.get(app_label='Product', model='clientproduct')
# ClientProduct = ClientProduct_type.model_class()

from django.contrib.auth import get_user_model
User = get_user_model()

class WhishListManager(models.Model):

    def add_product(self,**kwargs):
        product_id = kwargs['product_id']
        ClientProduct = kwargs['clientproduct_klass']
        product_obj = Product.objects.get(id=product_id)
        ClientProduct.objects.create(whishlist=self,product=product_obj)

    def switch_product_to_cart(self,**kwargs):
        client_product_id = kwargs['client_product_id']
        client_product_obj = self.clientproduct_set.get(id=client_product_id)
        client_product_obj.whishlist = None
        client_product_obj.cart = self
        client_product_obj.save()

    def drop_product(self,**kwargs):
        client_product_id = kwargs['client_product_id']
        client_product_obj = self.clientproduct_set.get(id=client_product_id)
        client_product_obj.delete()

class WhishList(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)

    objects = WhishListManager()
    def __str__(self):
        return self.user.username
