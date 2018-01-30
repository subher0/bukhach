from bukhach.models.profile_models import Profile


def navbar_avatar(request):
    if request.user.is_anonymous:
        return {}
    profile = Profile.objects.filter(user=request.user).first()
    context = {
        'profile_preloaded': profile
    }
    return context