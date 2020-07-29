from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import CommentForm
from taggit.models import Tag
from django.utils.safestring import mark_safe 
from accounts.models import Profile
from django import forms
import math, random





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

    paginator = Paginator(objects, 10)  
    page = request.GET.get('page')    
    total_pages = range(1, math.ceil(objects.count() / 10) + 1)

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
            new_comment.post = post
             
            # The post field under Comment model has not been field 
            # so we add the current post we are in  to the post field
            new_comment.name = request.user.username 
            new_comment.email = request.user.email
            new_comment.photo = request.user.profile.photo

            new_comment.save()  
        comment_form = CommentForm()
            
    else:
        comment_form = CommentForm()

    # for static image 
    # image_route = "{% static 'profile_pics/3.png' %}"
    
    # image_route = """<img  src= "/static/profile_pics/3.png" alt="John Doe" class="rounded-circle  mr-1" style="width:40px; height:40px;">"""
    # image_route_list = image_route.split('3', 1)
    # image_route_list[0] = image_route_list[0] + str(random.randint(1, 3))
    # image_route = ''.join(image_route_list)
    # image_route = mark_safe(image_route)

    # profile = Profile.objects.list_values('photo', flat=True).filter(user=request.user.username)
    # profile = profile[0]
    
    
    return render(request, 'thoughts/pages/detail_display.html', {
                                                                  'posts': posts,
                                                                  'tag': tag,
                                                                  'post': post,
                                                                  'comments': comments,
                                                                  'comment_form': comment_form,
                                                                  'new_comment': new_comment,
                                                                  'section': 'blog',
                                                                #   'profile_pic': image_route
                                                                  }
    )
