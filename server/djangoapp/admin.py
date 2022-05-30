from django.contrib import admin
# from .models import related models
from .models import CarMake, CarModel, CarDealer, DealerReview

# Register your models here.

# CarModelInline class
class CarModelInline(admin.StackedInline):
    model = CarModel
    extra = 5
# CarModelAdmin class
# class CarModelAdmin(admin.ModelAdmin):
#     inlines = null
# CarMakeAdmin class with CarModelInline
class CarMakeAdmin(admin.ModelAdmin):
    inlines = [CarModelInline]
# Register models here
admin.site.register(CarModel)
admin.site.register(CarMake, CarMakeAdmin)
