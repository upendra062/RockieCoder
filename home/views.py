from django.shortcuts import redirect, render, HttpResponse
from home.models import Contact
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from blog.models import Post

# Create your views here.


def home(request):
    return render(request, 'home/home.html')
    # return HttpResponse('This is home')


def about(request):
    messages.success(request, 'Welcome to about')
    messages.success(request, 'Welcome to about1')
    messages.error(request, 'Welcome to about1')
    return render(request, 'home/about.html')


def contact(request):
    if request.method == 'POST':
        # print('we are using post request')
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']
        # print(name, email, phone, content)

        if len(name) < 2 or len(email) < 3 or len(phone) < 10 or len(content) < 4:
            messages.error(request, "Please fill the form correctly")
        else:
            contact = Contact(name=name, email=email,
                              phone=phone, content=content)
            contact.save()
            messages.success(
                request, "Your message has been successfully send")
    return render(request, 'home/contact.html')


def own(request):
    return render(request, 'home/own.html')


def search(request):
    query = request.GET['query']
    # allPosts = Post.objects.all()
    if len(query) > 78:
        allPosts = Post.objects.none()
    else:
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)

    if allPosts.count() == 0:
        messages.error(
            request, "No search results found. Please refine your query")
    params = {"allPosts": allPosts, 'query': query}
    return render(request, 'home/search.html', params)
    # return HttpResponse('This is search')


def handleSignUp(request):
    if request.method == "POST":
        # Get the post parameters
        username = request.POST['username']
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for errorneous input
        # username should be under 10 characters
        if len(username) < 10:
            messages.error(request, "Username must be under 10 characters")
            return redirect('home')

        # username should be alphanumeric
        if not username.isalnum():
            messages.error(
                request, "Username should only contain letter and numbers")
            return redirect('home')
        # passwords should match
        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return redirect('home')

        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(
            request, "Your RockyCoder has been successfully created")
        return redirect('home')

    else:
        return HttpResponse("404 - Not found")


def handleLogin(request):

    if request.method == "POST":
        # Get the post parameters
        loginusername = request.POST['loginusername']
        loginpassword = request.POST['loginpassword']

        user = authenticate(username=loginusername, password=loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('home')
        else:
            messages.error(request, "Invalid Credentials Please try again")
            return redirect('home')

    return HttpResponse('404 - Not Found')


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')
