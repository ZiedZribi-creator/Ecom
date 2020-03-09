from django.contrib import admin
from .models import ProductVariant,Image,Product,ClientProduct,Section,Categorie,SubCategorie
class ImageAdmin(admin.ModelAdmin):
    list_display = ('image','primary',)
    fields = [
         'image',
         'primary',
    ]
admin.site.register(Product)
admin.site.register(ClientProduct)
admin.site.register(Section)
admin.site.register(Categorie)
admin.site.register(SubCategorie)
admin.site.register(Image,ImageAdmin)
admin.site.register(ProductVariant)
