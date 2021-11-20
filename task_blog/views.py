from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.views import generic

from .forms import CommentForm, RegisterForm
from .models import Comment, Post

User = get_user_model()


class RegisterFormView(generic.FormView):
    template_name = 'registration/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.save()

        username = self.request.POST['username']
        password = self.request.POST['password1']

        user = authenticate(username=username, password=password)
        login(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class UserEditView(LoginRequiredMixin, generic.UpdateView):
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    template_name = 'registration/update_user.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        user = self.request.user
        return user


class HomePageView(generic.TemplateView):
    template_name = 'index.html'


class PostCreate(LoginRequiredMixin, generic.CreateView):
    model = Post
    fields = ['title', 'brief_description', 'full_description']
    template_name = 'create_post.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.slug = slugify(post.title)
        post.save()
        self.object = post
        return HttpResponseRedirect(self.get_success_url())


class PostList(generic.ListView):
    model = Post
    paginate_by = 10
    template_name = 'blog/post_list.html'

    def get_queryset(self):
        return Post.objects.all().filter(posted=True)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, posted=True)
    comments = Comment.objects.all().filter(post=post)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comm = Comment()
            comm.username = form.cleaned_data['username']
            comm.text = form.cleaned_data['text']
            comm.post = post
            comm.save()
            return HttpResponseRedirect(reverse('post_detail', args=(post.id,)))

    else:
        initial = {'username': request.user.username}
        form = CommentForm(initial=initial)

    context = {'form': form, 'post': post, 'comments': comments}

    return render(request, 'blog/post_detail.html', context)


def user_detail(request, pk):
    user = get_object_or_404(User, pk=pk, is_staff=False)
    posts = Post.objects.filter(author=user).filter(posted=True)
    self_posts = request.user.username == user.username

    context = {
        'page_obj': posts,
        'user': user,
        'self_posts': self_posts
    }
    return render(request, 'blog/user_detail.html', context)
