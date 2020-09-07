from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.views import generic


class SettingsView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'users/users_settings.j2'


class SignUpView(generic.TemplateView):
    template_name = 'users/users_sign_up.j2'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:redirect', permanent=False)
        return super(SignUpView, self).get(self, request, *args, **kwargs)


class SignInView(generic.TemplateView):
    template_name = 'users/users_sign_in.j2'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('core:redirect', permanent=False)
        return super(SignInView, self).get(self, request, *args, **kwargs)
