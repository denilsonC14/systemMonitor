# monitoring/models.py

from django.db import models

class SystemMetrics(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    cpu_usage = models.FloatField()
    cpu_freq = models.FloatField(null=True)
    cpu_temp = models.FloatField(null=True)
    memory_total = models.BigIntegerField()
    memory_used = models.BigIntegerField()
    memory_free = models.BigIntegerField()
    memory_buffers = models.BigIntegerField(null=True)
    memory_cached = models.BigIntegerField(null=True)
    swap_total = models.BigIntegerField(null=True)
    swap_used = models.BigIntegerField(null=True)
    disk_total = models.BigIntegerField(null=True)
    disk_used = models.BigIntegerField(null=True)
    disk_free = models.BigIntegerField(null=True)
    disk_percent = models.FloatField(null=True)

class ProcessInfo(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    pid = models.IntegerField()
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, null=True)
    status = models.CharField(max_length=20, null=True)
    cpu_percent = models.FloatField()
    memory_percent = models.FloatField()
    memory_rss = models.BigIntegerField(null=True)
    memory_vms = models.BigIntegerField(null=True)
    create_time = models.CharField(max_length=50, null=True)
    io_read_bytes = models.BigIntegerField(null=True)
    io_write_bytes = models.BigIntegerField(null=True)
    
class NetworkMetrics(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True)
    bytes_sent = models.BigIntegerField()
    bytes_recv = models.BigIntegerField()
    packets_sent = models.BigIntegerField()
    packets_recv = models.BigIntegerField()
    errin = models.IntegerField(null=True)
    errout = models.IntegerField(null=True)
    dropin = models.IntegerField(null=True)
    dropout = models.IntegerField(null=True)
    bytes_sent_speed = models.BigIntegerField(null=True)  # bytes/s
    bytes_recv_speed = models.BigIntegerField(null=True)  # bytes/s
    
    def __str__(self):
        return f"Network metrics at {self.timestamp}"

class NetworkInterface(models.Model):
    network_metrics = models.ForeignKey(NetworkMetrics, related_name='interfaces', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    mac = models.CharField(max_length=50, null=True)
    ip_address = models.CharField(max_length=50, null=True)
    is_up = models.BooleanField(default=False)
    speed = models.IntegerField(null=True)  # Mbps
