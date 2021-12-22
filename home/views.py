from django.shortcuts import render, HttpResponse
from home.models import Contact
from django.contrib import messages
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
