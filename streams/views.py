# streams/views.py

from django.shortcuts import render, get_object_or_404,redirect,HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
import os
from django.contrib.auth.models import User
import tempfile
import subprocess
from django.contrib.auth import authenticate, login, logout
from .models import LiveStream,UserProfile
from django.contrib.auth.forms import UserCreationForm

@csrf_exempt
def live_stream(request, stream_id):
    stream = get_object_or_404(LiveStream, pk=stream_id)
    stream_path = '/home/development/Desktop/stream/livestream/videos/galaxy_black_hole_planet_spiral_621.mp4' 
    
    if not os.path.exists(stream_path):
        return HttpResponse(status=404)

    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        subprocess.run(['ffmpeg', '-i', stream_path, '-vcodec', 'copy', '-acodec', 'copy', '-f', 'mp4', '-movflags', 'frag_keyframe+empty_moov', '-'], stdout=temp_file)

    with open(temp_file.name, 'rb') as f:
        response = HttpResponse(f.read(), content_type='video/mp4')
        response['Content-Length'] = os.path.getsize(temp_file.name)
        response['Content-Disposition'] = 'inline; filename="stream.mp4"'

    os.unlink(temp_file.name)

    return response

@login_required
@csrf_exempt
def create_live_stream(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        stream = LiveStream.objects.create(user=request.user,name=name, description=description, start_time=now(), is_live=True)
        stream.save()
        live_stream(request, stream.id)
        return HttpResponse()
    
    return render(request, 'streams/create_stream.html')



# View Live Stream

@login_required
def view_my_streams(request):
    streams = LiveStream.objects.filter(user=request.user)
    return render(request, 'streams/my_streams.html', {'streams': streams})


# 11. view to handle auth 

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('view_my_streams')
        else:
            error = 'Invalid username or password'
    return render(request, 'streams/login.html')  

# logout

def user_logout(request):
    logout(request)
    return redirect('user_login')


#user registration


@csrf_exempt
def user_signup(request):
    if request.method == 'POST':
        # Get the form data from the request
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        # Check if the passwords match
        if password != password_confirm:
            return render(request, 'register.html', {'error': 'Passwords do not match'})

        # Create a new user
        user = User.objects.create_user(username=username, password=password)
        user.save()

        # Authenticate the user and log them in
        user = authenticate(username=username, password=password)
        login(request, user)

        # Redirect to the home page
        return redirect('view_my_streams')

    return render(request, 'streams/signup.html')
       
