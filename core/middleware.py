from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth import logout

class BlockedUserMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.path.startswith('/login'):
            return self.get_response(request)

        if request.user.is_authenticated:
            if hasattr(request.user, 'block_profiles') and request.user.block_profiles.is_blocked:

                # 🔥 prevent duplicate messages
                if not request.session.get('blocked_message_shown'):
                    messages.error(
                        request,
                        "Well… this is awkward 😬 Your account is currently blocked. Drop us a mail or call us — we promise we’re nice!"
                    )
                    request.session['blocked_message_shown'] = True

                logout(request)
                return redirect('login')

        return self.get_response(request)