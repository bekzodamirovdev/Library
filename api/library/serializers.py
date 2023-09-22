from rest_framework import serializers
from apps.library.models import Library, Book


class LibrarySerializers(serializers.ModelSerializer):
    class Meta:
        model = Library
        fields = ['id', 'name', 'address']


class BookSerializers(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['id', 'name', 'author', 'price']
