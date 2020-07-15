from django.shortcuts import render,HttpResponse,get_object_or_404,HttpResponseRedirect,Http404,redirect
from .models import Post
from .forms import PostForm
from django.contrib import messages

from comments.models import Comments
from django.contrib.contenttypes.models import ContentType
from comments.forms import CommentForm
from django.core.paginator import Paginator
from urllib.parse import quote_plus
from django.utils import timezone
from django.db.models import Q

# Create your views here.
def BlogHome(request):
    today=timezone.now().date()
    queryset=Post.objects.active()#.order_by("-timestamp")
    if request.user.is_staff or  request.user.is_superuser:
        queryset=Post.objects.all()
    query=request.GET.get("q")
    if query:
        queryset=queryset.filter(
            Q(title__icontains=query)|
            Q(content__icontains=query)|
            Q(user__first_name__icontains=query)|
            Q(user__last_name__icontains=query)
            ).distinct()
             
    paginator = Paginator(queryset, 3) # Show 25 contacts per page.
    page_request_variable='rithik'
    page_number = request.GET.get(page_request_variable)
    page_obj = paginator.get_page(page_number)
    context={"title":"List",
             "objects_list":page_obj,
             "page_request_variable":page_request_variable,
             "today":today
    }

  
    return render(request,'blog/bloghome.html',context)
    #return HttpResponse('This is BlogHome.We will keep all the blogpost here')












def BlogPost(request,id=None):
    instance=get_object_or_404(Post,id=id)
    if instance.draft or instance.published > timezone.now().date():
        if not request.user.is_staff or not request.user.is_superuser:
           raise Http404
    share_string=quote_plus(instance.content)
    
    comments=instance.comments#Comments.objects.filter_by_instance(instance)
    initial_data={
        "content_type":instance.get_content_type,
        "object_id":instance.id
    }
    form=CommentForm(request.POST or None,initial=initial_data)
    if form.is_valid():
        c_type=form.cleaned_data.get("content_type")
        content_type=ContentType.objects.get(model=c_type)
        #content_type = form.cleaned_data.get("content_type")
        obj_id=form.cleaned_data.get("object_id")
        content_data=form.cleaned_data.get("content")
        new_comment,created=Comments.objects.get_or_create(
                                    user=request.user,
                                    content_type=content_type,
                                    object_id=obj_id,
                                    content=content_data
        )
        
        if created:
            print('yeah it worked')

    context={"title":instance.title,
             "instance":instance,
             "share_string":share_string,
             "comments":comments,
             "comment_form":form
    }
    return render(request,'blog/blogpost.html',context)
    #return HttpResponse(f'This is blog{slug}')    



def BlogPostCreate(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    form=PostForm(request.POST or None,request.FILES or None)
    context={"form":form
    }
    if form.is_valid():
        instance=form.save(commit=False)
        instance.user=request.user
        print (form.cleaned_data.get("title"))
        instance.save()
        messages.success(request,"Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())

    else:
        messages.error(request,"Post Cannot Be Created")
    return render(request,'blog/BlogPostCreate.html',context)
    #return HttpResponse('This is BlogHome.We will keep all the blogpost here'



def BlogPostUpdate(request,id=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404

    instance=get_object_or_404(Post,id=id)
    form=PostForm(request.POST or None,request.FILES or None,instance=instance)
    context={"form":form,
            "title":instance.title,
             "instance":instance
    }
    if form.is_valid():
        instance=form.save(commit=False)
        instance.save()
        messages.success(request,"Successfully Updated")
        return HttpResponseRedirect(instance.get_absolute_url())
    return render(request,'blog/BlogPostCreate.html',context)
    #return HttpResponse('This is BlogHome.We will keep all the blogpost here'



def BlogPostDelete(request,id=None):
    if not request.user.is_staff or not request.user.is_supeuser:
        raise Http404
    instance=get_object_or_404(Post,id=id)
    instance.delete()
    messages.success(request,"Successfully Deleted")
    return HttpResponseRedirect('http://127.0.0.1:8000/blog/')











from django.contrib.auth import(
    authenticate,
    get_user_model,
    login,
    logout,
)
# Create your views here.
from .forms import UserLoginForm,UserRegisterForm


def login_view(request):
    print(request.user.is_authenticated)
    title="Login"
    form=UserLoginForm(request.POST or None)
    if form.is_valid():
        username=form.cleaned_data.get("username")
        password=form.cleaned_data.get("password")
        user=authenticate(username=username,password=password)
        login(request,user)
        print(user.is_authenticated)
        return redirect('http://127.0.0.1:8000/blog')
        
    return render(request,"blog/loginform.html",{"form":form,"title":title})


def register_view(request):
    title="Register"
    form=UserRegisterForm(request.POST or None)
    if form.is_valid():
        user=form.save(commit=False)
        password=form.cleaned_data.get("password")
        user.set_password(password)
        user.save()

        new_user=authenticate(username=user.username,password=password)
        login(request,new_user)
        #redirect
        return redirect('http://127.0.0.1:8000/blog')

    context={
        'form':form,
        'title':title
    }
    return render(request,"blog/loginform.html",context)

def logout_view(request):
    logout(request)
    return render(request,"home/home.html",{})