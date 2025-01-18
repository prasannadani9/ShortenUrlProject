from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ShortUrlApp.helpers import access_log_entry, shorten_url
from ShortUrlApp.models import AccessLogs, UrlDataMainModel
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import get_object_or_404

from ShortUrlApp.serializers import AccessLogsSerializer

class ShortenUrlAPIView(APIView):
    def post(self, request):
        main_url = request.data.get("main_url", "")
        if not main_url or len(main_url)==0:
            return Response({
                "message" : "Failed",
                "data" : "Main URL can not be empty."
            },
            status = status.HTTP_400_BAD_REQUEST
            )
        expiry_in_hours = request.data.get("expiry_in_hours", "")
        if expiry_in_hours:
            if type(expiry_in_hours) != int:
                return Response({
                    "message" : "Failed",
                    "data" : "Expiry hours should be in integers"
                },
                status = status.HTTP_400_BAD_REQUEST
                )
            expiry_in_mins = expiry_in_hours * 60
        else:
            expiry_in_mins = 24*60
        short_url, expiry_time = shorten_url(main_url, expiry_in_mins)
        try:
            current_data = UrlDataMainModel.objects.get(main_url = main_url)
        except:
            current_data = []
        current_time = timezone.now() + timedelta(hours = 5, minutes= 30)
        if current_data:
            if current_data.expiry_time < current_time :
                current_data.delete()
                create_instance = UrlDataMainModel.objects.create(
                    main_url = main_url,
                    short_url = short_url,
                    expiry_time = expiry_time,
                    creation_time = current_time
                )
                id = create_instance.id
                creation_time = create_instance.creation_time
                response_short_url = create_instance.short_url
                response_expiry_time = create_instance.expiry_time
            else:
                id = current_data.id
                creation_time = current_data.creation_time
                response_short_url = current_data.short_url
                response_expiry_time = current_data.expiry_time

        else:
            create_instance = UrlDataMainModel.objects.create(
                main_url = main_url,
                short_url = short_url,
                expiry_time = expiry_time,
                creation_time = current_time
            )
            id = create_instance.id
            creation_time = create_instance.creation_time
            response_short_url = create_instance.short_url
            response_expiry_time = create_instance.expiry_time
        response_data = {
            'message' : 'Success',
            'data': {
                'id' : id,
                'main_url' : main_url,
                'short_url' : response_short_url,
                'expiry_time' : response_expiry_time,
                'creation_time' : creation_time
            }
        }
        return Response(response_data, status = status.HTTP_201_CREATED)

class GetMainUrlByShortAPIView(APIView):
    def get(self, request, *args, **kwargs):
        short_url = request.GET.get("short_url", "")
        try:
            main_url_data = UrlDataMainModel.objects.get(short_url = short_url)
        except:
            return Response(
                {
                    "message" : "Failed",
                    "data" : "This short url does not exist"
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        current_time = timezone.now() + timedelta(hours = 5, minutes= 30)
        if main_url_data.expiry_time < current_time:
            response_data = {
                "message" : "Failed",
                "data" : "The provided short URL has been expired."
            }
            return Response(
                response_data,
                status=status.HTTP_412_PRECONDITION_FAILED
            )
        main_url = main_url_data.main_url
        access_log_entry(request, short_url)
        response_data = {
            "message" : "Success",
            "data" : {
                "main_url" : main_url
            }
        }
        return Response(
            response_data, status = status.HTTP_200_OK
        )
    
class GetAnalyticsOfUrlAPIView(APIView):
    def get(self, request, *args, **kwargs):
        short_url = request.GET.get("short_url", "")
        try:
            url_data = get_object_or_404(UrlDataMainModel, short_url=short_url)
            analytics_data = AccessLogs.objects.filter(short_url = url_data).values('id', 'ip_address', 'timestamp')
            serializer = AccessLogsSerializer(analytics_data, many=True)
            response_body = {
                'message' : 'Success',
                'count' : len(serializer.data),
                'body' : serializer.data
            }
        except:
            response_body = {
                'message' : 'Failed',
                'count' : '',
                'body' : 'Short URL did not match'
            }
        return Response(
            response_body,
            status = status.HTTP_200_OK
        )