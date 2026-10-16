from django.urls import path

from . import views

app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("category/<slug:category_slug>/", views.post_list, name="post_by_category"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    path("api/posts/", views.api_posts, name="api_posts"),
    path("api/posts/<slug:slug>/", views.api_post_detail, name="api_post_detail"),
]
