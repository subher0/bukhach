from collections import defaultdict

import os
import requests

from rest_framework import viewsets, status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from bukhach.models.matcher_models import UserInterval
from bukhach.serializers import UserSerializer, GroupSerializer, ProfileSerializer, IntervalSerializer, AppealSerializer
from bukhach.permissions.is_authenticated_or_write_only import IsAuthenticatedOrWriteOnly
from django.contrib.auth.models import User, Group
from bukhach.models.profile_models import Profile
from django.db.models import Q

from bukhach.utils.matcher_utils import UsersToInterval, IntervalAsDatetime, IntervalAsDatetimeSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class ProfileView(GenericAPIView):
    permission_classes = (IsAuthenticatedOrWriteOnly,)
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

    def post(self, request, *args, **kwargs):
        serializer_class = ProfileSerializer(data=request.data)
        if serializer_class.is_valid():
            user = serializer_class.save()
            if user:
                return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors)
        return Response(serializer_class.errors)


class ProfileSearchView(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    @staticmethod
    def __info_append(users, content):
        for user in users:
            element = {'first_name': user.first_name,
                       'last_name': user.last_name,
                       'username': user.username,
                       'email': user.email,
                       'info': user.profile.info,
                       'tel_num': user.profile.tel_num,
                       'rating': user.profile.rating,
                       'avatar': str(user.profile.avatar)
                       }
            content.append(element)
        return content

    def get(self,request):
        content = []
        name = request.GET.get('name')
        if name == '':
            return Response('gay')
        else:
            words = name.split()
            if len(words) == 1:
                name = words[0]
                users = User.objects.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name))
                response = Response(self.__info_append(users, content))
                return response
            elif len(words) == 2:
                f_name = words[0]
                l_name = words[1]
                users = User.objects.filter(first_name__icontains=f_name, last_name__icontains=l_name)
                response = Response(self.__info_append(users, content))
                return response


class IntervalView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer_class = IntervalSerializer(data=request.data)
        if serializer_class.is_valid():
            interval = serializer_class.save()
            if interval:
                return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors)
        return Response(serializer_class.errors)


class MatchView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        intervals = UserInterval.objects.filter(~Q(user=request.user))
        currentUserIntervals = UserInterval.objects.filter(user=request.user)

        usersToIntervals = defaultdict(list)
        for interval in intervals:
            usersToIntervals[interval.user].append(interval)

        matcher = UsersToInterval()
        for currentInterval in currentUserIntervals:
            matcher.add_interval(currentInterval.start_date.timestamp(), currentInterval.end_date.timestamp())

        matcher.matchIntervals()

        for key, value in usersToIntervals.items():
            for userInterval in value:
                matcher.add_interval(userInterval.start_date.timestamp(), userInterval.end_date.timestamp())
            matcher.matchIntervals()
            matcher.add_user(key)

        matchedUsers, matchedIntervals = matcher.get_matched_intervals()

        matchedIntervalsAsTimestamps = []
        for interval in matchedIntervals:
            matchedIntervalsAsTimestamps.append(IntervalAsDatetimeSerializer(IntervalAsDatetime(interval['start'], interval['end'])).data)

        context = {
            'intervals': matchedIntervalsAsTimestamps,
            'users': matchedUsers
        }
        return Response(context)


class AppealsView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = AppealSerializer(data=request.data)
        if serializer.is_valid():
            payload = {'user_id': '29497311', 'message': 'Тема: ' + str(serializer.data.pop('title'))+ '\n\n\n' + 'Email отправителя: ' + str(serializer.data.pop('email')) + '\n\n\n' + 'Сообщение: ' + str(serializer.data.pop('text')), 'access_token': os.environ.get('VK_TOKEN'), 'v': '5.73'}
            #'https://api.vk.com/method/messages.send?user_id=29497311&message=&access_token=ac8c62cc8e2dd246d691d1f9aa53dc5a68134ccbad4c84ef3f9e32a63f017405bd23a0c8a20b40fec109f&v=5.73'
            r = requests.post('https://api.vk.com/method/messages.send', params=payload)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)