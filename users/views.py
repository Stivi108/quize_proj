from django.views import View
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.views import LoginView


# Create your views here.

class RegisterUserView(View):
    def get(self, request):
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
        return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()  # Сохраняем пользователя
            profile = profile_form.save(commit=False)  # Не сохраняем сразу, связать с пользователем
            profile.user = user
            profile.save()  # Сохраняем профиль
            messages.success(request, 'Регистрация прошла успешно!')
            return redirect('taskmaster:home')  # Перенаправление на главную страницу
        else:
            messages.error(request, 'Ошибка при регистрации. Пожалуйста, исправьте ошибки.')

        return render(request, 'users/register.html', {'user_form': user_form, 'profile_form': profile_form})


class CustomLoginView(LoginView):
    template_name = 'users/login.html'
