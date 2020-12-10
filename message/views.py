from rest_framework import generics
from rest_framework import mixins
from rest_framework import permissions
from rest_framework.generics import get_object_or_404
from django.db.models import Q
from django.contrib.auth import get_user_model

from .models import Message
from .serializers import UpdateMessageSerializer, ListCreateMessageSerializer


class UpdateDestroyMessageAPIView(mixins.UpdateModelMixin,
                                  mixins.DestroyModelMixin,
                                  generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = UpdateMessageSerializer

    def put(self, request, pk, *args, **kwargs):
        return self.update(request=request, pk=pk, partial=True, *args, **kwargs)

    def delete(self, request, pk, *args, **kwargs):
        return self.destroy(request=request, pk=pk, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(sender=user, deleted=False)


class ListCreateMessageAPIView(mixins.ListModelMixin,
                               mixins.CreateModelMixin,
                               generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    serializer_class = ListCreateMessageSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request=request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request=request, *args, **kwargs)

    def get_queryset(self):
        user = self.request.user
        contact_id = self.request.query_params.get('contact_id', None)
        contact = get_object_or_404(get_user_model(), pk=contact_id)
        return Message.objects.filter((Q(sender=user) & Q(recipient=contact)) |
                                      (Q(sender=contact) & Q(recipient=user)), deleted=False).order_by('id')

    def perform_create(self, serializer):
        sender = self.request.user
        recipient = get_object_or_404(get_user_model(), pk=self.request.data.get('recipient_id'))
        sender.contacts.add(recipient)
        serializer.save(sender=sender, recipient=recipient)
