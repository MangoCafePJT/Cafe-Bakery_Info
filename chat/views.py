from django.shortcuts import render, redirect


# Create your views here.
# def index(request):
    
#     return render(request, 'chat/index.html')
def index(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        if room_name:
            return redirect('chat:room', room_name=room_name)
        else:
            return redirect('chat:index')
    return render(request, 'chat/index.html')

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name': room_name
    })