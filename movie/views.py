from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse
from movie.forms import *
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime
#coding:utf-8
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, render
from django.urls import reverse #url逆向解析

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.forms.models import model_to_dict #模型对象转字典

from .oauth_client import OAuth_Base
from .models import OAuth_ex, OAuth_type
from .forms import BindEmail

import time
import uuid

def index(request):
    category_list = Category.objects.order_by('-views')[:5]
    movie_list = Movie.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'movies': movie_list}
    return render(request, 'movie/index.html', context=context_dict)


def search(request):
    movie_list = Movie.objects.order_by('-views')
    context_dict = {'movies': movie_list}
    return render(request, 'movie/search.html', context=context_dict)


def categories(request):
    category_list = Category.objects.order_by('-views')[:5]
    context_dict = {'categories': category_list}
    return render(request, 'movie/categories.html', context=context_dict)


def category(request, category_name_slug):
    context_dict = {}
    try:
        cat = Category.objects.get(slug=category_name_slug)
        movies = Movie.objects.filter(category=cat)
        context_dict['category'] = cat
        context_dict['movies'] = movies
        response = render(request, 'movie/category.html', context=context_dict)
        category_cookie_handler(request, response, cat)
    except Category.DoesNotExist:
        context_dict['title'] = None
        context_dict['movies'] = None
        response = render(request, 'movie/category.html', context=context_dict)
    return response


@login_required
def category_add(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('/movie/')
    else:
        print(form.errors)
    return render(request, 'movie/category_add.html', {'form': form})


@login_required
def movie_add(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except:
        return redirect('/movie/')

    form = MovieForm()
    if request.method == 'POST':
        form = MovieForm(request.POST)
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return redirect(reverse('movie:category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': cat}
    return render(request, 'movie/movie_add.html', context=context_dict)


@login_required
def show_movie(request, movie_name_slug):
    if request.method == 'POST':
        try:
            movie = Movie.objects.filter(slug=movie_name_slug)[0]
            review_content = request.POST.get('review')
            review = Review.objects.get_or_create(user=request.user, movie=movie)[0]
            review.content = review_content
            review.save()
        except :
            print("ERR")

    context_dict = {}
    try:
        movie = Movie.objects.filter(slug=movie_name_slug)[0]
        reviews = Review.objects.filter(movie=movie)
        context_dict['movie'] = movie
        context_dict['reviews'] = reviews
        response = render(request, 'movie/movie.html', context=context_dict)
        movie_cookie_handler(request, response, movie)
    except Category.DoesNotExist:
        context_dict['movie'] = None
        response = render(request, 'movie/movie.html', context=context_dict)
    return response


@login_required
def me(request):
    recommend_lists = RecommendList.objects.filter(user=request.user)
    context_dict = {'recommend_lists': recommend_lists}
    return render(request, 'movie/me.html', context=context_dict)


@login_required
def recommend_list_add(request):
    form = RecommendListForm()
    if request.method == 'POST':
        form = RecommendListForm(request.POST)
        rl = form.save(commit=False)
        rl.user = request.user
        print(rl.title)
        rl = RecommendList.objects.get_or_create(title=rl.title, user=request.user)[0]
        rl.save()

        recommend_lists = RecommendList.objects.filter(user=request.user)
        context_dict = {'recommend_lists': recommend_lists}
        return render(request, 'movie/me.html', context=context_dict)
    else:
        print(form.errors)
    return render(request, 'movie/recommend_list_add.html', {'form': form})


@login_required
def recommend_list(request, recommend_list_slug):
    context_dict = {}
    try:
        rl = RecommendList.objects.get(slug=recommend_list_slug)
        print(rl)
        movies = rl.movie.all()
        context_dict['recommend_list'] = rl
        context_dict['movies'] = movies
        response = render(request, 'movie/recommend_list.html', context=context_dict)
    except Category.DoesNotExist:
        context_dict['recommend_list'] = None
        context_dict['movies'] = None
        response = render(request, 'movie/recommend_list.html', context=context_dict)
    return response


@login_required
def recommend_list_add_movie(request, recommend_list_slug):
    rl = RecommendList.objects.get(slug=recommend_list_slug)

    if request.method == 'POST':
        try:
            movie_title = request.POST.get('movie')
            movie = Movie.objects.filter(title=movie_title)[0]
            rl.movie.add(movie)
            rl.save()
        except:
            print("ERR")

    choices = []
    all_movies = Movie.objects.all()
    already_have = rl.movie.all()

    for cho in all_movies:
        if cho not in already_have:
            choices.append(cho.title)
    print(choices)

    context_dict = {
        'choices': choices,
        'recommend_list': rl,
        'movies': rl.movie.all()
    }
    return render(request, 'movie/recommend_list_add_movie.html', context=context_dict)


def other_user_profile(request, user_name):
    other_user = User.objects.filter(username=user_name)[0]
    other_user_recommend_list = RecommendList.objects.filter(user=other_user)
    print(other_user)
    print(other_user_recommend_list)
    dict_contest = {
        'other_user': other_user,
        'recommend_lists': other_user_recommend_list,
    }
    return render(request, 'movie/other_user.html', context=dict_contest)


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    dict_contest = {'user_form': user_form, 'profile_form': profile_form, 'registered': registered}
    return render(request, 'movie/register.html', context=dict_contest)


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('movie:index'))
            else:
                return HttpResponse("Your movie account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'movie/login.html')


@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('movie:index'))


def movie_cookie_handler(request, response, movie):
    movie_last_visit_cookie = request.COOKIES.get('movie_last_visit', str(datetime.now()))
    movie_last_visit_time = datetime.strptime(movie_last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - movie_last_visit_time).seconds > 30:  # 时间间隔大于30s，views计数
        # add movie views
        movie.views += 1
        movie.save()
        print(movie.views)
        response.set_cookie('movie_last_visit', str(datetime.now()))
    else:
        response.set_cookie('movie_last_visit', movie_last_visit_cookie)


def category_cookie_handler(request, response, category):
    cat_last_visit_cookie = request.COOKIES.get('cat_last_visit', str(datetime.now()))
    cat_last_visit_time = datetime.strptime(cat_last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')
    if (datetime.now() - cat_last_visit_time).seconds > 180:  # 时间间隔大于180s，views计数
        # add category views
        category.views += 1
        category.save()
        response.set_cookie('cat_last_visit', str(datetime.now()))
    else:
        response.set_cookie('cat_last_visit', cat_last_visit_cookie)

def _get_oauth(type_name, state):
    try:
        oauth_type = OAuth_type.objects.get(type_name=type_name)
    except:
        raise Http404

    kw = model_to_dict(oauth_type)
    kw['state'] = state
    return OAuth_Base.Get_OAth(**kw)

def _login_error_response(message, jump_url):
    data = {}
    data['message'] = u'Login error<br>(辅助信息：%s)”' % (message or u"无")
    data['goto_url'] = jump_url
    data['goto_time'] = 3000
    data['goto_page'] = True
    return render_to_response('message.html', data)

def _bind_email_response(open_id, nickname, type_name, jump_url):
    url = '%s?open_id=%s&nickname=%s&oauth_type=%s&state=%s' % (reverse('bind_email'), open_id, nickname, type_name, jump_url)
    return HttpResponseRedirect(url)

def _bind_success_response(jump_url):
    data = {}
    data['goto_url'] = jump_url
    data['goto_time'] = 3000
    data['goto_page'] = True
    data['message'] = u'Bind success'
    return render_to_response('oauth/message.html', data)

def _get_account_from_email(oauth_id, email, open_id, nickname):
    users = User.objects.filter(username=email)

    if users:
        user = users[0]
    else:
        user = User(username=email, email=email)
        pwd = str(uuid.uuid1())
        user.set_password(pwd)
        user.is_active = True
        user.save()

    oauth_type = OAuth_type.objects.get(id=oauth_id)
    oauth_ex = OAuth_ex(user=user, openid=open_id, oauth_type=oauth_type)
    oauth_ex.save()

    if not user.first_name:
        user.first_name = nickname
        user.save()
    return user

def _login_user(request, user):
    setattr(user, 'backend', 'django.contrib.auth.backends.ModelBackend')
    login(request, user)


def oauth_login(request):
    type_name = 'OAuth_Github'
    state = request.GET.get('state')
    oauth = _get_oauth(type_name, state)

    url = oauth.get_auth_url()
    return HttpResponseRedirect(url)


def github_check(request):
    request_code = request.GET.get('code')
    state = request.GET.get('state') or '/'
    oauth = _get_oauth('Github', state)

    try:
        access_token = oauth.get_access_token(request_code)
        time.sleep(0.05)
    except Exception as e:
        return _login_error_response(e.message, state)

    infos = oauth.get_user_info()
    open_id = str(infos.get('id', ''))
    nickname = infos.get('login', '')

    githubs = OAuth_ex.objects.filter(openid=open_id, oauth_type=oauth.id)

    if githubs:
        _login_user(request, githubs[0].user)
        return HttpResponseRedirect(state)
    else:
        try:
            email = oauth.get_email()
        except Exception as e:
            return _bind_email_response(open_id, nickname, oauth.type_name, state)

        user = _get_account_from_email(oauth.id, email, open_id, nickname)

        _login_user(request, user)
        return _bind_success_response(state)

def bind_email(request):
    open_id = request.GET.get('open_id')
    nickname = request.GET.get('nickname')
    oauth_type = request.GET.get('oauth_type')
    state = request.GET.get('state') or '/'
    data = {}

    oauth_types = OAuth_type.objects.filter(type_name = oauth_type)
    if oauth_types.count() > 0:
        oauth_type = oauth_types[0]
        img_url = oauth_type.img
    else:
        data['goto_url'] = state
        data['goto_time'] = 3000
        data['goto_page'] = True
        data['message'] = u'Unexpected login type'
        return render_to_response('message.html',data)

    data['form_title'] = u'Bind User'
    data['submit_name'] = u'　OK　'
    data['form_tip'] = u'Hi, <span class="label label-info"><img src="/%s">%s</span>！Login Succeed, please bind user' % (img_url, nickname)

    if request.method == 'POST':
        form = BindEmail(request.POST)

        if form.is_valid():
            openid = form.cleaned_data['openid']
            nickname = form.cleaned_data['nickname']
            email = form.cleaned_data['email']
            pwd = form.cleaned_data['pwd']

            users = User.objects.filter(email = email)
            if users:
                user = users[0]
                if not user.first_name:
                    user.first_name = nickname
                    user.save()
                data['message'] = u'Successfully bind to %s”' % email
            else:
                user = User(username=email, email=email)
                user.first_name = nickname
                user.set_password(pwd)
                user.is_active = True
                user.save()

                data['message'] = u'Bind success'

            oauth_ex = OAuth_ex(user = user, openid = openid, oauth_type = oauth_type)
            oauth_ex.save()

            user = authenticate(username=email, password=pwd)
            if user is not None:
                login(request, user)

            data['goto_url'] = state
            data['goto_time'] = 3000
            data['goto_page'] = True

            return render_to_response('message.html',data)
    else:
        form = BindEmail(initial={
            'openid': open_id,
            'nickname': nickname,
            'oauth_type_id': oauth_type.id,
            })
    data['form'] = form
    return render(request, 'form.html', data)
