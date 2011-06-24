from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.views.generic.list_detail import object_detail

from accounts.models import UserProfile

def profile(request):
    """Show a user profile."""
    object_id = request.user.userprofile.id
    queryset = UserProfile.objects.all()
    return object_detail(request, queryset=queryset, object_id=object_id,
                         template_name='accounts/profile.html',
                         template_object_name='profile')


def register(request):
    """Create a new user using UserCreationForm."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(user.get_profile().get_absolute_url())
    else:
        form = UserCreationForm()

    template_args = {
        'form': form,
    }
    return render_to_response('accounts/register.html', template_args)
