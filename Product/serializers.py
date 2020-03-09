from rest_framework import serializers
from .models import (Product,Image,Color,Size,
                    Section,Categorie,SubCategorie,
                    ClientProduct,ProductVariant)



class SubCategorieSerializer(serializers.ModelSerializer):
    class Meta :
        model = SubCategorie
        fields = ('id','name')

class CategorieSerializer(serializers.ModelSerializer):
    subcategories = serializers.SerializerMethodField()
    class Meta :
        model = Categorie
        fields = ('id','name','subcategories')

    def get_subcategories(self,cat_obj):
        sub_cat_qs = cat_obj.subcategorie.all()
        serializer = SubCategorieSerializer(sub_cat_qs,many=True)
        return serializer.data

class SectionSerializer(serializers.ModelSerializer):
   categories = serializers.SerializerMethodField(read_only=True)
   count = serializers.SerializerMethodField(read_only=True)
   class Meta :
       model = Section
       fields = ('id','name','categories','count')
   def get_count(self,sec_obj):
       return len(sec_obj.product_set.all())

   def get_categories(self,section_obj):
       cat_qs = section_obj.categorie.all()
       if cat_qs :
           serializer = CategorieSerializer(cat_qs,many=True)
           return serializer.data
       return []


class ImageSerializer(serializers.ModelSerializer):
    img_url = serializers.CharField(source='image.url',read_only=True)
    img_file = serializers.CharField(source='image.url',read_only=True)
    image = serializers.ImageField(write_only=True)
    class Meta :
        model = Image
        fields = ('id','image','img_url','img_file','primary')


class ClientProductSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    class Meta :
        model = ClientProduct
        fields = ('id','product','qty',)
    def get_product(self,clientproduct_obj):
        product_obj = clientproduct_obj.product
        serializer  = ProductSerializer(product_obj)
        return serializer.data

class ProductVariantSerializer(serializers.ModelSerializer):
    img = serializers.SerializerMethodField()
    class Meta :
        model = ProductVariant
        fields = ('id','img','size','price','qty','color')
    def get_img(self,pv_obj):
        if pv_obj.image :
            ser = ImageSerializer(pv_obj.image,many=False)
            return ser.data
        return None
# class ProductDataField(serializers.Field):
#     # def to_representation(self,instance):
#     #     # instance to data
#     #     print(instance)
#     #     return value
#     def to_internal_value(self,value):
#         # value to instance
#         print(value)
#         return value


class ProductSerializer(serializers.ModelSerializer):
    add_imgs = serializers.SerializerMethodField(read_only=True)
    product_variants = serializers.SerializerMethodField(read_only=True)
    section = serializers.SerializerMethodField(read_only=True)
    categorie = serializers.SerializerMethodField(read_only=True)
    subcategorie = serializers.SerializerMethodField(read_only=True)
    primary_img = serializers.SerializerMethodField(read_only=True)

    class Meta :
        model = Product
        fields = ('title','description','slug','price',
                  'primary_img',
                  'add_imgs',
                  'product_variants',
                  'section',
                  'categorie',
                  'subcategorie',

                  )
    def get_product_variants(self,product_obj):
        qs = product_obj.product_variants.all()
        serializer = ProductVariantSerializer(qs,many=True)
        return serializer.data

    def get_add_imgs(self,product_obj):
        qs = product_obj.add_imgs.all()
        serializer = ImageSerializer(qs,may=True)
        return serializer.data

    def get_primary_img(self,product_obj):
        img_obj = product_obj.add_imgs.all().filter(primary=True)
        if img_obj :
            serializer = ImageSerializer(img_obj[0],many=False)
            return serializer.data
        return {'img_url':None,'img_file':None}

    def get_section(self,product_obj):
        if product_obj.section :
            return {'id': product_obj.section.id , 'name':product_obj.section.name }
        return {'id':None,'name':None}
    def get_categorie(self,product_obj):
        if product_obj.categorie :
            return {'id': product_obj.categorie.id , 'name':product_obj.categorie.name }
        return {'id':None,'name':None}
    def get_subcategorie(self,product_obj):
        if product_obj.subcategorie :
            return {'id': product_obj.subcategorie.id , 'name':product_obj.subcategorie.name }
        return {'id':None,'name':None}




    # def get_sizes(self,product_obj):
    #     size_qs    = product_obj.sizes.all()
    #     serializer = SizeSerializer(size_qs,many=True)
    #     return serializer.data
    #
    # def get_colors(self,product_obj):
    #     color_qs    = product_obj.colors.all()
    #     serializer = ColorSerializer(size_qs,many=True)
    #     return serializer.data

    def get_add_imgs(self,product_obj):
        image_qs = product_obj.add_imgs.all()
        serializer = ImageSerializer(image_qs,many=True)
        return serializer.data
