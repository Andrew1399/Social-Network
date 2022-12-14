from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest
from django.contrib.auth.models import User
from messenger.models import Message
import json


@login_required
def inbox(request):
    conversations = Message.get_conversations(user=request.user)
    active_conversation = None
    messages = None
    if conversations:
        conversation = conversations[0]
        active_conversation = conversation['user'].username
        messages = Message.objects.filter(user=request.user, conversation=conversation['user'])
        messages.update(is_read=True)
        for conversation in conversations:
            if conversation['user'].username == active_conversation:
                conversation['unread'] = 0

    context = {
        'messages': messages,
        'conversations': conversations,
        'active': active_conversation
    }
    return render(request, 'messenger/inbox.html', context)

@login_required
def messages(request, username):
    conversations = Message.get_conversations(user=request.user)
    active_conversation = username
    mes = Message.objects.filter(user=request.user, conversation__username=username)
    mes.update(is_read=True)
    for conversation in conversations:
        if conversation['user'].username == username:
            conversation['unread'] = 0
    context = {
        'messages': mes,
        'conversations': conversations,
        'active': active_conversation
    }
    return render(request, 'messenger/inbox.html', context)

@login_required
def new(request):
    if request.method == 'POST':
        from_user = request.user
        to_user_username = request.POST.get('to')
        try:
            to_user = User.objects.get(username=to_user_username)
        except Exception:
            try:
                to_user_username = to_user_username[to_user_username.rfind('(') + 1:len(to_user_username) -1]
                to_user = User.objects.get(username=to_user_username)
            except Exception:
                return redirect('/messages/new')
        message = request.POST.get('message')
        if len(message.strip()) == 0:
            return redirect('/messages/new')
        if from_user != to_user:
            Message.send_message(from_user, to_user, message)
        return redirect('messenger:inbox')
    else:
        conversations = Message.get_conversations(user=request.user)
        context = {'conversations': conversations}
        return render(request, 'messenger/new.html', context)

@login_required
def send(request):
    if request.method == 'POST':
        from_user = request.user
        to_user_username = request.POST.get('to')
        to_user = User.objects.get(username=to_user_username)
        message = request.POST.get('message')
        if len(message.strip()) == 0:
            return redirect('messenger:inbox')
        if from_user != to_user:
            msg = Message.send_message(from_user, to_user, message)
            return redirect(request.META.get('HTTP_REFERER'))
        return HttpResponse()
    else:
        return HttpResponseBadRequest()

@login_required
def users(request):
    users = User.objects.filter(is_active=True)
    dump = []
    template = u'{0} ({1})'
    for user in users:
        if user.profile.get_screen_name() != user.username:
            dump.append(template.format(user.profile.get_screen_name(), user.username))
        else:
            dump.append(user.username)
    data = json.dumps(dump)
    return HttpResponse(data, content_type='application/json')
