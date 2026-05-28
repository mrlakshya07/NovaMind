"""
Authentication service for Supabase Auth integration.
Handles JWT token management, user validation, and session operations.
"""

import os
from functools import wraps
from flask import session, request, jsonify
from supabase_client import supabase

def get_current_user():
    """
    Retrieve authenticated user from Flask session.
    """

    user_id = session.get('user_id')
    access_token = session.get('access_token')

    if not user_id or not access_token:
        return None

    try:

        response = supabase.auth.get_user(access_token)

        user = response.user

        if user:

            return {
                'id': user.id,
                'email': user.email,
                'user_id': user_id
            }

    except Exception as e:

        print(f"Token verification error: {e}")

        return None

    return None

def login_required(f):
    """
    Decorator to protect routes that require authentication.
    Returns 401 if user is not authenticated.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if user is None:
            return jsonify({
                'success': False,
                'message': 'Authentication required'
            }), 401
        return f(*args, **kwargs)
    return decorated_function


def signup(email, password, username):
    """
    Create a new user account with Supabase Auth.
    
    Args:
        email: User email
        password: User password
        username: Display username
        
    Returns:
        dict with success status and message
    """
    try:
        # Sign up with Supabase Auth
        response = supabase.auth.sign_up({
            "email": email,
            "password": password
        })
        
        user = response.user
        
        if user is None:
            return {
                'success': False,
                'message': 'Signup failed. Please try again.'
            }
        
        # Store user profile in users table
        supabase.table("users").insert({
            "id": user.id,
            "username": username,
            "email": email
        }).execute()
        
        return {
            'success': True,
            'message': 'Signup successful. Please log in.',
            'user_id': user.id
        }
    
    except Exception as e:
        error_msg = str(e)
        if 'already registered' in error_msg.lower():
            return {
                'success': False,
                'message': 'Email is already registered.'
            }
        return {
            'success': False,
            'message': f'Signup error: {error_msg}'
        }


def login(email, password):
    """
    Authenticate user with email and password.
    
    Args:
        email: User email
        password: User password
        
    Returns:
        dict with success status, message, and user data
    """
    try:
        response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": password
        })
        
        user = response.user
        session_data = response.session
        
        if not user or not session_data:
            return {
                'success': False,
                'message': 'Invalid email or password.'
            }
        
        # Store tokens in Flask session
        session['user_id'] = user.id
        session['access_token'] = session_data.access_token
        session['refresh_token'] = session_data.refresh_token
        
        return {
            'success': True,
            'message': 'Login successful',
            'user_id': user.id,
            'email': user.email
        }
    
    except Exception as e:
        error_msg = str(e)
        if 'Invalid login credentials' in error_msg or 'invalid' in error_msg.lower():
            return {
                'success': False,
                'message': 'Invalid email or password.'
            }
        return {
            'success': False,
            'message': f'Login error: {error_msg}'
        }


def logout():
    """
    Logout user and clear session.
    
    Returns:
        dict with success status
    """
    try:
        access_token = session.get('access_token')
        if access_token:
            supabase.auth.sign_out()
    except Exception as e:
        print(f"Logout error: {e}")
    
    # Clear session
    session.clear()
    
    return {
        'success': True,
        'message': 'Logout successful'
    }
