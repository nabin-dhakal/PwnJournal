from rest_framework.response import Response
from core.models import Writeup,Comments
from .serializers import WriteupSerializer, UserProfileSerializer,CommentSerializer
from rest_framework import generics, permissions
from django.views.decorators.csrf import ensure_csrf_cookie,csrf_exempt, csrf_protect
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import authentication_classes
from .authentication import CsrfExemptSessionAuthentication
from django.shortcuts import get_object_or_404


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def get_writeups(request):
    if request.method == 'GET':
        writeups = Writeup.objects.all()
        serializer = WriteupSerializer(writeups, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        serializer = WriteupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.profile  

@ensure_csrf_cookie
def get_csrf(request):
    return JsonResponse({'detail': 'CSRF cookie set'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def writeup_detail(request, pk):
    writeup = get_object_or_404(Writeup, pk=pk)
    serializer = WriteupSerializer(writeup)
    return Response(serializer.data)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def get_comments(request,pk):
    post = get_object_or_404(Writeup,pk=pk)
    if request.method == "GET":
        comment = Comments.objects.filter(onwriteup = post)
        serializer = CommentSerializer(comment,many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = CommentSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save(author= request.user,onwriteup= post)
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    

    