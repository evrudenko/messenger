from django.db import models
from django.contrib.auth import get_user_model


class Message(models.Model):
    sender = models.ForeignKey(get_user_model(), related_name='sent_messages',
                               related_query_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey(get_user_model(), related_name='received_messages',
                                  related_query_name='received_messages', on_delete=models.CASCADE)
    text = models.TextField(null=False, blank=False)
    datetime = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    edited = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    class Meta:
        indexes = [
            models.Index(fields=['sender', 'recipient'])
        ]


class UnfinishedMessage(models.Model):
    sender = models.ForeignKey(get_user_model(), related_name='+', on_delete=models.CASCADE, db_index=True)
    recipient = models.ForeignKey(get_user_model(), related_name='+', on_delete=models.CASCADE, db_index=True)
    text = models.TextField(null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['sender', 'recipient'], name='user_writes_only_one_message')
        ]
        indexes = [
            models.Index(fields=['sender', 'recipient'])
        ]
