from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now

from .constants import SIZE_CUT_POST
from .models import Post, Category


def filter_posts_by_date(post_manager):
    return post_manager.select_related(
        'author',
        'location',
        'category'
    ).filter(
        pub_date__lte=now(),
        is_published=True,
        category__is_published=True,
    )


def index(request):
    post_list = filter_posts_by_date(Post.objects)
    return render(request, 'blog/index.html',
                  {'post_list': post_list[:SIZE_CUT_POST]})


def category_post(request, category_slug):
    category = get_object_or_404(
        Category,
        is_published=True,
        slug=category_slug
    )

    post_list = filter_posts_by_date(category.posts.all())
    return render(request, 'blog/category.html',
                  {'post_list': post_list,
                   'category': category})


def post_detail(request, post_id):
    post = get_object_or_404(
        filter_posts_by_date(Post.objects),
        pk=post_id
    )

    return render(request, 'blog/detail.html',
                  {'post': post})
