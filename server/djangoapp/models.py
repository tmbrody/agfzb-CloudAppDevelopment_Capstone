from django.db import models
from django.utils.timezone import now

# Create your models here.

class CarMake(models.Model):
    name = models.CharField(null= False, max_length=30, default='Brand')
    description = models.CharField(null= False, max_length=300, default='Brand cars are fine.')

    def __str__(self):
        return 'Name:' + self.name + ',' + \
            'Description:' + self.description

class CarModel(models.Model):
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    OTHERS = 'others'
    CAR_CHOICES = [(SEDAN, "Sedan"), (SUV, 'SUV'), (WAGON, 'Wagon'), (OTHERS, 'Others')]
    carmake = models.ForeignKey(CarMake, null= True, on_delete=models.CASCADE)
    name = models.CharField(null= False, max_length=30, default='Audi X8')
    dealerid = models.IntegerField(null=True)
    cartype = models.CharField(null= False, max_length=20, choices= CAR_CHOICES, default=SEDAN)
    year = models.DateField(null= True)

    def __str__(self):
        return 'Name ' + self.name
# <HINT> Create a plain Python class `CarDealer` to hold dealer data

class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, state, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        self.state = state
        # Dealer zip
        self.zip = zip
        self.idx = 0

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, id):
        self.dealership = dealership
        self.name = name
        self.purchase = purchase
        self.review = review
        self.id = id

    def __str__(self):
        return "Review: " + self.review