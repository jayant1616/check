from django.shortcuts import render,redirect,HttpResponse
from basicapp.models import profile,friends,Posts,Comments
from basicapp.forms import user_form,newpost,comment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

# Create your views here.
def registration(request):
    if request.method == 'POST':
        form_obj = user_form(request.POST)
        print('check1')
        if form_obj.is_valid():
            print('check2')
            username = form_obj.cleaned_data['username']
            firstname = form_obj.cleaned_data['first_name']
            lastname = form_obj.cleaned_data['last_name']
            pro_site = form_obj.cleaned_data['site']
            #pro_pic = form_obj.cleaned_data['picture']
           # birthdate = form_obj.cleaned_data['birthdate']
            password = form_obj.cleaned_data['password']
            user = User(username=username,first_name=firstname,last_name=lastname)#,birthdate=birthdate)
            user.set_password(password)
            profile_obj = profile(user=user,portfolio_site=pro_site)#,profile_pic=pro_pic)
            user.save()
            print(user.username)
            profile_obj.save()
            friends.objects.create(tag=user)
            friends.objects.get(tag=user).save()
            return HttpResponse('done')
    else:
        form_obj= user_form()
        return render(request,'registration.html',{'form_1':form_obj,})


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username= username,password=password)
        if user:
            login(request,user)
            print(str((request.user).first_name))
            return redirect('/newsfeed')
        else:
            return HttpResponse('invalid credentials')
    else:
        return render(request,'login.html',{})

def newsfeed(request):
    print(request.user.first_name)
    main_user = request.user
    load_friends = friends.objects.get(tag=main_user).following.all()
    post_all=Posts.objects.none()#creating an empty queryset
    for friends_all in load_friends:# basicaaly assigns users to filter out friends

        post_all = post_all | Posts.objects.filter(for_user = friends_all)
    dict_post = {'post_all':post_all,}

    return render(request,'Posts.html',dict_post)

def add_post(request):
    post_model = Posts(for_user = request.user)
    if request.method=='POST':
        post_object=newpost(request.method)
       # for test in post_object.errors:
        #     print('t')
         #    print(post_object.errors[test])
        if  post_object.is_valid():   
            
            print('check1')
            post_model.user_post=post_object.cleaned_data['post_1']
            post_model.save()
            return redirect('admin/')

    else:
        post_object = newpost()
        return render(request,'newpost.html',{'post':post_object,})

def comments(request,id):
    post_get = Posts.objects.get(id = id)
    comment_object = Comments(for_comment=post_get,user = request.user)
    if request.method == 'POST':
        form = comment(request.POST)
        if form.is_valid():
            print('checkcomment')
            comment_object.user_comment = form.cleaned_data['comment_add']
            comment_object.save()
            return redirect('http://127.0.0.1:8000/admin/')
    else:
        form = comment()
        return render(request,'comments.html',{'form':form,})

def user_profiles(request):
    all_users = User.objects.all()
    context = {'users': all_users}
    return render(request,'user_profiles.html',context)



def ind_profile(request,user_id):
    user = User.objects.get(id = user_id)
    follow_list = friends.objects.get(tag = user).following.all()
    follower_list = user.followers.all()
    users_qset = User.objects.none()
    #prof_pic = profile.objects.get(user=user).profile_pic
    """for all in follower_list:
        users_qset = users_qset|all.tag
        """
    if request.user in follow_list:
        status='Already following'
    else:
        status = 'Follow'
    values={'user_id':user_id,'username':user.username,'firstname1':user.first_name,'lastname1':user.last_name,'follow_list':follow_list,'  status':status}
    return render(request,'show_user.html',values)

def add_following(request,id):
    user = request.user
    if User.objects.get(id=id) not in friends.objects.get(tag=user).following.all():
        friends.objects.get(tag= user).following.add(User.objects.get(id=id))
        friends.objects.get(tag= user).save()

        return HttpResponse('followed')
    else:
        return HttpResponse('already following')
