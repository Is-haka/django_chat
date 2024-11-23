from django.shortcuts import render, redirect
from django.urls import reverse

def index(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name', '').strip()
        username = request.POST.get('username', '').strip()
        
        if room_name and username:
            # Format room name consistently
            formatted_room_name = room_name.replace(' ', '-').lower()
            return redirect(reverse('chat:room', kwargs={
                'room_name': formatted_room_name,
                'username': username
            }))
    
    return render(request, 'index.html')

def chatroom(request, room_name, username):
    return render(request, 'room.html', {
        'room_name': room_name,
        'username': username
    })