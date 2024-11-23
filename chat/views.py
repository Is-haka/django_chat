from django.shortcuts import render, redirect
from django.urls import reverse

def index(request):
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        username = request.POST.get('username')
        print(f"We received username: {username} and room name: {room_name}")
        
        # Redirect to chat room
        return redirect(reverse('chat:room', kwargs={'room_name': room_name, 'username': username}))
    
    return render(request, 'index.html')

def chatroom(request, room_name, username):
    return render(request, 'room.html', {'room_name': room_name, 'username': username})