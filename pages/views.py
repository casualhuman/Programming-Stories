from django import forms 
from django.shortcuts import render
from django.core.mail import send_mail 
from django.utils.safestring import mark_safe
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from .forms import ReportProblemForm, SearchForm, ReportProblemFormLoggedInUser
from .models import ReportProblem
from thoughts.models import Post
from accounts.views import EmailListForm
from accounts.models import Profile


def home_page_view(request):
    posts = Post.published.all().order_by('-publish')[:5]

    #create 5 different items for distinct display in the home_page
    # the homepage would always only display 5 recent posts 
    # posts = [post for post in posts]
    # post_1 = posts[0]
    # post_2 = posts[1]
    # post_3 = posts[2]
    # post_4 = posts[3]
    # post_5 = posts[4]


    context = {
        'section': 'home',
        'posts': posts,
        # 'post_1': post_1,
        # 'post_2': post_2,
        # 'post_3': post_3,
        # 'post_4': post_4,
        # 'post_5': post_5,
    }
        
    return render(request, 'pages/page/home.html', context=context)
    


def about_page_view(request):
    return render(request, 'pages/page/about.html', {'section': 'about'})


def report_problem(request):
    """
        The request.user.username looks if the user is logged in or not, if that is true, 
        then the user does not need to enter name, and email again as they would be done automatically and 
        a different form is used for logged in an not logged in users 

    """

    sent = False 

    if request.method == 'POST':
        if request.user.username:
            report_form = ReportProblemFormLoggedInUser(request.POST)
        else:
            report_form = ReportProblemForm(request.POST)  

        if report_form.is_valid():
            report_form = report_form.save(commit=False)
            
            
            if request.user.username:
                report_form.name = request.user.username
                report_form.email = request.user.email 

            report_form.save()

            # # Send email to developer about problem also 
            # subject = f"{ report_form.name } Reported a bug in randomthoughts.com"

            # body = f"""
            #             name: { report_form.name }
            #             email: { report_form.email }
            #             problem: { report_form.problem }

            #         """

            # send_mail(subject, body, report_form.email, ['abdulrahimjallohaarj@gmail.com',])
        
            sent = True
    
    else:
        if request.user.username:
            report_form = ReportProblemFormLoggedInUser()
        else:
            report_form = ReportProblemForm()

    return render(request, 'pages/page/rproblem.html', {'report_form': report_form,
                                                         'sent': sent})


def search_page(request):
    search_form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:  
        search_form = SearchForm(request.GET)
        if search_form.is_valid():
            query = search_form.cleaned_data['query']
            
            search_vector = SearchVector('title', 'body', 'tags')
            search_query = SearchQuery(query)

            results = Post.published.annotate(
                search=search_vector,
                search_rank=SearchRank(search_vector, search_query)
            ).filter(search=query).order_by('-search_rank')

    return render(request, 'pages/page/search.html', {
                                                    'search_form': search_form,
                                                    'query': query,
                                                    'results': results
                                                    }
    )
