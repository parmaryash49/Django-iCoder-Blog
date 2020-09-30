from django.shortcuts import render, HttpResponse, redirect
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from blog.models import Post
# Create your views here.

def home(request):
    return render(request, 'home/home.html')

def about(request):
    return render(request, 'home/about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        print(name, email, phone, content)
        if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
            messages.error(request, " please fill the form correctly")
        else: 
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, " Your message hass been successfully  sent....")
    return render(request, 'home/contact.html') 

def search(request):
    query = request.GET['query']
    if len(query)>78:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPostsAuthor = Post.objects.filter(author__icontains=query)
        allPostsTimestamp = Post.objects.filter(time_stamp__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent,allPostsAuthor,allPostsTimestamp)

    if allPosts.count() == 0:
        messages.warning(request, " No search result found. Please refine your query ...")
    params = {'allPosts': allPosts, 'query': query} 
    return render(request, 'home/search.html', params)
    

def handleSignup(request):
    if request.method == 'POST':
        # Get the post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        # Check for errorneous input
        # Username should be unser 10 characters
        if len(username) > 10:
            messages.error (request, ' Username must be under 10 characters')
            return redirect('home')
            
        # Username should be alphanumetric    
        if not username.isalnum():
            messages.error(request, ' Username should only contain letters and numbers')
            return redirect('home')

        # passwords should match
        if password != cpassword:
            messages.error(request, ' Password do not match')
            return redirect('home')

        # Create the user
        myuser = User.objects.create_user(username, email, password)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.cpassword = cpassword
        myuser.save()
        messages.success(request, ' Your iCoder account will be successfully created')
        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')


def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username = loginusername, password = loginpassword)
        
        if user is not None:
            login(request, user)
            messages.success(request, ' Successfully Logged in')
            return redirect('home')
        else:
            messages.error(request, ' Invalid Credentials,Please try again')
            return redirect('home')
    else:
        return HttpResponse('404 - Not Found')

def handleLogout(request):
        logout(request)
        messages.success(request, ' Successfully Logged out')
        return redirect('home')
        
