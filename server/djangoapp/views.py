from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarMake, CarModel
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, get_dealer_reviews_from_cf
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.
def index(request):
    return render(request, 'djangoapp/index.html')

# Create an `about` view to render a static about page
def about(request):
    return render(request, 'djangoapp/about.html')

# Create a `contact` view to return a static contact page
def contact(request):
    return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# # Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# # Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://dbe14de2.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # dealer_name = dealerships
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealership):
    context = {}
    if request.method == "GET":
        url = "https://dbe14de2.us-south.apigw.appdomain.cloud/api2/review"
        # Get reviews from the URL
        reviews = get_dealer_reviews_from_cf(url, dealership)
        context = "{}<br><br>{}".format(reviews[0], reviews[1])
        return HttpResponse(context)

# Create a `add_review` view to submit a review
def add_review(request, **kwargs):
    if request.method == "GET":
        # dealership = dealership
        url = "https://dbe14de2.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        context = {
            "cars": CarModel.objects.all(),
            # "dealership": dealership,
            "dealer_name": get_dealers_from_cf(url)[2],
        }
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            form = request.POST
            username = request.user.username
            print(form)
            payload = dict()
            car_id = form["car"]
            car = CarModel.objects.get(pk=car_id)
            payload["dealership"] = dealership
            payload["review"] = form["content"]
            payload["purchase"] = False
            if "purchasecheck" in form:
                payload["purchase_date"] = datetime.strptime(form.get("purchasedate"), "%Y-%m-%d").isoformat()
                car = CarModel.objects.get(pk=form["car"])
                payload["car_make"] = car.car_make.name
                payload["car_model"] = car.car_name
                payload["car_year"]= car.car_year.strftime("%Y")
            #json_payload = {}
            json_payload = {"review": payload}
            rev = json_payload["review"]
            print (rev)
            url = "https://dbe14de2.us-south.apigw.appdomain.cloud/api3/review"
            restapis.post_request(url, rev, dealership=dealership)
            
            return redirect("djangoapp:dealer_details", dealership=dealership)
        else:
            return redirect("/djangoapp/login")
