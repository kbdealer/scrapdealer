import json

from django.core.paginator import Paginator

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import ScrapPrice, QuoteRequest, PickupBooking, ContactMessage, SCRAP_TYPES, Comment
from django.contrib.auth import authenticate,login, logout
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from .forms import QuoteRequestForm, ContactMessageForm, PickupBookingForm , ContactMessage,CommentForm
from django.contrib.auth.decorators import login_required
# views.py

def home(request):
    comments = Comment.objects.select_related('user').all()
    form = CommentForm()
    scrap_types = SCRAP_TYPES                  # import from models.py

    all_prices = ScrapPrice.objects.all()
    paginator = Paginator(all_prices, 3)        # 3 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'myapp/home.html', {
        'comments': comments,
        'form': form,
        'page_obj': page_obj,
        'scrap_types': scrap_types,
    })  

    
def about(request):
    return render(request,"myapp/_about.html")

def login_view(request):
    if request.method =='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request,'invalid username or password')
            return redirect('login')
        
    return render(request, 'myapp/login.html')
        
def register_view(request):
    if request.method =="POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Regstration successful!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = UserRegistrationForm()
    return render(request, 'myapp/register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')

def prices(request):
    all_prices = ScrapPrice.objects.all()
    paginator = Paginator(all_prices, 3)          # 3 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
 
    return render(request, 'myapp/prices.html', {
        'page_obj': page_obj,
    })

def get_quote(request):
    quote_result = None

    if request.method == "POST":
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            quote_request = form.save(commit=False)

            # .filter().first() returns None if not found, never crashes
            scrap_price = ScrapPrice.objects.filter(scrap_type=quote_request.scrap_type).first()

            if scrap_price:
                quote_request.estimated_price = float(scrap_price.price_per_kg) * float(quote_request.weight_kg)
                price_per_kg = scrap_price.price_per_kg
            else:
                quote_request.estimated_price = None
                price_per_kg = None

            quote_request.save()

            quote_result = {
                'name':            quote_request.name,
                'phone':           quote_request.phone,
                'scrap_type':      quote_request.scrap_type,
                'weight_kg':       quote_request.weight_kg,
                'price_per_kg':    price_per_kg,
                'estimated_price': quote_request.estimated_price,
            }
            messages.success(request, 'Quote request submitted!')
    else:
        form = QuoteRequestForm()

    scrap_prices_json = json.dumps({
        sp.scrap_type: float(sp.price_per_kg)
        for sp in ScrapPrice.objects.all()
    })

    return render(request, 'myapp/quote.html', {
        'form':              form,
        'scrap_types':       SCRAP_TYPES,
        'quote_result':      quote_result,
        'scrap_prices_json': scrap_prices_json,
    })

@login_required(login_url='login')
def book_pickup(request):
    if request.method == 'POST':
        form = PickupBookingForm(request.POST)
        scrap_type = request.POST.get('scrap_type')

        if form.is_valid():
            book_user = form.save(commit=False)
            book_user.user = request.user
            book_user.save()
            messages.success(request, 'Pickup booked successfully!')
            return redirect('book_pickup')
    else:
        form = PickupBookingForm()
    
    return render(request, 'myapp/pickup.html', {'form': form, 'scrap_types': SCRAP_TYPES})        

def contact(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST['name'],
            phone=request.POST['phone'],
            message=request.POST['message']
        )
        messages.success(request, 'Message sent! We will call you soon.')
        return redirect('contact')

    # Your business coordinates — change these!
    context = {
        'lat': 34.168144,
        'lng': 72.306810,
        'business_name': 'saddam Scrap Dealers',
        'phone': '+92-3239106011',
        'address': 'shewa adda road haji abad stop dagai,swabi, KPK',
        'whatsapp': '92-3239106011',
    }
    return render(request, 'myapp/contact.html', context)

@login_required(login_url='login')
def add_comment(request):
    if request.method =="POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.save()
            messages.success(request, 'Comment added!')
            messages.success(request, 'Comment posted!')
        else:
            messages.error(request, 'Invalid comment.')
    return redirect('home')  # make sure 'home' matches your URL name

@login_required
def delete_comment(request, comment_id):
    comment = Comment.objects.get(id=comment_id, user=request.user)
    comment.delete()
    messages.success(request, 'Comment deleted.')
    return redirect('home')