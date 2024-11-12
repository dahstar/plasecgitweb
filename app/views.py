# views.py
from django.shortcuts import render
from django.http import JsonResponse
from .models import User

def main(request):
    """Render the main page."""
    return render(request, 'main.html')

def add_credit(request):
    """Add 100 credits to the specified user ID."""
    user_id = request.GET.get('user_id')  # Get the user ID from the request parameters
    
    if not user_id:
        # Return an error if the user_id parameter is missing
        return JsonResponse({'status': 'error', 'message': 'User ID not provided'})
    
    try:
        # Try to find the user by user_id
        user = User.objects.get(user_id=user_id)
        # Increment the user's credits by 100
        user.credits += 100
        user.save()  # Save the updated user record in the database
        
        # Return success response with the updated credits
        return JsonResponse({'status': 'success', 'new_credits': user.credits})
    except User.DoesNotExist:
        # Return an error if the user is not found
        return JsonResponse({'status': 'error', 'message': 'User not found'})
