from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from .models import CustomUser


class LoginView(View):
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'accounts/login.html')
    
    def post(self, request):
        # Handle AJAX request
        if request.headers.get('Content-Type') == 'application/json':
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({'success': True, 'message': 'Login successful'})
            return redirect('dashboard')
        else:
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({'success': False, 'message': 'Invalid credentials'}, status=400)
            messages.error(request, 'Invalid username or password')
            return render(request, 'accounts/login.html')


class RegisterView(View):
    
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'accounts/register.html')
    
    def post(self, request):
        # Handle AJAX request
        if request.headers.get('Content-Type') == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        password2 = data.get('password2')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        
        # Validation
        errors = {}
        if not username:
            errors['username'] = 'Username is required'
        elif CustomUser.objects.filter(username=username).exists():
            errors['username'] = 'Username already exists'
        
        if not email:
            errors['email'] = 'Email is required'
        elif CustomUser.objects.filter(email=email).exists():
            errors['email'] = 'Email already exists'
        
        if not password:
            errors['password'] = 'Password is required'
        elif len(password) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        
        if password != password2:
            errors['password2'] = 'Passwords do not match'
        
        if errors:
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({'success': False, 'errors': errors}, status=400)
            for field, error in errors.items():
                messages.error(request, error)
            return render(request, 'accounts/register.html')
        
        # Create user
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        
        login(request, user)
        
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'success': True, 'message': 'Registration successful'})
        
        messages.success(request, 'Registration successful!')
        return redirect('dashboard')


class LogoutView(View):
    
    def get(self, request):
        logout(request)
        return redirect('login')


class ProfileView(LoginRequiredMixin, View):
    
    def get(self, request):
        return render(request, 'accounts/profile.html', {'user': request.user})
    
    def post(self, request):
        user = request.user
        
        # Handle AJAX request
        if request.headers.get('Content-Type') == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
        
        user.first_name = data.get('first_name', user.first_name)
        user.last_name = data.get('last_name', user.last_name)
        user.email = data.get('email', user.email)
        user.phone = data.get('phone', user.phone)
        user.address = data.get('address', user.address)
        user.save()
        
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'success': True, 'message': 'Profile updated successfully'})
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')


class ChangePasswordView(LoginRequiredMixin, View):
    
    def get(self, request):
        return render(request, 'accounts/change_password.html')
    
    def post(self, request):
        user = request.user
        
        # Handle AJAX request
        if request.headers.get('Content-Type') == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
        
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        new_password2 = data.get('new_password2')
        
        errors = {}
        
        if not user.check_password(old_password):
            errors['old_password'] = 'Current password is incorrect'
        
        if not new_password or len(new_password) < 8:
            errors['new_password'] = 'New password must be at least 8 characters'
        
        if new_password != new_password2:
            errors['new_password2'] = 'New passwords do not match'
        
        if errors:
            if request.headers.get('Content-Type') == 'application/json':
                return JsonResponse({'success': False, 'errors': errors}, status=400)
            for field, error in errors.items():
                messages.error(request, error)
            return render(request, 'accounts/change_password.html')
        
        user.set_password(new_password)
        user.save()
        update_session_auth_hash(request, user)
        
        if request.headers.get('Content-Type') == 'application/json':
            return JsonResponse({'success': True, 'message': 'Password changed successfully'})
        
        messages.success(request, 'Password changed successfully!')
        return redirect('profile')
