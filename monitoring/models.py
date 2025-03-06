from django.db import models

class SystemMetrics(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    cpu_usage = models.FloatField()
    memory_total = models.BigIntegerField()
    memory_used = models.BigIntegerField()
    memory_free = models.BigIntegerField()

class ProcessInfo(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    pid = models.IntegerField()
    name = models.CharField(max_length=100)
    cpu_percent = models.FloatField()
    memory_percent = models.FloatField()
    
class NetworkMetrics(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    bytes_sent = models.BigIntegerField()
    bytes_recv = models.BigIntegerField()
    packets_sent = models.BigIntegerField()
    packets_recv = models.BigIntegerField()
    
    def __str__(self):
        return f"Network metrics at {self.timestamp}"
