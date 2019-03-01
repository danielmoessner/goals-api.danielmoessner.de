from django.views.generic.edit import FormMixin
from django.template.loader import render_to_string
from django.shortcuts import redirect
from django.shortcuts import render
from django.views import generic
from django.http import HttpResponse

import json


# views
class IndexView(generic.TemplateView):
    template_name = 'core_index.j2'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:redirect', permanent=False)
        else:
            return super(IndexView, self).get(request, *args, **kwargs)


class RedirectView(generic.RedirectView):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('users:sign_in', permanent=False)
        else:
            page_choice = request.user.page_choice
            if page_choice == 'DASHBOARD':
                return redirect('goals:index', permanent=False)
            elif page_choice == 'TO_DOS':
                return redirect('goals:to_dos_view', permanent=False)
            elif page_choice == 'TREE':
                return redirect('goals:tree_view', permanent=False)
            elif page_choice == 'STAR':
                return redirect('goals:star_view', permanent=False)
            elif page_choice == 'NOTES':
                return redirect('notes:index', permanent=False)
            return redirect('goals:index', permanent=False)


# mixins
class CustomGetFormMixin(FormMixin):
    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        user = self.request.user
        return form_class(user, **self.get_form_kwargs())


class CustomAjaxFormMixin(object):
    def form_invalid(self, form):
        html = render_to_string(self.template_name, self.get_context_data(form=form),
                                request=self.request)
        return HttpResponse(json.dumps({"valid": False, "html": html}),
                            content_type="application/json")

    def form_valid(self, form):
        form.save()
        return HttpResponse(json.dumps({"valid": True}), content_type="application/json")


class CustomSimpleAjaxFormMixin(object):
    def form_invalid(self, form):
        return HttpResponse(json.dumps({"valid": False, "html": "Error"}),
                            content_type="application/json")

    def form_valid(self, form):
        form.save()
        return HttpResponse(json.dumps({"valid": True}), content_type="application/json")


class CustomAjaxDeleteMixin(object):
    def delete(self, request, *args, **kwargs):
        object = self.get_object()
        object.delete()
        return HttpResponse(json.dumps({"valid": True}), content_type="application/json")


# error views
def error_400_view(request, exception=None):
    return render(request, "error_templates/400.html")


def error_403_view(request, exception=None):
    return render(request, "error_templates/403.html")


def error_404_view(request, exception=None):
    return render(request, "error_templates/404.html")


def error_500_view(request, exception=None):
    return render(request, "error_templates/500.html")
