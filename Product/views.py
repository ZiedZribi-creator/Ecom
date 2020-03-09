from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status,generics
from .models import Product,Size,Image,Color,Categorie,SubCategorie,Section,ProductVariant
from .serializers import (ProductSerializer,ImageSerializer,
                        CategorieSerializer,SubCategorieSerializer,
                        SectionSerializer)
from rest_framework.pagination import PageNumberPagination
import json
from django.db.models import Q

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 1000



class ProductViewset(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    lookup_field = 'slug'
    def get_queryset(self):
        search =  self.request.GET.get('search')
        sec    =  self.request.GET.get('sec')
        cat    =  self.request.GET.get('cat')
        subcat =  self.request.GET.get('subcat')
        print(str(sec)+' / '+str(cat)+' / '+str(subcat))
        qs = Product.objects.all()
        if search or sec  :
            print('search or sec')
            if search :
                print('search')
                qs = qs.filter(title__icontains=search)
            if sec :
                print('sec')
                qs = qs.filter(section__name=sec)
                if cat :
                    print('cat')
                    qs.filter(categorie__name=cat)
                    if subcat :
                        print('subcat')
                        qs.filter(subcategorie__name=subcat)

        return qs
        # cat = self.request.GET.get('categorie')
        # subcat = self.request.GET.get('subcategorie')
        # qs = Product.objects.all()
        # if search or section or cat or subcat :
        #     if search :
        #         qs = Product.objects.filter(title__icontains=search)
        #     if section :
        #         qs = qs.filter(section__name = section)
        #     if cat :
        #         qs = qs.filter(categorie__name = cat)
        #     if subcat :
        #         qs = qs.filter(subcategorie__name = subcat)
        # return qs
    @action(methods=['put'],detail=True)
    def custom_update(self,request,*args,**kwargs):
        product_data = request.data
        print(product_data)
        product_obj = self.get_object()
        title = product_data.get('title')
        description = product_data.get('description')
        price = float(product_data.get('price'))
        product_obj.title = title
        product_obj.description = description
        product_obj.price = price
        section = product_data.get('section')
        if section != 'null'  :
            sec_obj     = Section.objects.get(name=section)
            product_obj.section = sec_obj
            categorie = product_data.get('categorie')
            if categorie != 'null' :
                cat_obj = sec_obj.categorie.get(name=categorie)
                product_obj.categorie = cat_obj
                subcategorie = product_data.get('subcategorie')
                if subcategorie != 'null' :
                    subcat_obj  = cat_obj.subcategorie.filter(name=subcategorie)[0]
                    product_obj.subcategorie = subcat_obj
        product_obj.save()
        primary_img = product_data.get('primary_img')
        product_data_dict = dict(request.data)
        primary_img_obj = None
        if primary_img :
            primary_img_obj = Image.objects.create(image=primary_img,primary=True)
            product_obj.add_imgs.add(primary_img_obj)
            product_obj.save()
            del product_data_dict['primary_img']
        del product_data_dict['description']
        del product_data_dict['title']
        del product_data_dict['section']
        del product_data_dict['categorie']
        del product_data_dict['subcategorie']
        product_data_keys = list(product_data_dict.keys())
        product_data_keys.reverse()
        add_img_objs = []
        pv_products =[]
        pv = {}
        for i,key in enumerate(product_data_keys) :
            if key.startswith('add_img_'):
                image_obj = Image.objects.create(image=product_data.get(key))
                add_img_objs.append(image_obj)
                product_obj.add_imgs.add(image_obj)
                product_obj.save()
            elif key.startswith('pv_') :
                print(i+1,' ',len(product_data_keys))
                next_pv_idx = product_data_keys[i+1][3] if (i+1) < len(product_data_keys) else None
                if key[3] != next_pv_idx  : # save the last pv_obj and start with a new pv_obj
                    pv[key[5:]] = product_data.get(key) # put the last key
                    if 'img_idx' in pv.keys() :
                        if int(pv['img_idx']) == -1 :
                            pv['image'] = primary_img_obj if primary_img else product_obj.add_imgs.all().filter(primary=True)
                        else :
                            pv['image'] = add_img_objs[int(pv['img_idx'])]
                        del pv['img_idx']
                    elif 'img_id' in pv.keys():
                        pv['image'] = Image.objects.get(id=int(pv['img_id']))
                        del pv['img_id']
                    pv_obj = ProductVariant.objects.create(**pv)
                    product_obj.product_variants.add(pv_obj)
                    product_obj.save()
                    pv = {}
                else :  # set pv_obj key value
                    pv[key[5:]] = product_data.get(key)

        ser = ProductSerializer(product_obj,many=False)
        return Response({'res':ser.data},status=status.HTTP_200_OK)
    @action(methods=['post'],detail=False)
    def custom_creation(self,request,*args,**kwargs):
        product_data = request.data
        print(product_data)
        title = product_data.get('title')
        description = product_data.get('description')
        price = product_data.get('price')
        product_obj = Product.objects.create(title=title,description=description,price=price)
        section = product_data.get('section')
        if section != 'null'  :
            sec_obj     = Section.objects.get(name=section)
            product_obj.section = sec_obj
            categorie = product_data.get('categorie')
            if categorie != 'null' :
                cat_obj = sec_obj.categorie.get(name=categorie)
                product_obj.categorie = cat_obj
                subcategorie = product_data.get('subcategorie')
                if subcategorie != 'null' :
                    subcat_obj  = cat_obj.subcategorie.filter(name=subcategorie)[0]
                    product_obj.subcategorie = subcat_obj
        primary_img = product_data.get('primary_img')
        primary_img_obj = Image.objects.create(image=primary_img,primary=True)
        product_obj.add_imgs.add(primary_img_obj)
        product_obj.save()
        product_data_dict = dict(request.data)
        del product_data_dict['description']
        del product_data_dict['title']
        del product_data_dict['primary_img']
        del product_data_dict['section']
        del product_data_dict['categorie']
        del product_data_dict['subcategorie']
        product_data_keys = list(product_data_dict.keys())
        product_data_keys.reverse()
        add_img_objs = []
        pv_products =[]
        pv = {}
        for i,key in enumerate(product_data_keys) :
            if key.startswith('add_img_'):
                image_obj = Image.objects.create(image=product_data.get(key))
                add_img_objs.append(image_obj)
                product_obj.add_imgs.add(image_obj)
                product_obj.save()
            elif key.startswith('pv_') :
                print(i+1,' ',len(product_data_keys))
                next_pv_idx = product_data_keys[i+1][3] if (i+1) < len(product_data_keys) else None
                if key[3] != next_pv_idx  : # save the last pv_obj and start with a new pv_obj
                    pv[key[5:]] = product_data.get(key) # put the last key
                    if 'img_idx' in pv.keys() :
                        if int(pv['img_idx']) == -1 :
                            pv['image'] = primary_img_obj
                        else :
                            pv['image'] = add_img_objs[int(pv['img_idx'])]
                        del pv['img_idx']
                    elif 'img_id' in pv.keys():
                        pv['image'] = Image.objects.get(id=int(pv['img_id']))
                        del pv['img_id']
                    pv_obj = ProductVariant.objects.create(**pv)
                    product_obj.product_variants.add(pv_obj)
                    product_obj.save()
                    pv = {}
                else :  # set pv_obj key value
                    pv[key[5:]] = product_data.get(key)

        ser = ProductSerializer(product_obj,many=False)
        return Response({'res':ser.data},status=status.HTTP_200_OK)

    @action(methods=['put'],detail=False)
    def add_pv(self,request):
        product_obj = self.get_object()
        product_variant_obj = PorductVariant.objects.create(**self.requets.data)
        ser = ProductVariantSerializer(product_variant_obj,many=False)
        return Response({'res':ser.data},status=status.HTTP_200_OK)

    @action(methods=['put'],detail=True)
    def drop_add_img(self,request,*args,**kwargs):
        add_img_id = self.request.data.get('add_img_id')
        img_obj = Image.objects.get(id=add_img_id)
        img_obj.delete()
        return Response({'res':'img deleted'},status=status.HTTP_200_OK)

    @action(methods=['put'],detail=True)
    def drop_primary_img(self,request,*args,**kwargs):
        product_obj = self.get_object()
        qs = product_obj.add_imgs.all()
        for p_img in qs :
            p_img.delete()
        return Response({'res':'primary img deleted'},status=status.HTTP_200_OK)

    @action(methods=['put'],detail=True)
    def drop_pv(self,request,*args,**kwargs):
        pv_id = self.request.data.get('pv_id')
        product_variant_obj = ProductVariant.objects.get(id=pv_id)
        product_variant_obj.delete()
        return Response({'res':'product variant deleted'},status=status.HTTP_200_OK)








class ImageViewset(ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class SubCategorieViewset(ModelViewSet):
    queryset = SubCategorie.objects.all()
    serializer_class = SubCategorieSerializer

class CategorieViewset(ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer

    @action(methods=['put'],detail=True)
    def add_subcategorie(self,request,pk):
        categorie_obj = self.get_object()
        subcategorie_value = request.data.get('name')
        subcat_obj = SubCategorie.objects.create(name=subcategorie_value)
        categorie_obj.subcategorie.add(subcat_obj)
        return Response({'id':subcat_obj.id,'name':subcat_obj.name},status=status.HTTP_200_OK)

    @action(methods=['put'],detail=True)
    def drop_subcategorie(self,request,pk):
        categorie_obj = self.get_object()
        subcategorie_id    = request.POST.get('subcategorie_id')
        categorie_obj.drop_subcategorie(subcategorie_id=subcategorie_id)
        return Response({'response':'image dropped'},status=status.HTTP_200_OK)

    @action(methods=['put'],detail=True)
    def update_subcategorie(self,request,pk):
        section_obj = self.get_object()
        new_subcategorie_value = request.POST.get('new_subcategorie_value')
        subcategorie_id        = request.POST.get('subcategorie_id')
        section_obj.update_subcategorie_value(subcategorie_id=subcategorie_id,new_subcategorie_value=new_subcategorie_value)
        return Response({'response':'subcategorie value updated'},status=status.HTTP_200_OK)

    @action(methods=['put'],detail=True)
    def delete_subcategorie(self,request,pk):
        section_obj      = self.get_object()
        subcategorie_id  = request.POST.get('subcategorie_id')
        subcategorie_obj = Categorie.objects.get(id=subcategorie_id)
        subcategorie_obj.delete()
        return Response({'response':'subcategorie deleted'},status=status.HTTP_200_OK)

class SectionViewset(ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    @action(methods=['put'],detail=True)
    def add_categorie(self,request,pk):
        section_obj = self.get_object()
        categorie_value = request.data.get('name')
        cat_obj = Categorie.objects.create(name=categorie_value)
        section_obj.categorie.add(cat_obj)
        return Response({'id':cat_obj.id,'name':cat_obj.name},status=status.HTTP_200_OK)

    @action(methods=['put'],detail=True)
    def drop_categorie(self,request,pk):
        section_obj = self.get_object()
        categorie_id    = request.POST.get('categorie_id')
        section_obj.drop_categorie(categorie_id='categorie_id')
        return Response({'response':'categorie dropped'},status=status.HTTP_200_OK)

    @action(methods=['put'],detail=True)
    def update_categorie(self,request,pk):
        section_obj = self.get_object()
        new_categorie_value = request.POST.get('new_categorie_value')
        categorie_id        = request.POST.get('categorie_id')
        section_obj.update_categorie_value(categorie_id=categorie_id,new_categorie_value=new_categorie_value)
        return Response({'response':'categorie value updated'},status=status.HTTP_200_OK)

    @action(methods=['put'],detail=True)
    def delete_categorie(self,request,pk):
        section_obj   = self.get_object()
        categorie_id  = request.POST.get('categorie_id')
        categorie_obj = Categorie.objects.get(id = categorie_id)
        categorie_obj.delete()
        return Response({'response':'categorie deleted'},status=status.HTTP_200_OK)
