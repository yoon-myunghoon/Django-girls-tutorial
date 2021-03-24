from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm, UserRegisterForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from django.urls import reverse_lazy

# User


class UserCreateView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'user/register.html'
    success_url = reverse_lazy('login')


# def register(request):
#     if request.method == 'POST':
#         form = UserRegisterForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = UserRegisterForm()
#     return render(request, 'user/register.html', {'form': form})


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/user_detail.html'
    # slug_field = "username"
    context_object_name = 'user'


# @login_required
# def user_detail(request):
#     user = get_object_or_404(User, username=request.user.username)
#     return render(request, 'user/user_detail.html', {'user': user})


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    # slug_field = "username"
    template_name = 'user/profile.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return is_users(self.get_object(), self.request.user)

    def get_success_url(self):
        return reverse_lazy('user-detail', kwargs={'pk': self.get_object().pk})


# @login_required
# def profile(request):
#     if request.method == 'POST':
#         form = UserUpdateForm(request.POST, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return redirect('user-detail')
#     else:
#         form = UserUpdateForm(instance=request.user)
#     return render(request, 'user/profile.html', {'form': form})


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'user/user_delete.html'
    context_object_name = 'post'
    # slug_field = "username"

    def test_func(self):
        return is_users(self.get_object(), self.request.user)

    def get_success_url(self):
        return reverse('post_list')


# @login_required
# def user_remove(request):
#     user = get_object_or_404(User, username=request.user.username)
#     user.delete()
#     return redirect('post_list')


# Post

def is_users(post_user, logged_user):
    return post_user == logged_user


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


# def post_list(request):
#     posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
#     return render(request, 'blog/post_list.html', {'posts': posts})


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


# def post_detail(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     return render(request, 'blog/post_detail.html', {'post': post})


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'text']
    template_name = 'blog/post_edit.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})


# @login_required()
# def post_new(request):
#     if request.method == "POST":
#         form = PostForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'text']
    template_name = 'blog/post_edit.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return is_users(self.get_object().author, self.request.user)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.object.pk})


# @login_required()
# def post_edit(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = PostForm(request.POST, instance=post)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm(instance=post)
#     return render(request, 'blog/post_edit.html', {'form': form})


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    context_object_name = 'post'

    def test_func(self):
        return is_users(self.get_object().author, self.request.user)

    def get_success_url(self):
        return reverse('post_list')


# @login_required()
# def post_remove(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.delete()
#     return redirect('post_list')


class PostDraftListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'blog/post_draft_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).filter(published_date__isnull=True).order_by('-created_date')


# @login_required()
# def post_draft_list(request):
#     posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
#     return render(request, 'blog/post_draft_list.html', {'posts': posts})


class PostPublishView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post

    def test_func(self):
        return is_users(self.get_object().author, self.request.user)

    def get(self, request, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        post.publish()
        return redirect('post_detail', pk=post.pk)


# @login_required()
# def post_publish(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.publish()
#     return redirect('post_detail', pk=pk)


# Comment

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['text']
    template_name = 'blog/add_comment_to_post.html'

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs['pk']})


# @login_required()
# def add_comment_to_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.author = request.user
#             comment.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = CommentForm()
#     return render(request, 'blog/add_comment_to_post.html', {'form': form})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['text']
    template_name = 'blog/add_comment_to_post.html'

    def form_valid(self, form):
        form.instance.post = get_object_or_404(Comment, pk=self.kwargs['pk']).post
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return is_users(self.get_object().author, self.request.user)

    def get_success_url(self):
        post_pk = get_object_or_404(Comment, pk=self.kwargs['pk']).post.pk
        return reverse('post_detail', kwargs={'pk': post_pk})


# @login_required
# def comment_edit(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     if request.method == "POST":
#         form = CommentForm(request.POST, instance=comment)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.author = request.user
#             comment.save()
#             return redirect('post_detail', pk=comment.post.pk)
#     else:
#         form = CommentForm(instance=comment)
#     return render(request, 'blog/add_comment_to_post.html', {'form': form})


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_delete.html'
    context_object_name = 'comment'

    def test_func(self):
        return is_users(self.get_object().author, self.request.user)

    def get_success_url(self):
        post_pk = get_object_or_404(Comment, pk=self.kwargs['pk']).post.pk
        return reverse('post_detail', kwargs={'pk': post_pk})


# @login_required
# def comment_remove(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     comment.delete()
#     return redirect('post_detail', pk=comment.post.pk)


class CommentApproveView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment

    def test_func(self):
        return is_users(self.get_object().author, self.request.user)

    def get(self, request, **kwargs):
        comment = get_object_or_404(Comment, pk=self.kwargs['pk'])
        comment.approve()
        return redirect('post_detail', pk=comment.post.pk)


# @login_required
# def comment_approve(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     comment.approve()
#     return redirect('post_detail', pk=comment.post.pk)
