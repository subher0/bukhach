from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from bukhach.forms import AddFriendForm
from bukhach.models.profile_models import Profile


@login_required(login_url='/login')
def profile_view(request, profileId):
    template = loader.get_template('bukhach/profile.html')
    profile = Profile.objects.filter(id=profileId).first()
    friends = profile.friends.all()
    user_profile = request.user.profile
    is_friend = None
    if profile in user_profile.friends.all():
        is_friend = True

    context = {
        'profile': profile,
        'friends': friends,
        'is_friend': is_friend
    }
    return HttpResponse(template.render(context, request))


@login_required(login_url='/login')
def add_friend(request):
    if request.method == 'POST':
        form = AddFriendForm(request.POST)
        if form.is_valid():
            user_profile = Profile.objects.filter(user=request.user).first()
            friend_profile = Profile.objects.filter(id=form.cleaned_data['profile_id']).first()
            user_profile.friends.add(friend_profile)
            return profile_view(request, form.cleaned_data['profile_id'])
        else:
            return redirect('/dashboard')
    else:
        return redirect('/dashboard')