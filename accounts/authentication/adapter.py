from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):

    def populate_user(self, request, sociallogin, data):
        # Populate data seperti biasa
        user = super().populate_user(request, sociallogin, data)
        
        if sociallogin.account.provider == 'google':
            extra_data = sociallogin.account.extra_data
            user.registration_method = 'google'
            user.email = extra_data.get('email', user.email)
            user.first_name = extra_data.get('given_name', user.first_name)
            user.last_name = extra_data.get('family_name', user.last_name)
            user.google_avatar_url = extra_data.get('picture', '')

        return user
