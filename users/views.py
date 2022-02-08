"""Users views."""
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse

"""Exceptions"""
from django.db.utils import IntegrityError

"""Models"""
from django.contrib.auth.models import User
from users.models import Profile
from posts.models import Post
"""Forms"""
from users.forms import ProfileForm, SignupForm

# Create your views here.

class UserDatailView(LoginRequiredMixin,DeleteView):#Me ayuda a redirigir el usuario preciso al que esta logueado y ver su inf personal 

    login_url = 'users:login'
    template_name = 'users/detail.html'
    slug_field= 'username'
    slug_url_kwarg= 'username'
    queryset=User.objects.all()
    context_object_name='user'

    def get_context_data(self, **kwargs): #Me redirige a la imformacion propia de casa user al presionar en perfil
        """Add user's posts to context"""
        context = super().get_context_data(**kwargs)
        user= self.get_object()
        context['posts'] = Post.objects.filter(user=user).order_by('-created')
        return context

@login_required
def update_profile(request):
    """"update userr's profile"""

    profile= request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data

            profile.website = data ['website']
            profile.phone_number = data ['phone_number']
            profile.biography = data ['biography']
            if data['picture']:
                profile.picture = data ['picture']
            profile.save()

            url = reverse('users:detail', kwargs={'username':request.user.username})
            return redirect(url)  
    else:
        form = ProfileForm()

    return render(
        request = request,
        template_name= 'users/update_profile.html',
        context={
            'profile': profile,
            'user': request.user,
            'form': form,
        }
    )



def login_view(request):
    if request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)
        if user:
            login(request, user)
            return redirect('posts:feed')#redirige al feed de cada usuario
        else:
            return render(request, 'users/login.html', {'error':'invalid user name or password'})#responde con la misma pagina y manda el diccionario
        
    return render(request, 'users/login.html')


def signup(request):
    """Sign up view"""
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')
    else:
        form = SignupForm()
    
    return render(
        request=request,
        template_name='users/signup.html',
        context = {'form':form}
    )
        

@login_required   #Forzamos que halla un logout
def logout_view(request):
    """Loougt a user """
    logout(request)
    return redirect('users:login')#redirijimos a login

