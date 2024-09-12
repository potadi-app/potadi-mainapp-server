from rest_framework_simplejwt.tokens import RefreshToken
from allauth.socialaccount.models import SocialAccount
from accounts.models import User

def generate_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)
    refresh_token = str(refresh)
    return access_token, refresh_token
    
def get_user_data(user):
    try:
        social_account = SocialAccount.objects.get(user=user, provider='google')
        return {
            'email': social_account.extra_data.get('email', ''),
            'first_name': social_account.extra_data.get('given_name', ''),
            'last_name': social_account.extra_data.get('family_name', ''),
            'picture': social_account.extra_data.get('picture', ''),
        }
    except SocialAccount.DoesNotExist:
        return None
    
def get_or_create_user(user_data):
    try:
        user = User.objects.get(email=user_data['email'])
    except User.DoesNotExist:
        user = User.objects.create_user(
            email=user_data['email'],
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            registration_method='google',
            avatar=user_data.get('picture', None),
        )
    else:
        if user.registration_method != 'google':
            user.registration_method = 'google'
            user.save()
    return user