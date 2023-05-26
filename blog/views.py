from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView, DeleteView
from django.contrib.auth.models import User
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

# Send and administrates the user experience with the Blog posts.


def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

# Administrates the View of the posts in the home page.


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-datePost']
    paginate_by = 3

# Administrates the View of the posts in the User posts page.


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-datePost')

# Administrates the View of the detail in a specific post.


class PostDetailView(DetailView):
    model = Post

# Set up the creation of Posts page.


def create_post(request):
    if request.method == 'GET':
        return render(request, 'blog/post_form.html')

    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        if not title:
            messages.error(request, 'Amount is required')
        Post.objects.create(author=request.user, title=title, content=content)
        messages.success(request, 'New expense added')

        return redirect('blog-home')

# Set up the update posts page.


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ('title', 'content')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

# Set up the deletion of posts page.


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = "/"

    def test_func(self):
        post = self.get_object()

        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
