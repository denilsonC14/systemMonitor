# monitoring/tests.py
from django.test import TestCase
from .utils import get_system_metrics

class SystemMonitorTests(TestCase):
    def test_system_metrics(self):
        metrics = get_system_metrics()
        self.assertIn('cpu_usage', metrics)
        self.assertIn('memory_total', metrics)