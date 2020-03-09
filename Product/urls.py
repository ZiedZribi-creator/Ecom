from django.urls import path
from django.conf.urls import include
from rest_framework import routers
from .views import (ProductViewset,ImageViewset,
                    SectionViewset,CategorieViewset,SubCategorieViewset
                    )

router = routers.DefaultRouter()
router.register('product',ProductViewset)
router.register('image',ImageViewset)
router.register('section',SectionViewset)
router.register('categorie',CategorieViewset)
router.register('subcategorie',SubCategorieViewset)

urlpatterns = [
path('',include(router.urls)),

]
