import hashlib
import smtplib
import uuid
from email.mime.text import MIMEText
from threading import Thread

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import HttpResponseRedirect
from rest_framework import status
from rest_framework.decorators import action, api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from django.template import loader, Context

from bukhach.consts import ProfileMessages, MainMessages
from bukhach.models.profile_models import Profile, Invite
from bukhach.permissions.is_authenticated_or_write_only import IsAuthenticatedOrWriteOnly
from bukhach.serializers.user_serializers import ProfileMinSerializer, ProfileMaxSerializer, ProfileMedSerializer


def send_email_with_confirmation(profile):
    server = smtplib.SMTP_SSL('smtp.zoho.eu', 465)
    sender = 'gayycrew@coordinat.org'
    server.login(sender, '1!gayPassword.')

    hash_func = hashlib.sha3_512()
    hash_func.update(str(profile.user.email).encode('utf-8'))
    hash_func.update(str(profile.user.username).encode('utf-8'))
    hash_func.update(str(uuid.uuid4()).encode('utf-8'))
    hash = hash_func.hexdigest()

    Invite.objects.create(invitation_code=hash, user=profile.user)

    html = loader.get_template('bukhach/invitation.html').render({'confirmation_hash': hash})

    msg = MIMEText(html, 'html')
    msg['Subject'] = "Посвящение в алкаши"
    msg['From'] = sender
    msg['To'] = profile.user.email

    server.sendmail(sender, [profile.user.email], msg.as_string())
    server.quit()


@api_view(['GET'])
def confirm(request):
    confirmation_hash = request.query_params['confirmation_hash']
    try:
        invite = Invite.objects.get(invitation_code=confirmation_hash)
    except ObjectDoesNotExist:
        return Response(ProfileMessages.INVITE_DOES_NOT_EXIST, status.HTTP_401_UNAUTHORIZED)
    user = invite.user
    user.is_active = True
    user.save()
    print(confirmation_hash)
    return HttpResponseRedirect('https://coordinat.org/')


class ProfileViewSet(ViewSet):
    permission_classes = (IsAuthenticatedOrWriteOnly,)

    def create(self, request):
        serializer_class = ProfileMaxSerializer(data=request.data)
        if serializer_class.is_valid():
            if User.objects.filter(email=request.data['user']['email']).first() is not None:
                return Response(ProfileMessages.EMAIL_ALREADY_EXISTS, status=status.HTTP_400_BAD_REQUEST)
            profile = serializer_class.save()
            Thread(target=send_email_with_confirmation, args=(profile,)).start()
            return Response(serializer_class.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)

    def list(self, request):
        profile = Profile.objects.get(user=request.user)
        response = Response(ProfileMaxSerializer(profile).data, status=status.HTTP_200_OK)
        return response

    def retrieve(self, request, pk=None):
        try:
            profile = Profile.objects.get(pk=pk)
        except ObjectDoesNotExist:
            return Response(data=ProfileMessages.PROFILE_DOES_NOT_EXIST, status=status.HTTP_404_NOT_FOUND)
        return Response(ProfileMedSerializer(profile).data, status=status.HTTP_200_OK)

    # Only for debug mode
    def destroy(self, request, pk=None):
        try:
            Profile.objects.get(user=request.user).delete()
            return Response(MainMessages.OK, status=status.HTTP_204_NO_CONTENT)
        except ObjectDoesNotExist:
            return Response(ProfileMessages.PROFILE_DOES_NOT_EXIST, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        if int(pk) != request.user.profile.id:
            return Response(ProfileMessages.NOT_ENOUGH_PERMISSIONS, status=status.HTTP_403_FORBIDDEN)
        profile = Profile.objects.get(pk=pk)
        serializer = ProfileMaxSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=False)
    def search(self, request):
        name = request.GET.get('name', None)
        if not name:
            return Response(ProfileMessages.EMPTY_SEARCH_MESAGE, status=status.HTTP_400_BAD_REQUEST)
        name = name.strip()
        if not name:
            return Response(ProfileMessages.UNSUPPORTED_SEARCH_MESAGE, status=status.HTTP_400_BAD_REQUEST)
        else:
            words = name.split()
            if len(words) == 1:
                name = words[0]
                profiles = Profile.objects.select_related('user').filter(
                    user__in=User.objects.filter(
                        Q(first_name__icontains=name) | Q(last_name__icontains=name) | Q(username__icontains=name)))
                return Response(ProfileMinSerializer(profiles, many=True).data, status=status.HTTP_200_OK)
            elif len(words) == 2:
                f_name = words[0]
                l_name = words[1]
                profiles = Profile.objects.select_related('user').filter(
                    user__in=User.objects.filter((Q(first_name__icontains=f_name) & Q(last_name__icontains=l_name)) | (
                            Q(first_name__icontains=l_name) & Q(last_name__icontains=f_name)))).distinct()
                serialized = ProfileMinSerializer(profiles, many=True)
                return Response(serialized.data, status=status.HTTP_200_OK)
