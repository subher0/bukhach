from bukhach.models.profile_models import Profile


def navbar_avatar(request):
    profile = Profile.objects.filter(user=request.user).first()
    context = {
        'profile_preloaded': profile
    }
    return context