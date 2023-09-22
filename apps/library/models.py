from django.db import models


class Library(models.Model):
    name = models.CharField(max_length=221)
    address = models.CharField(max_length=221)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=221)
    author = models.CharField(max_length=221)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name
