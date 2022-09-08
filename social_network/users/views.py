from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import Profile, Relationship
from users.forms import ProfileModelForm


def home(request):
    return render(request, 'main/home.html')

@login_required
def user_profile(request):
    profile = Profile.objects.get(user=request.user)
    form = ProfileModelForm(request.POST or None, request.FILES or None, instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True
    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }
    return render(request, 'users/profile.html', context)

@login_required
def invites_received(request):
    profile = Profile.objects.get(user=request.user)
    queryset = Relationship.objects.invitations_received(profile)
    results = list(map(lambda x: x.sender, queryset))
    is_empty = False
    if len(results) == 0:
        is_empty = True
    context = {
        'queryset': results,
        'is_empty': is_empty
    }

    return render(request, 'users/my_invites.html', context)

@login_required
def accept_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        if rel.status == 'send':
            rel.status = 'accepted'
            rel.save()
    return redirect('users:my_invites')

@login_required
def reject_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender = Profile.objects.get(pk=pk)
        receiver = Profile.objects.get(user=request.user)
        rel = get_object_or_404(Relationship, sender=sender, receiver=receiver)
        rel.delete()
    return redirect('users:my_invites')


class ProfileInviteListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'users/list_invitations.html'

    def get_queryset(self):
        queryset = Profile.objects.get_all_profiles_to_invite(self.request.user)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        r_receiver = Relationship.objects.filter(sender=profile)
        r_sender = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in r_receiver:
            rel_receiver.append(item.receiver.user)
        for item in r_sender:
            rel_sender.append(item.sender.user)

        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context

@login_required
def profiles_list(request):
    user = request.user
    queryset = Profile.objects.get_all_profiles(user)

    context = {'queryset': queryset}

    return render(request, 'users/profiles_list.html', context)


class ProfileListView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'users/profiles_list.html'

    def get_queryset(self):
        queryset = Profile.objects.get_all_profiles(self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        r_receiver = Relationship.objects.filter(sender=profile)
        r_sender = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in r_receiver:
            rel_receiver.append(item.receiver.user)
        for item in r_sender:
            rel_sender.append(item.sender.user)

        context['rel_receiver'] = rel_receiver
        context['rel_sender'] = rel_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True
        return context


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'users/detail.html'

    def get_object(self, slug=None):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = Profile.objects.get(user=self.request.user)
        rel_r = Relationship.objects.filter(sender=profile)
        rel_s = Relationship.objects.filter(receiver=profile)
        rel_receiver = []
        rel_sender = []
        for item in rel_r:
            rel_receiver.append(item.receiver.user)
        for item in rel_s:
            rel_sender.append(item.sender.user)
        context["rel_receiver"] = rel_receiver
        context["rel_sender"] = rel_sender
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False
        return context

@login_required
def send_invitation(request):
   if request.method == 'POST':
       pk = request.POST.get('profile_pk')
       user = request.user
       sender = Profile.objects.get(user=user)
       receiver = Profile.objects.get(pk=pk)

       rel = Relationship.objects.create(sender=sender, receiver=receiver, status='send')

       return redirect(request.META.get('HTTP_REFERER'))
   return redirect('users:profile')

@login_required
def remove_from_friends(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        user = request.user
        sender = Profile.objects.get(user=user)
        receiver = Profile.objects.get(pk=pk)

        rel = Relationship.objects.filter(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))
        )
        rel.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('users:profile')
