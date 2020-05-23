from biz.models import Biz, Hours
from comments.models import Comment
from rest_framework import viewsets, permissions, authentication
from biz.serializers import BizSerializer, HoursSerializer
from comments.serializers import CommentSerializer
from biz.permissions import HasGroupPermission
from rest_framework.permissions import DjangoModelPermissions

# Biz Viewset


class BizViewSet(viewsets.ModelViewSet):
    queryset = Biz.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = [HasGroupPermission]
    required_groups = {
        "list": ["__all__"],
        "create": ["member", "biz_post"],
        "upate": ["member", "biz_edit"],
        "partial_update": ["member", "biz_edit"],
        "destroy": ["member", "admin"],
    }

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    serializer_class = BizSerializer


class HoursViewSet(viewsets.ModelViewSet):
    queryset = Hours.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = [HasGroupPermission]
    required_groups = {
        "list": ["__all__"],
        "create": ["member"],
        "upate": ["member"],
        "partial_update": ["member"],
        "destroy": ["member", "admin"],
    }

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)

    serializer_class = HoursSerializer


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = [HasGroupPermission]
    required_groups = {
        "list": ["__all__"],
        "create": ["member"],
        "upate": ["member"],
        "partial_update": ["member"],
        "destroy": ["member", "admin"],
    }

    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)
