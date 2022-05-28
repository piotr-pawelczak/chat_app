from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.models import User
from chat.models import ChatMessage


@login_required
def index_view(request):
    users = User.objects.exclude(username=request.user.username)
    context = {"users": users}
    return render(request, "chat/index.html", context)


@login_required
def room(request, username):
    receiver_user = User.objects.get(username=username)
    users = User.objects.exclude(username=request.user.username)

    if request.user.id > receiver_user.id:
        thread_name = f'chat_{request.user.id}-{receiver_user.id}'
    else:
        thread_name = f'chat_{receiver_user.id}-{request.user.id}'

    messages = ChatMessage.objects.filter(thread_name=thread_name)
    context = {"users": users, "receiver_user": receiver_user, "chat_messages": messages}
    return render(request, 'chat/room.html', context)
