from django.db import models


class Manufacturer(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Model(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.manufacturer.name + " " + self.name


class Motorcycle(models.Model):
    name = models.CharField(max_length=50)
    model = models.ForeignKey(Model, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('Date published', auto_now_add=True)
    pub_user = models.ForeignKey('auth.User', related_name="publisher", on_delete=models.CASCADE)
    year = models.IntegerField(default=0)
    mileage = models.IntegerField(default=0)
    price = models.IntegerField(default=0)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    description = models.TextField(default='')
    show_to = models.ManyToManyField('auth.User', related_name="show_to", blank=True)

    def __str__(self):
        return str(self.name) + "(" + str(self.model) + ")"


class MotorcycleFeature(models.Model):
    motorcycle = models.ForeignKey(Motorcycle, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', blank=True)
    description = models.TextField(default='')

    def __str__(self):
        return self.description


