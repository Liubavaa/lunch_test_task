from rest_framework import generics, status
from rest_framework.response import Response
from .models import Restaurant, Menu, CustomUser
from .serializers import RestaurantSerializer, MenuSerializer, UserSerializer, MyTokenObtainPairSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsRestaurantAdmin, IsEmployee
from rest_framework.decorators import api_view, permission_classes
from datetime import date
from rest_framework_simplejwt.views import TokenObtainPairView
from django.shortcuts import get_object_or_404


# Login User
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Register User
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsRestaurantAdmin])
def create_restaurant(request):

    # It's example of how I would handle supporting both version (by adding such code to each endpoint). But now it
    # seems to me like an unnecessary additional code, because I don't even know what the difference between versions.

    # vers = request.version
    # if vers == "1.0":
    #     create_restaurant_1_0(request)
    # elif vers == "2.0":
    #     create_restaurant_2_0(request)

    data = request.data.copy()
    data["admin"] = request.user.id

    serializer = RestaurantSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsRestaurantAdmin])
def upload_menu(request):
    data = request.data.copy()
    data["restaurant"] = get_object_or_404(Restaurant, admin=request.user).id

    serializer = MenuSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_today_menu(request):
    today_menus = Menu.objects.filter(date=date.today())
    if today_menus:
        serializer = MenuSerializer(today_menus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response({"error": "No menu available for today."}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsEmployee])
def vote_for_menu(request, menu_id):
    menu = get_object_or_404(Menu, pk=menu_id)
    vote, created = menu.vote_set.get_or_create(employee=request.user)
    if created:
        return Response({"message": "Vote cast successfully!"}, status=status.HTTP_201_CREATED)
    return Response({"message": "Vote's already cast for this menu!"}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_results(request):
    today_menus = Menu.objects.filter(date=date.today())
    if today_menus:
        res = [{'menu': MenuSerializer(menu).data, 'votes': menu.vote_set.count()} for menu in today_menus]
        return Response(res, status=status.HTTP_200_OK)
    return Response({"error": "No voting results for today."}, status=status.HTTP_404_NOT_FOUND)
