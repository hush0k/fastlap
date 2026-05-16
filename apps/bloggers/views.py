# apps/bloggers/views.py
"""
Views for the bloggers app.
"""

# Django REST Framework
from django.utils.translation import gettext as _
from rest_framework.response import Response
from rest_framework.views import APIView


class BloggerViewSet(APIView):
    """
    Placeholder for Blogger ViewSet.
    """

    def get(self, request):
<<<<<<< HEAD
        return Response({"message": _("Blogger endpoints coming soon")})
=======
        return Response({"message": "Blogger endpoints coming soon"})
>>>>>>> 0e6107e1c089943cbfda7566fea209a804af52ae
