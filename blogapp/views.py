from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from blogapp.forms import CommentForm, ContactForm
from blogapp.models import Category, Post
from django.contrib import messages
from taggit.models import Tag
from django.http import HttpResponse


def home_page(request):
    all_posts = Post.objects.all()
    all_cat = Category.objects.all()
    all_tags = Tag.objects.all()
    trending_posts = Post.objects.all().order_by('?')[0:5]
    paginator = Paginator(all_posts, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'all_posts': page_obj,
        'all_cats': all_cat,
        'all_tags': all_tags,
        'pagination': page_obj,
        'trending_posts': trending_posts,
    }
    return render(request, 'home.html', context)


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    all_cat = Category.objects.all()
    category = post.category
    related_posts = Post.objects.filter(category=category).exclude(slug=slug)
    all_comments = post.comments.all()

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
    else:
        form = CommentForm()

    context = {
        'post': post,
        'related_posts': related_posts,
        'all_cats': all_cat,
        'cform': form,
        'all_comments': all_comments,
    }
    return render(request, 'postdetail.html', context)


def tag_posts(request, tagslug):
    tag = get_object_or_404(Tag, slug=tagslug)
    posts = Post.objects.filter(tags__in=[tag])
    return render(request, 'tag_results.html', {'posts': posts, 'tags': tag})


def category(request, catslug):
    query = Category.objects.get(slug=catslug)
    posts = Post.objects.filter(category=query)
    all_cat = Category.objects.all()
    context = {
        'cats_posts': posts,
        'all_cats': all_cat,
        'category_search': query,
    }

    return render(request, 'category_results.html', context)


def search(request):
    query = request.GET['query']
    search_result = Post.objects.filter(title__icontains=query)
    all_cat = Category.objects.all()
    context = {
        'search_query': query,
        'search_results': search_result,
        'all_cats': all_cat,

    }
    if not search_result:
        context['no_posts_found'] = True

    return render(request, 'search_results.html', context)


def about_page(request):
    return render(request, 'about.html')


def contact_page(request):
    if request.method == 'POST':
        cform = ContactForm(request.POST)
        if cform.is_valid():
            cform.save()
            messages.info(request, 'Mail sent succesfully')
            cform = ContactForm()

    else:
        cform = ContactForm()

    return render(request, 'contact_form.html', {'form': cform})


def robots_txt(request):
    lines = [
        "User-Agent: *",
        "Disallow: /admin/",
        "Sitemap : http://127.0.0.1:8000/sitemap.xml"

    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


def custom_404_page(request, exception):
    return render(request, '404.html', {}, status=404)
