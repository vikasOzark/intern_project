import profile
from unicodedata import category
from xml.dom.minidom import parseString
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfileModel, BlogModel
from django.contrib import messages
# import Q
from django.db.models import Q
# Create your views here.

def authentication(request):
    method = request.method

    if method == 'POST':
        type = request.POST['type_auth']
        print(type)
        if type == 'type_login':
            print('in login')
            username_login = request.POST['username_login']
            password_login = request.POST['password_login']
            user = authenticate(request, username=username_login, password=password_login)
            if user is not None:
                login(request, user)

                return redirect('detail')

            else:
                messages.error(request, 'Invalid username or password !')
                return redirect('index')

        else :
            #User model fields
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            username = request.POST['username']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            #UserProfileModel fields
            address = request.POST['address']
            profile_pic = request.FILES.get('profile_pic')

            fields = [first_name, last_name, email, username, password1, password2, address]
            if all(fields) == True:
                if password1 == password2:
                    user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=username, 
                    password=password1
                    )
                    user.save()
                    user_auth = authenticate(request, username=username, password=password1)
                    if user_auth is not None:
                        login(request, user_auth)

                    user_profile = UserProfileModel(
                        user=request.user,
                        address=address,
                        photo=profile_pic,
                    )
                    user_profile.save()
                    return redirect('detail')
                else:
                    messages.error(request, "Password din't matched try again !")
                    return render(request, 'hospital/auth.html')

            messages.error(request, 'Please fill all the fields !')
            return render(request, 'hospital/auth.html')
    
    return render(request, 'hospital/auth.html')

def detail_view(request):
    user = request.user
    
    if user.is_authenticated:
        if user.is_superuser or user.is_staff:
            data_patient = UserProfileModel.objects.filter(is_patient=True)
            user_profile = UserProfileModel.objects.get(user=request.user)
            blogs = BlogModel.objects.filter(user = user)
            draft_blogs = BlogModel.objects.filter(Q(is_draft=True) & Q(user=user))
            
            context = {
                'blogs': blogs,
                'data_patient': data_patient,
                'user_profile': user_profile,
                'draft_blogs': draft_blogs,
            }

            return render(request, 'hospital/detail_view.html', context)
        else:

            user_profile = UserProfileModel.objects.get(user=user)
            blogs = BlogModel.objects.all()
            context = {
                'blogs': blogs,
                'user_profile': user_profile,
            }
            
            return render(request, 'hospital/detail_view.html', context)
            
        
    return redirect('index')

def logout_view(request):
    logout(request)
    return redirect('index')

def blog_view(request,slug):
    user = request.user
    data_blog = BlogModel.objects.get(slug=slug)
    return render(request, 'hospital/blog.html', {'data_blog': data_blog})
    
def blog_create(request):
    method = request.method 
    if method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        category = request.POST['category']
        blog_image = request.FILES.get('blog_image')
        summary = request.POST['summary']
        # is_draft = request.POST['is_draft']
        all_fields = [title, content, category, summary, blog_image]
        if all(all_fields) == True:
            blog = BlogModel(
                title=title,
                content=content,
                category=category,
                summary=summary,
                blog_image=blog_image,
                user=request.user,
            )
            blog.save()
            return redirect('detail')
        else:
            messages.error(request, 'Please fill all the fields !')
            return render(request, 'hospital/blog_create.html')
        
    return render(request, 'hospital/blog_create.html')

def save_draft(request):
    pass
