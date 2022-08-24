import profile
from unicodedata import category
from xml.dom.minidom import parseString
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import UserProfileModel, BlogModel, BookAppointment
from django.contrib import messages
# import Q
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count
# JsonResponse import 
from django.http import JsonResponse
# from . import event
from datetime import datetime , date, timedelta
# from googleapiclient.discovery import build
# from google.oauth2 import service_account

# Create your views here.
# SCOPES = ["https://www.googleapis.com/auth/calendar"]
# service_account_email = "vikask99588@gmail.com"
# credentials = service_account.Credentials.from_service_account_file('client_secret_200284731842-0i542ral2qlshrte9dqiv7q30bdoocs0.apps.googleusercontent.com.json')
# scoped_credentials = credentials.with_scopes(SCOPES)
# calendarId = "n1264sanvvuog5ojbf3qibql2s@group.calendar.google.com"



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

# def build_service(request):

#     service = build("calendar", "v3", credentials=scoped_credentials)
#     return service


def detail_view(request):
    user = request.user
    
    if request.method == 'POST':
        data = request.POST
        doc_id = data['doc_id']
        discription = data['discription']
        time = data['time']
        date_apt = data['date']
        doctor = User.objects.get(id=int(doc_id))
        fields = [doc_id, discription, time, date_apt]
        if all(fields):
        
            appoint_date = datetime.strptime(date_apt,'%Y-%m-%d').date()
            if date.today() < appoint_date:
                book = BookAppointment(
                    doctor = doctor,
                    patient = user,
                    apppoint_date = appoint_date,
                    appoint_time = time,
                    discription = discription,

                )   
                book.save()
                # event.create_event(doctor, discription, date_apt)
                
                messages.info(request, 'Appointment created successfully !')
                return redirect('detail')
            else:
                messages.info(request, 'Appointment date shout not be less then current date !')
                return redirect('detail')
        else:
            messages.info(request, 'All fields required !')
            return redirect('detail')

    
    if user.is_authenticated:
        if user.is_superuser or user.is_staff:

            data_patient = UserProfileModel.objects.filter(is_patient=True)
            user_profile = UserProfileModel.objects.get(user=request.user)
            total_draft = BlogModel.objects.filter(Q(is_draft=True) & Q(user=user)).count()
            blogs = BlogModel.objects.filter(user = user).order_by('-updated_at')
            draft_blogs = BlogModel.objects.filter(Q(is_draft=True) & Q(user=user)).order_by('-updated_at')
            patient_obj = BookAppointment.objects.select_related().filter(doctor=user).order_by('-apppoint_date')
            
            patient_profile = []
            for obj in patient_obj:
                patient_profile.append(UserProfileModel.objects.get(user = obj.patient))
            
            context = {
                'blogs': blogs,
                'data_patient': data_patient,
                'user_profile': user_profile,
                'draft_blogs': draft_blogs,
                'total_draft' : total_draft,
                'patient_obj' : patient_obj,
                'patient_profile' : patient_profile
            }

            return render(request, 'hospital/detail_view.html', context)
        else:

            doctors = User.objects.select_related().filter(Q(is_staff = True) | Q(is_superuser = True))
            print(doctors)
            user_profile = UserProfileModel.objects.get(user=user)
            blogs = BlogModel.objects.all()
            patient_obj = BookAppointment.objects.select_related().filter(patient=user).order_by('-apppoint_date')
            # after = 45
            # # Add 45 minutes to datetime object
            # final_time = patient_obj.appoint_time + timedelta(minutes=after)

            # print(final_time)
            context = {
                'blogs': blogs,
                'user_profile': user_profile,
                'doctors' : doctors,
                'patient_obj' : patient_obj,
                # 'final_time' : final_time

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
    print(request.POST)
    if method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        category = request.POST['category']
        blog_image = request.FILES.get('blog_image')
        summary = request.POST['summary']
        is_draft = request.POST.get('is_draft')
        
        if is_draft == 'True':
            is_draft = True
        else:
            is_draft = False

        print(is_draft)
        all_fields = [title, content, category, summary, blog_image]
        if all(all_fields) == True:
            blog = BlogModel(
                title=title,
                content=content,
                category=category,
                summary=summary,
                blog_image=blog_image,
                user=request.user,
                is_draft=is_draft,
            )
            blog.save()
            return redirect('detail')
        else:
            messages.error(request, 'Please fill all the fields !')
            return render(request, 'hospital/blog_create.html')
        
    return render(request, 'hospital/blog_create.html')


# csrf exempt import

@csrf_exempt
def save_draft(request):

    method = request.method
    print(method)
    print(request.POST)
    if method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        category = request.POST.get('category')
        blog_image = request.POST.get('blog_image')
        summary = request.POST['summary']

     
        print(f'title : {title} | content : {content} | category : {category} | summary : {summary} | blog_image : {blog_image}')
        
        all_fields = [title, content, category, summary, blog_image]
        

        if all(all_fields) == True:
            blog = BlogModel(
                title=title,
                content=content,
                category=category,
                summary=summary,
                blog_image=blog_image,
                user=request.user,
                is_draft=True,
                is_published=False,
            )
            blog.save()
            return redirect('detail')
        else:
            return JsonResponse({'status': 'error'})
        
def all_blogs(request):
    blogs = BlogModel.objects.all()
    context = {
        'blogs': blogs,
    }
    return render(request, 'hospital/all_blog.html', context)

@csrf_exempt
def book_appoint(request):
    if request.method == 'POST':
        data = request.POST
        id = data['id']
        discription = data['discription']
        time = data['time']
        date = data['date']

        print(id,discription, time, date)
    
    return JsonResponse({'data':'success'})


def book_ap(request):
    patient_id = request.GET['id']

    if patient_id :
        btn = BookAppointment.objects.get(id=patient_id)
        btn.is_pending = False

        btn.save()
    
    return JsonResponse({'statuc': f'done :{patient_id}'})