from django.contrib import admin
from .models import Library, Book
# Register your models here.


class LibraryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'address']
    search_fields = ['name', 'address']
    fields = ['id', 'name', 'address']
    list_filter = ['name']
    readonly_fields = ['address']


admin.site.register(Library, LibraryAdmin)
admin.site.register(Book)
