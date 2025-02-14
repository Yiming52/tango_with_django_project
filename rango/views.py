from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm

from datetime import datetime

def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    # Handle the visit count via session
    visitor_cookie_handler(request)
    # Add 'visits' to the context so we can display it in the template if desired
    context_dict['visits'] = request.session['visits']

    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    # Demonstrate how you could check if a test cookie worked (optional)
    if request.session.test_cookie_worked():
        print("TEST COOKIE WORKED!")
        request.session.delete_test_cookie()

    # Handle visits just like in index()
    visitor_cookie_handler(request)
    visits = request.session['visits'] if 'visits' in request.session else 1

    return render(request, 'rango/about.html', context={'visits': visits})

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['category'] = category
        context_dict['pages'] = pages
    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)

@login_required
def add_category(request):
    form = CategoryForm()
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect(reverse('rango:index'))
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect(reverse('rango:index'))

    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()
            return redirect('rango:show_category', category_name_slug=category_name_slug)
        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)

def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST, request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            # Hash the password
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'rango/register.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'rango/login.html')

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))


# ============ Helper function: using Session to track visits ============
def visitor_cookie_handler(request):
    """
    Uses session data to track the number of visits and the last visit time.
    In this version, the visit count increments if more than THRESHOLD seconds have passed.
    """
    THRESHOLD_SECONDS = 10  # Change this value to your desired interval in seconds
    
    visits = int(request.session.get('visits', '1'))
    last_visit_str = request.session.get('last_visit', str(datetime.now()))

    last_visit_time = datetime.strptime(last_visit_str, '%Y-%m-%d %H:%M:%S.%f')
    
    # Check if the difference in seconds is greater than our threshold
    if (datetime.now() - last_visit_time).total_seconds() > THRESHOLD_SECONDS:
        visits += 1
        request.session['last_visit'] = str(datetime.now())
    else:
        # If not over the threshold, just update last_visit without incrementing
        request.session['last_visit'] = last_visit_str

    request.session['visits'] = visits

