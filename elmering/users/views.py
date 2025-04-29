from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.views.generic import CreateView, UpdateView
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from users.forms import (
    UserRegistrationForm,
    UserLoginForm,
    UserProfileForm,
    UserPasswordChangeForm
    )


class UserRegistrationView(CreateView):
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('words_polls:index')

    def form_valid(self, form):
        response = super().form_valid(form)

        user = authenticate(
            email=form.cleaned_data.get('email'),
            password=form.cleaned_data.get('password1')
            )
        if user is not None:
            login(self.request, user)
            messages.success(self.request,
                             f"{user.username} registered successfully.")
        return response


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    # success_url = reverse_lazy('words_polls:index')

    def get_success_url(self):
        return reverse_lazy('words_polls:index')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = form.get_user()
        if user:
            messages.success(self.request,
                             f"{user.email} logged in successfully.")
            return response

    def form_invalid(self, form):
        self.request.session['username'] = form.data.get('username')
        return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.request.session.get('username', '')
        return context


class UserProfileView(LoginRequiredMixin, UpdateView):
    template_name = 'users/profile.html'
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Password changed successfully.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Password change failed.")
        return super().form_invalid(form)


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "User logged out successfully.")
    return redirect(reverse('words_polls:index'))
