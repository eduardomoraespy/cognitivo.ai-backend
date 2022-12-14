from django.db import models
import datetime

class Metric(models.Model):
    track_name = models.CharField(
        verbose_name='Track Name',
        max_length=255,
    ) 
    n_citacoes = models.IntegerField()
    size_bytes = models.BigIntegerField()
    price = models.DecimalField(
        max_digits=999, 
        decimal_places=2
    )
    prime_genre = models.CharField(
        verbose_name='App Genre',
        max_length=30
    )


    class Meta:
        db_table = 'metric'


class LogMetric(models.Model):
    metric_id = models.ForeignKey(
        Metric,
        verbose_name='Metric',
        db_column='metric_id',
        on_delete=models.PROTECT
    )
    hours = models.CharField(
        verbose_name='hours',
        max_length=194,
        null=False,
        blank=False,
        default=datetime.datetime.now()
    )

    class Meta:
        db_table = 'log_metric'