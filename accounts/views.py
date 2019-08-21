from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.schemas import SchemaGenerator
from rest_framework.views import APIView
from rest_framework.pagination import LimitOffsetPagination

from django.conf import settings

from .serializers import *
from .models import User, Affiliate, PasswordReset
from .utils import generate_token, send_email


class SignInView(APIView):
    """
    Sign In endpoint
    """
    permission_classes = (AllowAny,)
    serializer_class = SignInSerializer

    @swagger_auto_schema(
        operation_id='Sign In',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING)
            },
        ),
        security=[],
        tags=['Accounts'],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, _ = Token.objects.get_or_create(user=user)
            user_serializer = UserAuthSerializer(user)
            return Response({'token': token.key, 'user': user_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class SignUpView(APIView):
    """
    Sign Up endpoint
    """
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer

    @swagger_auto_schema(
        operation_id='Sign Up',
        operation_description="use 'ref' as optional request parameter for referral link",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password', 'password2'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'password2': openapi.Schema(type=openapi.TYPE_STRING),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING)
            },
        ),
        security=[],
        tags=['Accounts'],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            user_serializer = UserAuthSerializer(user)
            try:
                affiliate_code = request.query_params['ref']
                owner = User.objects.get(affiliate_code__iexact=affiliate_code)
                Affiliate.objects.create(owner=owner, member=user)
            except (KeyError, User.DoesNotExist) as e:
                pass
            return Response({'token': token.key, 'user': user_serializer.data},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserList(APIView):
    """
    Get list of all users
    """
    serializer_class = UserAuthSerializer
    pagination_class = LimitOffsetPagination

    @swagger_auto_schema(
        operation_id='Get users',
        security=[],
        tags=['Accounts'],
    )
    def get(self, request):
        users = User.objects.all()
        result_page = paginator.paginate_queryset(users, request)
        data = self.serializer_class(result_page, many=True).data
        return Response({'users': data}, status=status.HTTP_200_OK)


class UserUpdateView(APIView):
    """
    An endpoint for updating username, first name and last name
    """
    permission_classes = [IsAuthenticated]
    serializer_class = UserUpdateSerializer

    def get_object(self, queryset=None):
        return self.request.user

    @swagger_auto_schema(
        operation_id='Update Profile',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING)
            },
        ),
        security=[],
        tags=['Accounts'],
    )
    def put(self, request):
        serializer = self.serializer_class(instance=request.user, data=request.data, partial=True)
        if serializer.is_valid():
            user = serializer.save()
            user_serializer = UserAuthSerializer(user)
            return Response({'user': user_serializer.data}, status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# class UserUpdatePhotoView(APIView):
#     """
#     An endpoint for updating profile photo
#     """
#     permission_classes = [IsAuthenticated]

#     def get_object(self, queryset=None):
#         return self.request.user

#     @swagger_auto_schema(
#         operation_id='Update Profile Photo',
#         request_body=openapi.Schema(
#             type=openapi.TYPE_OBJECT,
#             required=['photo'],
#             properties={
#                 'photo': openapi.Schema(type=openapi.TYPE_FILE)
#             },
#         ),
#         security=[],
#         tags=['Accounts'],
#     )
#     def put(self, request, format=None):
#         photo_obj = request.FILES['photo']
#         try:
#             user = self.get_object()
#             user.photo = photo_obj
#             user.save()
#             photo_url = 'https://digifox.s3.amazonaws.com/media/%s' % user.photo
#             return Response({'photo_url': photo_url}, status=status.HTTP_200_OK)
#         except:
#             return Response({'error': 'something went wrong'}, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    """
    An endpoint for changing password
    """
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        return self.request.user

    @swagger_auto_schema(
        operation_id='Change Password',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['old_password', 'new_password', 'new_password2'],
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING),
                'new_password2': openapi.Schema(type=openapi.TYPE_STRING)
            },
        ),
        security=[],
        tags=['Accounts'],
    )
    def put(self, request):
        object = self.get_object()
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Check old password
            data = serializer.data
            if not object.check_password(data.get("old_password")):
                return Response({"error": ["Wrong password."]},
                                status=status.HTTP_400_BAD_REQUEST)
            # Check if new password is equal to old password
            if data.get("new_password") == data.get("old_password"):
                return Response({"error": "New password should not be equal to old password"},
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            elif data.get("new_password2") != data.get("new_password"):
                return Response({"error": "Passwords don't match."},
                                status=status.HTTP_400_BAD_REQUEST)
            object.set_password(data.get("new_password"))
            object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    """
    Forgot Password (generate reset_key and send email)
    """
    permission_classes = [AllowAny]
    serializer_class = ForgotPasswordSerializer

    @swagger_auto_schema(
        operation_id='Forgot Password',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING)
            },
        ),
        security=[],
        tags=['Accounts'],
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            # save recover token for user
            try:
                reset_password = PasswordReset.objects.get(user=user)
            except:
                # if user didn't has reset_key -> create reset_key
                reset_password = PasswordReset.objects.create(user=user)
            else:
                # if user already has reset_key -> update reset_key
                reset_password.reset_key = generate_token()
                reset_password.expired = False
                reset_password.save()

            if settings.production:
                reset_password_url = "localhost:8080/reset-password/?key={}".format(reset_password.reset_key)
                send_email(subject="Reset Password", user=user.username, template='reset-password.html',
                           from_email='admin@digifox.exchange',
                           content={'user': user, 'reset_url': reset_password_url})
            if settings.heroku:
                return Response({'reset_key': reset_password.reset_key}, status=status.HTTP_200_OK)

            return Response(status=status.HTTP_200_OK)
        else:
            return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordView(APIView):
    """
    Reset password
    """
    permission_classes = [AllowAny]
    serializer_class = ResetPasswordSerializer

    @swagger_auto_schema(
        operation_id='Reset Password',
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['new_password', 'new_password2'],
            properties={
                'new_password': openapi.Schema(type=openapi.TYPE_STRING),
                'new_password2': openapi.Schema(type=openapi.TYPE_STRING)
            },
        ),
        security=[],
        tags=['Accounts'],
    )
    def put(self, request):
        reset_key = request.query_params['key']

        try:
            reset_key_in_db = PasswordReset.objects.get(reset_key=reset_key, expired=False)
        except Exception as e:
            print(e)
            return Response({'error': 'Reset key is expired.'}, status=status.HTTP_400_BAD_REQUEST)

        if reset_key != reset_key_in_db.reset_key:
            return Response({'error': 'Reset key is not valid.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            if data.get("new_password2") != data.get("new_password"):
                return Response({"error": "Passwords don't match"},
                                status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(id=reset_key_in_db.user.id)
            except:
                return Response({'error': "User doesn't exist."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                user.set_password(data.get("new_password"))
                user.save()
                reset_key_in_db.expired = True
                reset_key_in_db.save()
                return Response(status=status.HTTP_204_NO_CONTENT)

        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
