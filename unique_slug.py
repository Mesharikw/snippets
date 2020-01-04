import random
import string

from django.utils.text import slugify


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_unique_slug(instance, fields=None):
    if fields is None:
        fields = ['name']
    Klass = instance.__class__
    _ = list(map(lambda a: slugify(getattr(instance, a) if a != '__str__' else getattr(instance, a)(), allow_unicode=True), fields))
    if len(_) > 1:
        __ = list(map(lambda a: _[0] + "-" + a, _[1:]))
        __.insert(0, _[0])
    else:
        __ = [_[0]]

    if instance.slug == _[0]: return _[0]
    try:
        original_slug = Klass.objects.get(pk=instance.pk).slug
    except:
        original_slug = False

    for i in __:
        if not Klass.objects.filter(slug=i).exists() or original_slug == i:
            return i

    slug = _[0]
    unique_slug = slug
    extension = 1

    while Klass.objects.filter(slug=slug).exists:
        unique_slug = F"{slug}{extension}"
        extension += 1
    return unique_slug
