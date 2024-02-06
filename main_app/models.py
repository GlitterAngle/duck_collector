from django.db import models
# this allows me to use date
from datetime import date

# Create your models here.
class Duck(models.Model):
    name = models.CharField(max_length=100)
    breed = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

    def __str__(self):
        return self.name
    # to get this to show up you have to make sure you include it in your serializer under duck
    def fed_for_today(self):
        return self.feeding_set.filter(date=date.today()).count() >= len(MEALS)

    #this will let me have a drop down with the worrds applied to it. 
MEALS = (
     ('B', 'Breakfast'),
     ('L', 'Lunch'),
     ('D', 'Dinner')
)
class Feeding(models.Model):
        date = models.DateField('Quack Time')
        meal = models.CharField(max_length=1,
                                choices=MEALS,
                                default=MEALS[0][0])
        # this will give the feeding the id of the duck
        duck = models.ForeignKey(Duck, on_delete=models.CASCADE)

        def __str__(self):
             return f"{self.get_meal_display()} on {self.date}"
        # this reutrns everthing in the order of newest created first
        class Meta:
             ordering = ['-date']