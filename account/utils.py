import random
import string
from django.utils.text import slugify

def random_string_generator(size=5, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



def unique_slug_generator(instance, new_slug=None):

    if new_slug is not None:
        slug = new_slug
    else:
        if hasattr(instance,'title') :
            slug = slugify(instance.title)
        elif hasattr(instance,'user') :
            slug = slugify(instance.user.username)
        elif hasattr(instance,'full_name') :
            slug = slugify(instance.full_name)
        elif hasattr(instance,'result') :
            slug = slugify(random_string_generator(size=4))
            Model = instance.__class__
            qs_exists = Model.objects.filter(slug=slug).exists()
            while qs_exists :
                slug = slugify(random_string_generator(size=4))
                qs_exists = Model.objects.filter(slug=slug).exists()


    Model = instance.__class__
    qs_exists = Model.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug
