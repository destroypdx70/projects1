# Django
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy

# Local
from posts.models import Post
from posts.forms import PostForm


class PostFeedView(LoginRequiredMixin, ListView):

    template_name = "posts/feed.html"
    model = Post
    ordering = ("-created",)
    paginate_by = 30
    context_object_name = "posts"



class PostDetailView(LoginRequiredMixin, DetailView):

    template_name = "posts/detail.html"
    queryset = Post.objects.all()
    context_object_name = "post"


class CreatePostView(LoginRequiredMixin, CreateView):

    template_name = "posts/new.html"
    form_class = PostForm
    success_url = reverse_lazy("posts:feed")

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        context["profile"] = self.request.user.profile
        return context




@login_required
def list_posts(request):

    post = Post.objects.all().order_by("-created")
    return render(
        request,
        template_name="posts/feed.html", 
        context={
            "post": post
        }
    )

"""
@login_required
def create_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("posts:feed")
        
    else:
        form = PostForm()

    return render(request, "posts/new.html", {
        "form": form,
        "user": request.user,
        "profile": request.user.profile
    })
"""