from users.models import Profile, Relationship

def profile_pic(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        pic = profile_obj.image
        return {'picture': pic}
    return {}

def invitations_received_number(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.get(user=request.user)
        qs_count = Relationship.objects.invitations_received(profile_obj).count()
        return {'invites_num': qs_count}
    return {}
