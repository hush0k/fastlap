# apps/bloggers/views.py
"""
Views for the bloggers app.
"""

# Django REST Framework
from rest_framework.response import Response
from rest_framework.views import APIView


class BloggerViewSet(APIView):
    """
    Placeholder for Blogger ViewSet.
    """

    def get(self, request):
        return Response({"message": "Blogger endpoints coming soon"})
