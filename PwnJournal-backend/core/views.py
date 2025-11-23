from django.contrib.auth import authenticate, login, logout, get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.hashers import make_password
from .models import UserProfile, CustomUser
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.http import require_http_methods
from django.db import transaction
from api.serializers import UserProfileSerializer
from rest_framework.decorators import api_view,authentication_classes
from api.authentication import CsrfExemptSessionAuthentication

User = get_user_model()


def login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        user = authenticate(request, username=data.get('username'), password=data.get('password'))
        if user is not None:
            login(request, user)
            return JsonResponse({'message': 'Login Successful'}, status=200)
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return JsonResponse({'error': 'POST Method Required'}, status=400)


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'message': 'Logged out successfully'})
    return JsonResponse({'error': 'POST Method Required'}, status=400)


def current_user_view(request):
    if request.user.is_authenticated:
        return JsonResponse({'username': request.user.username})
    return JsonResponse({'error': 'Not logged in'}, status=401)


def register_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            email = data.get('email')
            password = data.get('password')
            confirm_password = data.get('confirm_password')

            if not all([username, email, password, confirm_password]):
                return JsonResponse({'error': 'All Fields Are Required!!'}, status=400)
            if password != confirm_password:
                return JsonResponse({'error': 'Password did not match'}, status=400)
            if User.objects.filter(email=email).exists():
                return JsonResponse({'error': 'Email Already Exists'}, status=400)
            if User.objects.filter(username=username).exists():
                return JsonResponse({'error': 'Username Already Exists'}, status=400)

            user = CustomUser.objects.create(
                username=username,
                email=email,
                password=make_password(password)
            )

            # Create blank profile (remove DP=None if DP is not nullable)
            UserProfile.objects.create(user=user, full_name='', contact='')

            return JsonResponse({'Success': 'User registered successfully'}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'POST Method Required'}, status=400)

@api_view([ 'POST'])
def update_user(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    user = request.user
    profile, _ = UserProfile.objects.get_or_create(user=user)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON data'}, status=400)

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    contact_number = data.get('contact_number')
    full_name = data.get('full_name')

    if username and username != user.username:
        if CustomUser.objects.filter(username=username).exclude(id=user.id).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        user.username = username

    if email and email != user.email:
        if CustomUser.objects.filter(email=email).exclude(id=user.id).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)
        user.email = email

    if password or confirm_password:
        if not (password and confirm_password):
            return JsonResponse({'error': 'Both password and confirm_password are required'}, status=400)
        if password != confirm_password:
            return JsonResponse({'error': 'Passwords do not match'}, status=400)
        user.set_password(password)

    with transaction.atomic():
        user.save()
        if full_name:
            profile.full_name = full_name
        if contact_number:
            profile.contact = contact_number
        profile.save()

    return JsonResponse({'success': 'Profile updated successfully'})


@api_view(['GET'])
def get_user_profile(request):
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Authentication required'}, status=401)

    user = request.user
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)

    serializer = UserProfileSerializer(profile)
    return JsonResponse(serializer.data, safe=True)
