from rest_framework import serializers

from .models import Message


class UpdateMessageSerializer(serializers.ModelSerializer):
    def update(self, instance, validated_data):
        instance.text = validated_data.get('text', instance.text)
        instance.read = validated_data.get('read', instance.read)
        instance.edited = validated_data.get('edited', instance.edited)
        instance.deleted = validated_data.get('deleted', instance.deleted)
        instance.save()
        return instance

    class Meta:
        model = Message
        fields = (
            'id',
            'recipient_id',
            'text',
            'datetime',
            'read',
            'edited',
            'deleted',
        )
        extra_kwargs = {
            'recipient_id': {'read_only': True},
            'text': {'required': True},
            'datetime': {'read_only': True},
        }


class ListCreateMessageSerializer(serializers.ModelSerializer):
    recipient_id = serializers.IntegerField(required=True)

    class Meta:
        model = Message
        fields = (
            'id',
            'recipient_id',
            'text',
            'datetime',
            'read',
            'edited',
        )
        extra_kwargs = {
            'id': {'read_only': True},
            'text': {'required': True},
            'datetime': {'required': True},
            'read': {'read_only': False},
            'edited': {'read_only': False},
        }
