from django.shortcuts import render
from rest_framework.views import APIView
from adresler.models import Adresler
from adresler.serializer import AdreslerSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework.decorators import api_view, action
from rest_framework import viewsets
class AdreslerView(APIView):

    def post(self, request, *args, **kwargs):

        if request.user.is_customer:
            data = request.data
    
            serializer = AdreslerSerializer(data=data)
    
            if serializer.is_valid():
            
                serializer.save()
    
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            else:
            
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request, pk, *args, **kwargs):

        try:

            adres = Adresler.objects.get(pk=pk)
        
        except Adresler.DoesNotExist:

            return Response({'error': 'Adres bulunamadı.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AdreslerSerializer(adres, data=request.data)

        if serializer.is_valid():
             
             serializer.save()

             return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, *args, **kwargs):

        adresler = Adresler.objects.all()

        serializer = AdreslerSerializer(adresler, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def delete(self, request, pk, *args, **kwargs):

        try: 
            adres = Adresler.objects.get(pk=pk)

        except Adresler.DoesNotExist:

            return Response({'error': 'Adres bulunamadı.'}, status=status.HTTP_404_NOT_FOUND)
        
        adres.delete()

        return Response(status=status.HTTP_200_OK)
    

class CreateAdresView(generics.CreateAPIView):
    queryset = Adresler.objects.all()
    serializer_class = AdreslerSerializer

class UpdateAdresView(generics.UpdateAPIView):
    queryset = Adresler.objects.all()
    serializer_class = AdreslerSerializer

class DeleteAdresView(generics.DestroyAPIView):
    queryset = Adresler.objects.all()
    serializer_class = AdreslerSerializer

class GetAllAdresView(generics.ListAPIView):
    queryset = Adresler.objects.all()
    serializer_class = AdreslerSerializer

class GetAdresById(generics.RetrieveAPIView):
    queryset = Adresler.objects.all()
    serializer_class = AdreslerSerializer

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def api_view_adres(request, pk=None):
    if request.method == 'GET':
        if pk:
            # Handle GET request to retrieve the address by ID
            try:
                adres = Adresler.objects.get(pk=pk)
                serializer = AdreslerSerializer(adres)
                return Response(serializer.data)
            except Adresler.DoesNotExist:
                return Response({'error': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Handle GET request to retrieve all addresses
            adresler = Adresler.objects.all()
            serializer = AdreslerSerializer(adresler, many=True)
            return Response(serializer.data)

    elif request.method == 'POST':
        # Handle POST request to create a new address
        serializer = AdreslerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        # Handle PUT request to update the address by ID
        try:
            adres = Adresler.objects.get(pk=pk)
        except Adresler.DoesNotExist:
            return Response({'error': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AdreslerSerializer(adres, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        # Handle DELETE request to delete the address by ID
        try:
            adres = Adresler.objects.get(pk=pk)
        except Adresler.DoesNotExist:
            return Response({'error': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)

        adres.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    else:
        return Response({'error': 'Unsupported HTTP method'}, status=status.HTTP_400_BAD_REQUEST)
    
class AdreslerViewSet(viewsets.ModelViewSet):
    queryset = Adresler.objects.all()
    serializer_class = AdreslerSerializer

    def retrieve(self, request, pk=None):
        try:
            adres = Adresler.objects.get(pk=pk)
            serializer = AdreslerSerializer(adres)
            return Response(serializer.data)
        except Adresler.DoesNotExist:
            return Response({'error': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            adres = Adresler.objects.get(pk=pk)
        except Adresler.DoesNotExist:
            return Response({'error': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(adres, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            adres = Adresler.objects.get(pk=pk)
        except Adresler.DoesNotExist:
            return Response({'error': 'Address not found'}, status=status.HTTP_404_NOT_FOUND)

        adres.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=False, methods=['GET'], url_path='filter')
    def filter_adresler(self, request):
        # Handle filtering logic based on request parameters
        sehir = request.query_params.get('sehir', None)
        mahalle = request.query_params.get('mahalle', None)
        sokak = request.query_params.get('sokak', None)
        bina = request.query_params.get('bina', None)
        daire = request.query_params.get('daire', None)

        queryset = Adresler.objects.all()

        if sehir:
            queryset = queryset.filter(sehir=sehir)
        if mahalle:
            queryset = queryset.filter(mahalle=mahalle)
        if sokak:
            queryset = queryset.filter(sokak=sokak)
        if bina:
            queryset = queryset.filter(bina=bina)
        if daire:
            queryset = queryset.filter(daire=daire)

        serializer = AdreslerSerializer(queryset, many=True)
        return Response(serializer.data)