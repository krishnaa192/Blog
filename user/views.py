
from django.shortcuts import get_object_or_404, render
from .models import *
from django.shortcuts import redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import CustomUserCreationForm,ProfileForm,CreateAccountForm
from blogging.models import *
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .utils  import searchAuthors, PaginationProfile
from django.db.models import Q




def authors(request):
    search_authors= ''
    if request.GET.get('search_authors'):
        search_authors = request.GET.get('search_authors')
    profiles = Profile.objects.filter(username__icontains=search_authors) 
    print(profiles)
    # profiles, search_query = searchAuthors(request)
    # custom_ranges, author = PaginationProfile(request, author, 3)
    a_pms={'profiles':profiles,'search_query':search_authors}
    return render(request, "author.html" , a_pms)

def loginuser(request):
    page= login
    if request.user.is_authenticated:
        return redirect("Home")
    if request.method == 'POST':
        username = request.POST['username'] 
        password =request.POST['password']
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "username does not exist")
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('Home')
        else:
            messages.error(request,"User not found")
    return render(request, 'newsignin.html')

def follower_count(request):
    if request.method == 'POST':
        value = request.POST['value']
        user = request.POST['user']
        follower = request.POST['follower']
        if value == 'follow':
            follow = Follow.objects.create(user=user, follower=follower)
            follow.save()
        
        return redirect('/?user'+user)

def logoutuser(request):
    logout(request)
    return redirect('login')


def signup(request):
    form = CustomUserCreationForm()
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'User account was created!')
            login(request, user)
            return redirect('create_profile')
        else:
            messages.success(
                request, 'An error has occurred during registration')
    return render(request, 'signup.html', {'form': form})

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = "home.html" 

def userProfile(request, pk):
    profile = get_object_or_404(Profile, id=pk)
    loggged = get_object_or_404(Profile, user=request.user)
    blogs=Blog.objects.filter(Author=profile.id)
    follow=Follow.objects.filter(follower=profile.id)
    follower_coun=len(follow)
    posts=len(blogs)
    context = {'profiles': profile,'blogs':blogs,'loggged':loggged,'follower_coun':follower_coun,'posts':posts}
    return render(request, 'user-profile.html', context)


@login_required(login_url="login")
def profile(request,pk):
    profile=Profile.objects.get(user=request.user)
    follow=Follow.objects.filter(follower=profile.id)
    val=len(follow)
    print(val)
   
    post=Blog.objects.filter(id=pk).first()
    blogs=Blog.objects.filter(Author=profile).order_by('upload')
    comments=Comment.objects.filter(post=post)
    cmt=len(comments)
    posts=len(blogs)
    context={ 'profile': profile,'blogs':blogs,'posts':posts,'cmt':cmt,'follow':follow,'val':val}
    return render(request, 'profile1.html',context)



def authors(request):
    author=Profile.objects.all()
    a_pms={'author':author}
    return render(request, "author.html",a_pms)

@login_required(login_url="login")
def edit_profile(request):
    profile=request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form=ProfileForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
        return redirect('profile')
    context ={'form': form}
    return render(request, 'edit_profile.html',context)


@login_required(login_url="login")
def create_profile(request):
    profile=request.user.profile
    form=CreateAccountForm(instance=profile)
    if request.method == 'POST':
        form=CreateAccountForm(request.POST,request.FILES,instance=profile)
        if form.is_valid():
            form.save()
        return redirect('Home')
    context={'form':form}
    return render(request, 'create_profile.html',context)
   

