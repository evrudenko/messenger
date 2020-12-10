from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import get_user_model
from django.apps import apps
from django.db.models import Q


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'avatar',
        )


class UserSerializerWithToken(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'password',
            'avatar',
            'token',
        )
        extra_kwargs = {
            'avatar': {'required': False},
        }


class UserContactsSerializer(serializers.ModelSerializer):
    username = serializers.CharField(read_only=True)
    avatar = serializers.ImageField(read_only=True)
    last_message_text = serializers.SerializerMethodField()

    def get_last_message_text(self, obj):
        message_class = apps.get_model('message', 'Message')
        last_message = message_class.objects.filter(Q(sender=obj) | Q(recipient=obj)).last()
        if last_message:
            return last_message.text
        return None

    class Meta:
        model = get_user_model()
        fields = (
            'id',
            'username',
            'avatar',
            'last_message_text'
        )
