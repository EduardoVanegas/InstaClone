#django posts
#from django.http import HttpResponse
from django.db.models import query
from django.db.models.query import QuerySet
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.detail import DetailView
import posts
#Forms
from posts.forms import PostForm
#Models
from posts.models import Post


#@login_required
# def list_posts(request):
#     posts = Post.objects.all().order_by('-created')
#     return render(request, 'posts/feed.html', {'posts': posts})
class PostsFeedView(LoginRequiredMixin, ListView):
    """Return all published posts"""
    template_name= 'posts/feed.html'
    model=Post
    ordering=('-created')
    paginate_by=10
    context_object_name='posts'

class PostDetailView(LoginRequiredMixin, DetailView):
    """Return Post Detail"""
    template_name= 'posts/detail.html'
    queryset = Post.objects.all()
    contex_object_name= 'post'

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('posts:feed')
    else:
        form = PostForm()

    return render(
        request=request,
        template_name='posts/new.html',
        context={
            'form':form,
            'user':request.user,
            'profile':request.user.profile
        }

    )
