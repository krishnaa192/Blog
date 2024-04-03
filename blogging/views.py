from django.http import   HttpResponseRedirect
from calendar import c
from operator import le
from django.shortcuts import get_object_or_404, render,redirect,reverse
from blogging.models import *
from user.models import Profile
from blogging.models import Tags
from django.contrib.auth.decorators import login_required
from .forms import *
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from .utils import Paginationpage,searchProject
from django.db.models import Q
from django.contrib import messages


# Create your views here.

def Home(request):
  tag= Tags.objects.all()
  love=Tags.objects.filter(name="Love")
  work=Blog.objects.order_by('-upload')[:3]
  profile=Profile.objects.all()
  if request.method == "POST":
        email = request.POST["email"]
        new_signup = Subscribe()
        new_signup.email = email
        new_signup.save()
        messages.info(request, 'Thankyou for subscribing!!')

  params={'work':work,'tag':tag,'love':love,'profile':profile}
  return render(request,"index.html", params)

# view for author



def Blogpage(request):
  return render(request,'blogpage.html')


#view for signin page
@login_required(login_url="login")
def Read(request,pk):
    profile=request.user.profile
    tags=Tags.objects.all()
    post=Blog.objects.filter(id=pk).first()
    other =Blog.objects.filter()[:4]
    cmt=Comment.objects.filter(post=post)

    
       
    form = CommentForm(request.POST , request.FILES)
    if request.user.is_authenticated:
      if request.method == "POST":
        if form.is_valid():
          form.instance.user = request.user
          form.instance.post = post
          form.save()
          return redirect('Read',pk=post.id)
    else:
      return redirect('login')
    read={'post':post,'other':other,'profile':profile,'tags':tags,'form':form,'cmt':cmt}
    return render(request,"post.html",read)



@login_required(login_url="login")
def Submit_Form(request):
  profile=request.user.profile
  form=SubmitForm()
  if request.method=='POST':
    # newtags = request.POST.get('newtags').replace(',',  " ").split()
    form=SubmitForm(request.POST,request.FILES)
    if form.is_valid():
      blog=form.save(commit=False)
      blog.Author=profile
      blog.save()
      # for tag in newtags:
      #           tag, created = Tags.objects.get_or_create(name=tag)
      #           blog.tags.add(tag)
      return redirect('/')
  context ={'form':form}
  return render(request,"submitform.html",context)

@login_required(login_url="login")
def update_blog(request,pk):
  profile = request.user.profile
  blog=Blog.objects.get(id=pk)
  form=SubmitForm(instance=blog)
  
  if request.method=='POST':
    # newtags = request.POST.get('newtags').replace(',',  " ").split()

    form=SubmitForm(request.POST, request.FILES,instance=blog)
    if form.is_valid():
      blog=form.save()
    return redirect('Home')
  context ={'form':form,'blog':blog}
  return render(request,"submitform.html",context)

@login_required(login_url="login")
def delete_blog(request,pk):
 profile = request.user.profile
 blog=Blog.objects.get(id=pk)
#  if request.user == blog.user:
 if request.method == 'POST':
    blog.delete()
    return redirect('Home')
 context={'blog':blog}
 return render(request,"blog_delete.html",context)




def all_blog(request):
  search_query,blogs=searchProject(request)
  # custom_ranges,blogs=Paginationpage(request,blogs,4)
  context={'blogs':blogs,'search_query':search_query}
  return render(request,'blogpag.html',context)