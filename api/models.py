from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    company=models.CharField(null=True,max_length=50,blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table='userprofile'

class APIKEY(models.Model):
    profile=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    key_name=models.CharField(max_length=60)
    key_hash=models.CharField(db_index=True,max_length=100,unique=True)
    is_active=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table='apikey'
class IPBlacklist(models.Model):
    ip_address=models.GenericIPAddressField(unique=True)
    reason=models.CharField(max_length=255)
    banned=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table='ipblacklist'
class TrafficLog(models.Model):
    profile=models.ForeignKey(UserProfile,on_delete=models.CASCADE)
    request_ip=models.GenericIPAddressField()
    endpoint=models.CharField(max_length=255)
    method=models.CharField(max_length=10)
    status_code=models.IntegerField()
    response_time_ms=models.IntegerField()
    timestamp=models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table='trafficlog'
        indexes=[models.Index(fields=['request_ip','timestamp'])]