from django.shortcuts import render, redirect
from accounts.models import *
from accounts.forms import *

# CVB

from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Django authentication

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

# Create your views here.

def register_request(request):

    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            print(username)
            form.save()
            return render(request, 'blog/home.html', {"title": "Home", "message": f"Usuario {username} creado!"})
            return redirect('Home')
        else:
            return render(request, 'blog/home.html', {"title": "Home", "message": "Error de registro", "errors": ["No se pudo crear el usuario. Revise los datos e intente nuevamente"]})
    
    else:
        form = UserRegistrationForm()
        return render(request, 'accounts/register.html', {"form": form})

def login_request(request):

    if  request.method == "POST":

        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            data = form.cleaned_data
            username = data.get('username')
            password = data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return render(request, 'blog/home.html', {"title": "Home", "message": f"Bienvenido usuario {user}!"})
            else:
                return render(request, 'blog/home.html', {"title": "Home", "message": "Error", "errors": [f"El usuario {user} no existe"]})
        
        else:
            return render(request, 'blog/home.html', {"title": "Home", "message": "Error de login", "errors": ["No se pudo iniciar sesión con el usuario ingresado. Revise los datos e intente nuevamente."]})

    else:
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', {"form": form})

@login_required()
def update_user(request):

    user = request.user

    if request.method == "POST":
        form = UserEditForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            user.name = data["name"]
            user.email = data["email"]
            # user.password1 = data["password1"]
            # user.password2 = data["password2"]
            password1 = form.cleaned_data.get("password1")
            password2 = form.cleaned_data.get("password2")
            if password1:
                user.set_password(password1)  # Establecer la contraseña de manera segura
                update_session_auth_hash(request, user)  # Actualizar la sesión del usuario para evitar el cierre de sesión
            if password2:
                user.set_password(password2)  # Establecer la contraseña de manera segura
                update_session_auth_hash(request, user)  # Actualizar la sesión del usuario para evitar el cierre de sesión
            user.save()
            return redirect("Home")
        else:
            form = UserEditForm(initial={"email":user.email})
            return render(request, 'accounts/update_user.html', {"title": "Editar usuario", "message": "Editar usuario", "form": form, "errors": ["Datos inválidos"]})
    
    else:
        form = UserEditForm(initial={"email":user.email})
        return render(request, 'accounts/update_user.html', {"title": "Editar usuario", "message": "Editar usuario", "form": form})

@login_required()
def profile(request):

    avatar = Avatar.objects.filter(user=request.user)

    if len(avatar) > 0:
        imagen = avatar[0].imagen.url
        return render(request, 'accounts/profile.html', {"image_url": imagen})

    return render (request, 'accounts/profile.html')

@login_required()
def upload_avatar(request):   
    
    
    if request.method == "POST":

        formulario = AvatarForm(request.POST,request.FILES)

        if formulario.is_valid():

            usuario = request.user

            avatar = Avatar.objects.filter(user=usuario)

            if len(avatar) > 0:
                avatar = avatar[0]
                avatar.imagen = formulario.cleaned_data["imagen"]
                avatar.save()

            else:
                avatar = Avatar(user=usuario, imagen=formulario.cleaned_data["imagen"])
                avatar.save()
            
        return redirect("Home")
    else:

        formulario = AvatarForm()
        return render(request, "accounts/upload_avatar.html", {"title": "Cargar avatar", "message": "Cargar avatar","form": formulario})