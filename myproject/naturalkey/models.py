from django.db import models
from django.utils.translation import ugettext_lazy as _


class PersonManager(models.Manager):
    def get_by_natural_key(self, first_name, last_name):
        return self.get(first_name=first_name, last_name=last_name)


class Person(models.Model):
    objects = PersonManager

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    birthdate = models.DateField()

    def natural_key(self):
        return self.first_name, self.last_name

    class Meta:
        unique_together = (('first_name', 'last_name'),)


class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Person, on_delete=models.CASCADE)


class CountryManager(models.Manager):
    def get_by_natural_key(self, name):
        return self.get(name=name)


class CountryModel(models.Model):
    """国家"""
    objects = CountryManager()

    name = models.CharField(_("国家"), max_length=32, unique=True)

    def natural_key(self):
        return self.name,

    def __str__(self):
        return self.name


class StateModel(models.Model):
    """州"""

    name = models.CharField(_("州"), max_length=32)
    country = models.ForeignKey(CountryModel, on_delete=models.CASCADE)

    def natural_key(self):
        return self.name,

    def __str__(self):
        return self.name
