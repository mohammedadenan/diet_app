from django.shortcuts import render
from diet_app.models import *
from diet_app.serializers import *
from rest_framework.generics import CreateAPIView,RetrieveAPIView,UpdateAPIView,ListAPIView,DestroyAPIView,RetrieveUpdateAPIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from diet_app.utility_func import calculate_bmr
from diet_app.permissions import IsOwner
# Create your views here.


class SignUpView(CreateAPIView):
    serializer_class=UserSerializer

class ProfilCreateView(CreateAPIView):
    serializer_class=UserProfileSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAuthenticated]


    def perform_create(self, serializer):
        user_objects=self.request.user
        # data=serializer.validated_data
        # bmr=calculate_bmr(
        #     age=data.get('age'),
        #     height=data.get('height'),
        #     weight=data.get('weight'),
        #     gender=data.get('gender'),
        #     activity_level=data.get('activity_level')
        # )

        return serializer.save(owner=user_objects)


class ProfileRetrieView(RetrieveAPIView,UpdateAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsOwner]
    serializer_class=UserProfileSerializer
    queryset=UserProfile.objects.all()


class UserRetriveView(RetrieveAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsOwner]
    serializer_class=UserSerializer
    queryset=CustomUser.objects.all()

class FoodLogCreate(CreateAPIView,ListAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsOwner]
    serializer_class=FoodLogSerializer
    queryset=FoodLog.objects.all()

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    
    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)
    
class FoodRetrieveUpdateDestoy(RetrieveUpdateAPIView,DestroyAPIView):
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsOwner]
    serializer_class=FoodLogSerializer
    queryset=FoodLog.objects.all()

    