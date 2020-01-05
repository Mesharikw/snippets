from django.utils.text import slugify


def my_slugify(value, **kwargs):
    return slugify(str(value).replace(":", "-").replace("/", "-"), **kwargs)


def get_unique_slug(instance, fields=None):
    if fields is None:
        fields = ['name']
    Klass = instance.__class__
    newFields = []
    for field in fields:

        try:
            newFields.append(getattr(instance, field)())
        except:
            newFields.append(getattr(instance, field))

    _ = list(map(lambda a: my_slugify(a, allow_unicode=True), newFields))
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
