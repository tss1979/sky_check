from django.urls import reverse_lazy, reverse
from pytils.translit import slugify

from .models import Post
from django.views.generic import DetailView, CreateView, ListView, UpdateView, DeleteView
from blog.services import get_cached_posts


# Create your views here.
class PostCreateView(CreateView):
    model = Post
    fields = ('title', 'content', 'preview',)
    success_url = reverse_lazy('blog:posts')

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()
        return super().form_valid(form)


class PostListView(ListView):
    model = Post

    def get_queryset(self, *args, **kwargs):
        queryset = get_cached_posts().filter(is_published=True)
        return queryset

class PostDetailView(DetailView):
    model = Post

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_count += 1
        self.object.save()
        return self.object

class PostUpdateView(UpdateView):
    model = Post
    fields = ('title', 'content', 'preview',)

    def form_valid(self, form):
        if form.is_valid():
            new_post = form.save()
            new_post.slug = slugify(new_post.title)
            new_post.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('blog:post_detail', args=[self.kwargs.get('pk')])



class PostDeleteView(DeleteView):
    model = Post
    success_url = reverse_lazy('blog:posts')
