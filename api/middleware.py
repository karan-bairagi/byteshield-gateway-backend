from django.http import JsonResponse
from .models import IPBlacklist,APIKEY,TrafficLog
from rest_framework import status
import hashlib
from django.core.cache import cache
import time
class SecurityByteshield:
    def __init__(self,get_response):
        self.get_response=get_response
    def __call__(self,request):
        method=request.method
        endpoint=request.path
        if (endpoint.startswith('/api/v1/auth/') or 
            endpoint.startswith('/api/v1/user/') or 
            endpoint.startswith('/api/v1/api-keys/') or
            endpoint.startswith('/api/v1/dashboard/') or
            endpoint.startswith('/api/v1/home/') or
            endpoint.startswith('/api/v1/api-key') or
            endpoint.startswith('/api/v1/api_key/') or
            endpoint.startswith('/admin/')):
            return self.get_response(request)


        start_time=time.time()
        user_ip=request.META.get('REMOTE_ADDR')
        if  IPBlacklist.objects.filter(ip_address=user_ip).exists():
            response_time=int((time.time() - start_time)*1000)
            return JsonResponse({
                'detail':'Your IP address has been banned from ByteShield.'
            },status=status.HTTP_403_FORBIDDEN)
        



        api_key=request.headers.get('X-ByteShield-Key')
        if not api_key:
            response_time=int((time.time() - start_time)*1000)
            return JsonResponse({  
                'detail':"Authentication credentials were not provided. Missing 'X-ByteShield-Key' header."         
            },status=status.HTTP_401_UNAUTHORIZED)
        secret_key=hashlib.sha3_256(api_key.encode()).hexdigest()
        try:
            user_api_key=APIKEY.objects.get(key_hash=secret_key,is_active=True)
            profile_obj=user_api_key.profile
        except APIKEY.DoesNotExist:
            response_time=int((time.time() - start_time) * 1000)
            return JsonResponse({
                'detail':"Invalid or inactive API Key provided."
            },status=status.HTTP_401_UNAUTHORIZED)
        
        redis_key=f"rate_limit_{user_ip}"
        cache.add(redis_key, 0, timeout=60)
        current_request=cache.incr(redis_key)
        if current_request>5:
            response_time=int((time.time() - start_time) * 1000)
            sv=TrafficLog.objects.create(profile=profile_obj,request_ip=user_ip,endpoint=endpoint,method=method,status_code=429,response_time_ms=response_time)
            return JsonResponse({
                'detail':'Too many requests. You have exceeded your limit of 5 requests per minute.'
            },status=status.HTTP_429_TOO_MANY_REQUESTS)
        response=self.get_response(request)
        response_time=int((time.time() - start_time) * 1000)
        sv=TrafficLog.objects.create(profile=profile_obj,request_ip=user_ip,endpoint=endpoint,method=method,status_code=response.status_code,response_time_ms=response_time)
        return response