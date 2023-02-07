from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Profile


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request,
                          'accounts/register_done.html',
                          {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'accounts/register.html', {'user_form': user_form})


@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Профиль успешно изменен')
        else:
            messages.error(request, 'При обновлении профиля возникла ошибка')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user)
    return render(request, 'accounts/edit.html',
                  {'user_form': user_form, 'profile_form': profile_form})


@login_required
def dashboard(request):
    return render(request, 'accounts/dashboard.html', {'section': 'dashboard'})
