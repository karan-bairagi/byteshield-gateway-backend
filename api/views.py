from django.shortcuts import render
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import UserProfile,APIKEY,TrafficLog
from django.db.models import Avg,Count
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from .serializer import SignupSerializer,LoginSerializer,APIKeySerializername,UserProfileSerializer,APIKeySerializers
from rest_framework import status
import secrets,hashlib
from django.db.models.functions import TruncHour
from datetime import datetime, timedelta
# Create your views here.
class Signup(APIView):
    def post(self,request):
        user_data=SignupSerializer(data=request.data)
        if user_data.is_valid():
            user_input=user_data.validated_data
            username=user_input['username']
            password=user_input['password']
            email=user_input['email']
            user=User.objects.create_user(username=username,password=password,email=email)
            user_profile=UserProfile.objects.create(user=user)
            token=RefreshToken.for_user(user)
            return Response({
                'user_data':user_data.data,
                'access_token':str(token.access_token),
                'refresh_token':str(token),
            },status=status.HTTP_201_CREATED)
        else:
            return Response({
                'errors':user_data.errors
            },status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):
    def post(self,request):
        user_data=LoginSerializer(data=request.data)
        if user_data.is_valid():
            user_input=user_data.validated_data
            username=user_input['username']
            password=user_input['password']
            user=authenticate(username=username,password=password)
            if user is not None:
                token=RefreshToken.for_user(user)
                return Response({
                    'user_data':user_data.data,
                    'access_token':str(token.access_token),
                    'refresh_token':str(token),
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'detail':'Invalid Username or Password Please try again.'
                },status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({
                'errors':user_data.errors
            },status=status.HTTP_400_BAD_REQUEST)
class GenerateAPIKey(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def post(self,request):
        try:
            user_key_name=APIKeySerializername(data=request.data)
            if user_key_name.is_valid():
                user_key=user_key_name.validated_data['key_name']
                user=request.user
                api_key=f"bs_live_{secrets.token_hex(32)}"
                secret_key=hashlib.sha3_256(api_key.encode()).hexdigest()
                userprofile=user.userprofile
                sv=APIKEY.objects.create(profile=userprofile,key_name=user_key,key_hash=secret_key)
                return Response({
                    'key_name':user_key,
                    'api_key':api_key,
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'errors':user_key_name.errors,
                },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'detail':f'Something Went Wrong {e}',
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class SecurityScannerDashboard(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def get(self,request):
        try:
            user=request.user
            profile_obj=user.userprofile
            user_logs=TrafficLog.objects.filter(profile=profile_obj)
            count=user_logs.count()
            average=user_logs.aggregate(average=Avg('response_time_ms'))
            status_groups=user_logs.values('status_code').annotate(group_count=Count('id'))
            return Response({
                'count':count,
                'avg':average,
                'status_group':status_groups,
                'username':user.username,
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'detail':f'Something Went Wrong {e}',
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class SecurityScannerCharts(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self, request):
        try:
            login_profile = request.user.userprofile
            past_24_hours = datetime.now() - timedelta(hours=24)
            chart_data = (
                TrafficLog.objects
                .filter(profile=login_profile, timestamp__gte=past_24_hours)
                .annotate(hour=TruncHour('timestamp'))
                .values('hour')
                .annotate(hits=Count('id'))
                .order_by('hour')
            )
            final_chart_list = []
            for entry in chart_data:
                formatted_time = entry['hour'].strftime('%I:%M %p')
                final_chart_list.append({
                    "time": formatted_time,
                    "hits": entry['hits']
                })
            return Response({
                'graph_data':final_chart_list,
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'detail':f'Something Went Wrong {e}',
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
class UserprofileUpdate(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def get(self,request):
        user=request.user.userprofile
        find=user.company
        if find:
            return Response({
                'current_name':find,
            },status=status.HTTP_200_OK)
        else:
            return Response({
                'current_name':''
            },status=status.HTTP_404_NOT_FOUND)
    def patch(self,request):
        try:
            user=request.user
            user_data=UserProfileSerializer(data=request.data)
            if user_data.is_valid():
                user_input=user_data.validated_data['company_name']
                sv=UserProfile.objects.get(user=user)
                sv.company=user_input
                sv.save()
                return Response({
                    'company_name':user_input,
                },status=status.HTTP_200_OK)
            else:
                return Response({
                    'errors':user_data.errors,
                },status=status.HTTP_400_BAD_REQUEST)
        except UserProfile.DoesNotExist:
            return Response({
                'detail':'User Does Not Exists or unauthorized',
            },status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'detail':f'Something Went Wrong {e}',
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class InactiveView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def patch(self,request):
        key_id=request.query_params.get('key_id')
        try:    
            if not key_id:
                return Response({
                    'detail':'Query Parameter is Required',
                },status=status.HTTP_400_BAD_REQUEST)
            find=request.user.userprofile
            api_id=APIKEY.objects.get(id=key_id,profile=find)
            api_id.is_active=not api_id.is_active
            api_id.save()
            status_str = "Active" if api_id.is_active else "Inactive"
            return Response({
                'is_active':status_str,
            }, status=status.HTTP_200_OK)
        except APIKEY.DoesNotExist:
            return Response({
                'detail':f'API_KEY with ID {key_id} does not exist or unauthorized.'
            },status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'detail':f'Something Went Wrong {e}',
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AllAPIKey(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def get(self,request):
        try:
            user=request.user.userprofile
            find=APIKEY.objects.filter(profile=user)
            serializer=APIKeySerializers(find,many=True)
            return Response({
                'user_all_api_key':serializer.data,
            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'detail':f'Something Went Wrong {e}',
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class DeleteAPIView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def delete(self,request):
        try:
            user=request.user.userprofile
            key_id=request.query_params.get('key_id')
            find=APIKEY.objects.get(id=key_id,profile=user)
            find.delete()
            return Response({
                'detail':'API KEY Deleted Successfully',
            },status=status.HTTP_200_OK)
        except APIKEY.DoesNotExist:
            return Response({
                'detail':f'API KEY with ID {key_id} Does not Exist or unauthorized'
            },status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'detail':f'Something Went Wrong {e}',
            },status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


class ExternalTrafficChechView(APIView):
    def post(self,request):
        return Response({
            'detail':'Successfully Passesd',
        },status=status.HTTP_200_OK)