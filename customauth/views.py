from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import get_object_or_404
from django.contrib.auth import get_user_model
from django.apps import apps
from django.db import transaction
from django.db.models import Q

from .serializers import (
    UserSerializer, UserSerializerWithToken, UserContactsSerializer
)


@api_view(['GET'])
def current_user(request):
    """
    Determine the current user by their token, and return their data
    """
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


class UserList(APIView):
    """
    Create a new user. It's called 'UserList' because normally we'd have a get
    method here too, for retrieving a list of all User objects.
    """
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        queryset = get_user_model().objects.filter(is_active=True)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = UserSerializerWithToken(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserContactsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        if user:
            serializer = UserContactsSerializer(user.contacts.all(), many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'auth': 'Unauthorized user'}, status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request):
        user = request.user
        serializer = UserContactsSerializer(data=request.data)
        if serializer.is_valid():
            contact_id = serializer.validated_data.get('id')
            contact = get_object_or_404(get_user_model(), pk=contact_id)
            user.contacts.add(contact)
            return Response({'success': '{} contacts {}'.format(user.username, contact.username)},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        user = request.user
        contact = get_object_or_404(get_user_model(), pk=pk)
        user.contacts.remove(contact)
        message_class = apps.get_model('message', 'Message')
        users_messages = message_class.objects.select_for_update().filter((Q(sender=user) & Q(recipient=contact)) |
                                                                          (Q(sender=contact) & Q(recipient=user)),
                                                                          deleted=False)
        with transaction.atomic():
            users_messages.update(deleted=True)
        return Response({'success': '{} does not contact {}'.format(user.username, contact.username)},
                        status=status.HTTP_204_NO_CONTENT)
