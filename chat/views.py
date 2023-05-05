from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.
# def index(request):
    
#     return render(request, 'chat/index.html')
@login_required
def index(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        if room_name:
            return redirect('chat:room', room_name=room_name)
        else:
            return redirect('chat:index')
    return render(request, 'chat/index.html')

@login_required
def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })