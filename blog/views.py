from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_GET

from .forms import CommentForm
from .models import Category, Post


def post_list(request, category_slug=None):
    posts = Post.published.select_related("author", "category")
    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        posts = posts.filter(category=category)

    query = request.GET.get("q", "").strip()
    if query:
        posts = posts.filter(Q(title__icontains=query) | Q(body__icontains=query))

    page = Paginator(posts, 5).get_page(request.GET.get("page"))
    return render(
        request,
        "blog/post_list.html",
        {"page": page, "category": category, "categories": Category.objects.all(), "q": query},
    )


def post_detail(request, slug):
    post = get_object_or_404(Post.published.select_related("author", "category"), slug=slug)
    comments = post.comments.filter(approved=True)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect(post.get_absolute_url())  # Post/Redirect/Get
    else:
        form = CommentForm()

    return render(
        request, "blog/post_detail.html", {"post": post, "comments": comments, "form": form}
    )


# --- tiny read-only JSON API -------------------------------------------------

def _serialize(post: Post) -> dict:
    return {
        "id": post.id,
        "title": post.title,
        "slug": post.slug,
        "author": post.author.get_username(),
        "category": post.category.name if post.category else None,
        "published_at": post.published_at.isoformat(),
        "url": post.get_absolute_url(),
    }


@require_GET
def api_posts(request):
    posts = Post.published.select_related("author", "category")[:50]
    return JsonResponse({"results": [_serialize(p) for p in posts]})


@require_GET
def api_post_detail(request, slug):
    post = get_object_or_404(Post.published.select_related("author", "category"), slug=slug)
    data = _serialize(post) | {"body": post.body}
    return JsonResponse(data)
