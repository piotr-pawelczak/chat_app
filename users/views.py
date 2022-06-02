from django.shortcuts import render, get_object_or_404
from users.forms import UserRegisterForm, ProfileForm, UserEditForm
from django.contrib import messages
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(user_logged_in)
def got_online(user, request, **kwargs):
    user.profile.is_online = True
    user.profile.save()


@receiver(user_logged_out)
def got_offline(user, request, **kwargs):
    user.profile.is_online = False
    user.profile.save()


def register(request):
    if request.method == 'POST':
        user_form = UserRegisterForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            messages.success(request, 'You are successfully registered! You can log in now.')
            return redirect(reverse('users:login'))
    else:
        user_form = UserRegisterForm()
        profile_form = ProfileForm()

    context = {'user_form': user_form, "profile_form": profile_form}

    return render(request, 'users/register.html', context)


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    context = {'user': user}
    return render(request, 'users/profile_view.html', context)


def profile_edit(request, username):
    user = get_object_or_404(User, username=username)

    user_form = UserEditForm(instance=user)
    profile_form = ProfileForm(instance=user.profile)

    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('users:profile', user.username)
    context = {'user_form': user_form, 'profile_form': profile_form}

    return render(request, 'users/profile_update.html', context)


def user_delete(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        user.delete()
        messages.warning(request, 'User has been deleted')
    return redirect(reverse('chat:index'))
