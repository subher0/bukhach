from rest_framework import viewsets
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from bukhach.serializers import UserSerializer, GroupSerializer, ProfileSerializer
from django.contrib.auth.models import User, Group
from bukhach.models.profile_models import Profile
from django.db.models import Q


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ProfileView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ProfileSerializer

    def get(self, request):
        profile = Profile.objects.filter(user=request.user).first()
        print(profile.avatar)
        print(profile.user.first_name)
        response = Response({'first_name': profile.user.first_name,
                             'last_name': profile.user.last_name,
                             'username': profile.user.username,
                             'email': profile.user.email,
                             'info': profile.info,
                             'tel_num': profile.tel_num,
                             'rating': profile.rating,
                             'avatar': str(profile.avatar)
                             })
        return response


class ProfileSearchView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    def get(self,request):
        name = request.GET.get('name')
        words = name.split()
        if len(words) == 1:
            name = words[0]
            queryset = User.objects.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
            serializer_context = {
                'request': request,
            }
            serializer_class = UserSerializer(queryset, context=serializer_context)
            return Response(serializer_class.data)
        elif len(words) == 2:
            f_name = words[0]
            l_name = words[1]
            queryset = User.objects.filter(first_name__icontains=f_name, last_name__icontains=l_name)
            serializer_context = {
                'request': request,
            }
            serializer_class = UserSerializer(queryset, context=serializer_context, many=True)
            return Response(serializer_class.data)
