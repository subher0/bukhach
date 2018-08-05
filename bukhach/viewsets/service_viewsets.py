import redis
import os
import requests

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from bukhach.serializers.service_serializers import AppealSerializer


class AppealsView(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def check_request_number(request, r,  time):
        if 'HTTP_X_REAL_IP' in request.META:
            requests_number = r.get(request.META['HTTP_X_REAL_IP'])
            if requests_number is not None:
                requests_number = int(requests_number)
                requests_number += 1
                if requests_number > 3:
                    return False
                else:
                    r.set(request.META['HTTP_X_REAL_IP'], str(requests_number), time)
                    return True
            else:
                r.set(request.META['HTTP_X_REAL_IP'], '1', time)
                return True

    def post(self, request):
        redis_client = redis.StrictRedis(host='localhost', port=6379, db=4)
        if self.check_request_number(request, redis_client, 86400) is True:
            serializer = AppealSerializer(data=request.data)
            if serializer.is_valid():
                payload = {'user_id': '29497311',
                           'message': 'Тема: ' + str(serializer.data.pop('title')) + '\n\n\n' +
                                      'Email петуха: ' + str(serializer.data.pop('email')) + '\n\n\n' +
                                      'Сообщение: ' + str(serializer.data.pop('text')) + '\n\n\n' +
                                      'IP петуха: ' + str(request.META.get('HTTP_X_REAL_IP', 'gay')) + '\n\n\n' +
                                      'Номер высера: ' + str(int(redis_client.get(request.META['HTTP_X_REAL_IP']))) + '\n\n\n' +
                                      '===================================================',
                           'access_token': os.environ.get('VK_TOKEN'), 'v': '5.73'}
                vk_request = requests.post('https://api.vk.com/method/messages.send', params=payload)
                content = []
                content.append(vk_request)
                content.append(serializer.data)
                return Response(content)
            else:
                return Response(serializer.errors)
        else:
            return Response('fuck off')