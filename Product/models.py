from django.db import models
from Whishlist.models import WhishList
# from Cart.models import Cart
from .utils import unique_slug_generator
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
# Create your models here.



class Section(models.Model):
    name = models.CharField(max_length=255)
    categorie = models.ManyToManyField('Categorie')
    def __str__(self):
        return self.name

class Categorie(models.Model):
    name = models.CharField(max_length=255)
    subcategorie = models.ManyToManyField('SubCategorie')
    def __str__(self):
        return self.name

class SubCategorie(models.Model):
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name



class Size(models.Model):
    nb = models.IntegerField()
    def __str__(self):
        return "{title} => size : {nb} DT".format(title=self.product.title,
                                              price = self.price)

class Color(models.Model):
    code = models.CharField(max_length=255)
    def __str__(self):
        return "{title} => color : {code} DT".format(title = self.product.title,
                                                     price = self.code)

class Image(models.Model):
    image = models.ImageField()
    primary = models.BooleanField(default=False)
    # def __str__(self):
    #     return "{title} => img_order {order} DT".format(title = self.product.title,
    #                                                     order = self.order)


class ProductManager(models.Manager):
    def add_size(self,**kwargs):
        nb = kwargs['size_nb']
        size_obj = None
        if nb :
            size_obj = Size.objects.create(nb=nb)
        else :
            size_id = kwargs['size_id']
            size_obj = Size.objects.get(id=size_id)
        self.sizes.add(size_obj)
        self.save()
    def drop_size(self,**kwargs):
        size_id = kwargs['size_id']
        size_obj = self.sizes.get(id=size_id)
        self.sizes.remove(size_obj)
        self.save()

    def add_color(self,**kwargs):
        color_code = kwargs['color_code']
        color_obj = None
        if color_code :
            color_obj = Color.objects.create(code=color_code)
        else :
            clor_id = kwargs['color_id']
            color_obj = Color.objects.get(id=color_id)
        self.colors.add(color_obj)
        self.save()

    def drop_color(self,**kwargs):
        color_id = kwargs['color_id']
        color_obj = self.colors.get(id=color_id)
        self.colors.remove(color_obj)
        self.save()

    def set_subcategorie(self,**kwargs):
        subcategorie_id = kwargs['subcategorie_id']
        self.subcategorie = SubCategorie.objects.get(id=subcategorie_id)
        self.save()

class ProductVariant(models.Model):

    image = models.ForeignKey(Image,on_delete=models.SET_NULL,blank=True,null=True)
    size = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=20, decimal_places=3)
    qty = models.IntegerField(default=0)
    color = models.CharField(max_length=255)

    def __str__(self):
        return "{size} {price} {qty} {color}".format(size=self.size,price=self.price,qty=self.qty,color=self.color)


class Product(models.Model):
    add_imgs        = models.ManyToManyField(Image)
    # primary_img    = models.ImageField(blank=True,null=True)
    slug            = models.SlugField(blank=True,null=True)
    title           = models.CharField(max_length=255)
    description     = models.TextField(blank=True,null=True)
    price           = models.DecimalField(max_digits=20, decimal_places=3,blank=True,null=True)
    section         = models.ForeignKey(Section,on_delete=models.SET_NULL,blank=True,null=True)
    categorie       = models.ForeignKey(Categorie,on_delete=models.SET_NULL,blank=True,null=True)
    subcategorie    = models.ForeignKey(SubCategorie,on_delete=models.SET_NULL,blank=True,null=True)
    product_variants  = models.ManyToManyField(ProductVariant)
    objects        = ProductManager()
    class Meta :
        ordering = ('-id',)
    def __str__(self):
        return "{title} => {price} DT".format(title=self.title,
                                              price = self.price)



class ClientProduct(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True)
    qty = models.IntegerField(default=1)
    def __str__(self):
        return '{title} => nb : {nb}'.format(title=self.product.title,qty=self.qty)


# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created :
#         profile_obj = Profile.objects.create(user=instance)

@receiver(pre_save, sender=Product)
def set_product_slug(sender, instance, **kwargs):
    if not instance.slug :
        instance.slug = unique_slug_generator(instance)
