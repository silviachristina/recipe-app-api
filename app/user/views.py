# (authentication, permissions) ManageUserView
from rest_framework import generics, authentication, permissions

# CreateTokenView
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

# CreateUserView and CreateTokenView
from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user"""
    serializer_class = UserSerializer
    # Specify the mechanisms of the authentication (cookies, token, session)
    authentication_classes = (authentication.TokenAuthentication,)
    # Level of access the user has
    # Make sure the user is authenticated
    permission_classes = (permissions.IsAuthenticated,)

    # Get the model from the logged in user
    def get_object(self):
        """Retrieve and return authenticated user"""
        return self.request.user
        # Because we have the authentication_classes it will assign the
        # authenticated user to the request
