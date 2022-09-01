import imp
from Config import settings
from django.http import HttpResponseRedirect
from multiprocessing import context
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login,logout, authenticate
from .models import News, Comments, Contact
from django.db.models import Q

# Create your views here.
def home(request):
    context = {
        
    }
    return render(request, 'home.html', context)

def register(request):
    if request.method == "POST":
        if request.POST['username'] != '' and request.POST['email'] != '' and request.POST['password'] != '':
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            repeat_password = request.POST['repeat_password']
            if password == repeat_password:
                if User.objects.filter(username=username).exists():
                    messages.info(request, 'Bunday username mavjud')
                    return redirect('register')
                elif User.objects.filter(email=email).exists():
                    messages.info(request, 'Bunday e-mail mavjud')
                    return redirect('register')
                else:
                    user = User.objects.create_user(
                        username = username,
                        password = password,
                        email = email
                    )
                    user.save()
                    return redirect('loginuser')
            else:
                messages.info(request, 'Coniform parol to`g`ri kelmayabdi')
                return redirect('register')
        else:
            messages.info(request, 'Ma`lumot kiritilmadi')
    context = {
        
    }
    return render(request, 'login/register.html', context)

def loginuser(request):
    if request.method == "POST":
        next = request.POST.get('next', '/')
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Bunday username yo`q !!')
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            # return redirect('home')
            return HttpResponseRedirect(next)
        else:
            messages.error(request, 'Username yoki parol xato')
    context = {}
    return render(request, 'login/login.html', context)

def logoutuser(request):
    next = request.GET.get('next', '/')
    logout(request)
    return redirect(next)

def news(request):
    news = News.objects.all()
    recent_news = News.objects.all().order_by('-created_at')
    paginator = Paginator(news, 9)
    page_number = request.GET.get('page')

    q = request.GET.get('search')
    if request.GET.get('search') is not None:
        news = News.objects.filter(
            Q(title__icontains = q)|
            Q(subtitle__icontains = q)|
            Q(body__icontains = q)
        )
        paginator = Paginator(news, 6)
        page_obj = paginator.get_page(page_number)
        news_count = news.count()
    else:
        page_obj = paginator.get_page(page_number)
        news_count = None

    context ={
    # 'news': news
    'page_obj': page_obj, 
    'recent_news': recent_news,
    'news_count': news_count
    }
    return render(request, 'news.html', context)

def news_detail(request, pk):
    details = News.objects.get(id=pk)
    recent_news = News.objects.all().order_by('-created_at')
    comments = Comments.objects.filter(news=details).order_by('-created_at')
    # parent = Comments.objects.filter(parent__isnull=False)
    print(type(pk))

    if request.method == "POST":
        if request.POST.get('reply') is not None:
            reply_id = str(request.POST.get('reply'))
            print(type(reply_id))
            reply = comments.get(id=reply_id)
            com = Comments.objects.create(
                user = request.user,
                news = details,
                body = request.POST.get('body'),
                parent = reply
            )
            com.save()
            print(reply)
            return redirect('news_detail', pk = details.id)
        else:
            Comments.objects.create(
                user = request.user,
                news = details,
                body = request.POST.get('body')
            )
            return redirect('news_detail', pk = details.id)

    context = {
        'details': details,
        'recent_news': recent_news,
        'comments': comments
    }
    return render(request, 'news_detail.html', context)

def contact_form(request):

    if request.method == "POST":
        if request.user.is_authenticated:
            Contact.objects.create(
                username = request.user.username,
                email = request.user.email,
                subject = request.POST['subject'],
                message = request.POST['message']
            )
            messages.info(request, 'Xabaringiz yuborildi tez orada bog`lanamiz, rahmat !!!')
        else:
            Contact.objects.create(
                username = request.POST['username'],
                email = request.POST['email'],
                subject = request.POST['subject'],
                message = request.POST['message']
            )
            messages.info(request, 'Xabaringiz yuborildi tez orada bog`lanamiz, rahmat !!!')

    return render(request, 'contact_form.html')
