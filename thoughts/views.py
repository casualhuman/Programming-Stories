from django import forms
from django.contrib.auth.models import User 
from django.utils.safestring import mark_safe  
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger 
import math, random
from .models import Post
from taggit.models import Tag
from .forms import CommentForm
from accounts.models import Profile


def list_display(request, tag_slug=None):
    # Global Variables 
    # enables display in the detail_display; the tags and use the paginator correctly 
    global tag
    global posts

    objects = Post.published.all()
    tag = None 

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        objects = objects.filter(tags__in=[tag])   # find if the tag selected is in any of the objects returned previously

    paginator = Paginator(objects, 6)  
    page = request.GET.get('page')    
    total_pages = range(1, math.ceil(objects.count() / 6) + 1)

    try:
        posts = paginator.page(page)    # posts that should be in the current page 

    except PageNotAnInteger:
        posts = paginator.page(1)  # If 'page' does not return an integer then go to page 1

    except EmptyPage:
        posts = paginator.page(paginator.num_pages) # returns the last page 

    
    # differentiate the odd and even index posts  
    # so the list_display page can display them in grid format 
    posts_list = [post for post in posts]
    even_index_posts = [post for post in posts_list if posts.index(post) % 2 == 0]
    odd_index_posts = [post for post in posts_list if posts.index(post) % 2 == 1]

    
    return render(request, 'thoughts/pages/list_display.html', {'posts': posts,
                                                                'page': page,
                                                                'total_pages': total_pages,
                                                                'tag': tag,
                                                                'section': 'blog',
                                                                'even_index_posts': even_index_posts,
                                                                'odd_index_posts': odd_index_posts
                                                               }
    )


    
def detail_display(request, year, month, day, post_slug, tag_slug=None):
    list_display(request) # to make use of the posts and tag variables 
    new_comment = None 
    

    post = get_object_or_404(Post,
                                status = 'publish',
                                publish__year = year,
                                publish__month = month,
                                publish__day = day,
                                slug = post_slug

    )
    
    comments = post.comments.filter(active=True)

    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False) 
             
            # fill the remaining fields that are empty after submission
            new_comment.post = post
            new_comment.email = request.user.email
            user = User.objects.get(username=request.user.username) # get the username from user db using the request given username
            new_comment.user_name = user
            
            new_comment.save()  
            
    else:
        comment_form = CommentForm()

    
    return render(request, 'thoughts/pages/detail_display.html', {
                                                                  'posts': posts,
                                                                  'tag': tag,
                                                                  'post': post,
                                                                  'comments': comments,
                                                                  'comment_form': comment_form,
                                                                  'new_comment': new_comment,
                                                                  'section': 'blog',
                                                                  }
    )
