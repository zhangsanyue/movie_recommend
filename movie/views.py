from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponse
from django.template.defaultfilters import title
from movie.forms import *
from django.urls import reverse
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from datetime import datetime


def index(request):
    category_list = Category.objects.order_by('-views')[:5]
    movie_list = Movie.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list, 'movies': movie_list}
    return render(request, 'movie/index.html', context=context_dict)


def search(request):
    # TODO 没有匹配，返回了所有电影
    movie_list = Movie.objects.order_by('-views')
    context_dict = {'movies': movie_list}
    return render(request, 'movie/search.html', context=context_dict)


def categories(request):
    category_list = Category.objects.order_by('-views')
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

        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                cat_name = form.cleaned_data['name']
                cat_image = form.cleaned_data['image']
                cat = Category.objects.get_or_create(name=cat_name, image=cat_image)[0]
                cat.save()
                return redirect('/movie/')
            except:
                return HttpResponse("Err: create category")
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
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            if cat:
                movie_title = form.cleaned_data['title']
                movie_director = form.cleaned_data['director']
                movie_writers = form.cleaned_data['writers']
                movie_stars = form.cleaned_data['stars']
                movie_storyline = form.cleaned_data['storyline']
                movie_image = form.cleaned_data['image']
                movie = Movie.objects.get_or_create(
                    category = cat, 
                    title = movie_title,
                    director = movie_director,
                    writers = movie_writers,
                    stars = movie_stars,
                    storyline = movie_storyline,
                    image = movie_image)[0]
                movie.save()
                
                return redirect(reverse('movie:category', kwargs={'category_name_slug': category_name_slug}))
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': cat}
    return render(request, 'movie/movie_add.html', context=context_dict)


@login_required
def show_movie(request, movie_name_slug):
    if request.method == 'POST':
        try:
            # desc = request.POST.get('desc')
            # star = request.POST.get('star')
            # print(desc)
            # print(star)
            movie = Movie.objects.filter(slug=movie_name_slug)[0]
            review_content = request.POST.get('desc')
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
