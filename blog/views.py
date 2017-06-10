from django.shortcuts import render,get_object_or_404
from django.utils import timezone
from .models import Post
from .forms import PostForm
from django.db.models import Q
from django.shortcuts import redirect, render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    query = request.GET.get("q")
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(text__icontains=query) |
            Q(author__username__icontains=query)
        ).distinct()
    paginator = Paginator(posts , 5)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        queryset = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        queryset = paginator.page(1)
    except EmptyPage:

        # If page is out of range (e.g. 9999), deliver last page of results.
        queryset = paginator.page(paginator.num_pages)

    context = {
            'posts': posts,
            "object_list": queryset,
            "title": " List",
            "page_request_var": page_request_var,
        }


    return render(request, 'blog/post_list.html', context)




def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_delete(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('/')