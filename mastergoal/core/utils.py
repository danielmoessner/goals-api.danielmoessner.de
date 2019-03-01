from django.utils.html import strip_tags
from django.utils.text import slugify

from django.conf import settings


def print_df(df):
    if settings.DEBUG:
        import tabulate
        table = tabulate.tabulate(df, headers="keys")
        print(table)


def create_slug(instance, on=None, slug=None):
    if slug is None:
        if on:
            slug = slugify(on)
        else:
            slug = slugify(instance.name)

    instance_class = instance.__class__
    qs = instance_class.objects.filter(slug=slug).order_by("-pk")
    if qs.exists():
        new_slug = "%s-%s" % (slug, qs.first().pk)
        return create_slug(instance=instance, on=on, slug=new_slug)
    return slug


def form_invalid_universal(view, form, errors_name, heading="Something went wrong.", **kwargs):
    context = view.get_context_data(**kwargs)
    context[errors_name] = [heading, ]
    for field in form:
        context[errors_name].append(
            strip_tags(field.errors).replace(".", ". ").replace("  ", " ")
        )
    while "" in context[errors_name]:
        context[errors_name].remove("")
    return view.render_to_response(context)


def errors_to_view(view, errors_heading="Something went wrong.", errors=()):
    errors = list(errors)
    errors.insert(0, errors_heading)
    context = view.get_context_data()
    context["errors"] = errors
    return view.render_to_response(context)


def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)
