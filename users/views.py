from django.shortcuts import render
from users.forms import UserRegisterForm
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'You are successfully registered! You can log in now.')
            return redirect(reverse('users:login'))
    else:
        user_form = UserRegisterForm()

    context = {'user_form': user_form}

    return render(request, 'users/register.html', context)
