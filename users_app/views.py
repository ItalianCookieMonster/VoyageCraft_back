from django.shortcuts import render
from .models import User, Preference
from rest_framework import generics
from .serializers import UserSerializer, PreferenceSerializer, UserUpdateSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny


# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class RetrieveUpdateUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class CreatePreferenceView(generics.ListCreateAPIView):
    serializer_class = PreferenceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Preference.objects.filter(user=user)

    def perform_create(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)


class DeletePreferenceView(generics.DestroyAPIView):
    serializer_class = PreferenceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Preference.objects.filter(user=user)


class UpdatePreferenceView(generics.UpdateAPIView):
    serializer_class = PreferenceSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        user = self.request.user
        return Preference.objects.filter(user=user)

    def perform_update(self, serializer):
        if serializer.is_valid():
            serializer.save(user=self.request.user)
        else:
            print(serializer.errors)
