from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class MySocialAccountAdapter(DefaultSocialAccountAdapter):

    def populate_user(self, request, sociallogin, data):
        user = super().populate_user(request, sociallogin, data)
        
        if sociallogin.account.provider == 'google':
            extra_data = sociallogin.account.extra_data
            user.registration_method = 'google'
            user.email = user.email or extra_data.get('email')
            user.first_name = user.first_name or extra_data.get('given_name', '')
            user.last_name = user.last_name or extra_data.get('family_name', '')
            user.google_avatar_url = extra_data.get('picture', '')

        return user

