from django.http import HttpResponse, JsonResponse
# from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from apps.library.models import Library, Book
from .serializers import LibrarySerializers, BookSerializers
from rest_framework import mixins, generics
from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated


class LibraryView(generics.ListCreateAPIView):
    queryset = Library.objects.all()
    serializer_class = LibrarySerializers

    def get(self, request, *args, **kwargs):
        # Note the use of `get_queryset()` instead of `self.queryset`
        queryset = Library.objects.all()
        serializer = LibrarySerializers(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        sz = LibrarySerializers(data=request.data)
        if sz.is_valid():
            sz.save()
            return JsonResponse({'success': True, 'data': sz.data}, status=201)
        return HttpResponse(404)


class BookView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializers




