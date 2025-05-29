from rest_framework import generics
from user_app.serializers import (
    RegisterSerializer
)
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction, IntegrityError
from user_app.models import Cash, CustomUser
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction, IntegrityError
from rest_framework.permissions import IsAuthenticated
from user_app.serializers import MyPageSerializer

# API Views

# 1. RegisterView와 RegisterAPIView의 차이점 설명

# RegisterView는 Django REST framework의 generics.CreateAPIView를 상속받아
# 회원가입 처리를 매우 간단하게 구현할 수 있습니다.
# serializer_class만 지정하면, POST 요청 시 자동으로 serializer의 유효성 검사 및 저장(save)까지 처리해줍니다.
# 즉, 커스텀 로직이 필요 없고, 단순한 생성(Create) API에 적합합니다.

# class RegisterView(generics.CreateAPIView):
#     serializer_class = UserSignupSerializer
#     permission_classes = []  # 누구나 접근 가능

# RegisterAPIView는 APIView를 상속받아 post 메서드를 직접 구현합니다.
# 이 방식은 회원가입 시 추가적인 비즈니스 로직(예: 트랜잭션 처리, Cash 객체 생성, JWT 토큰 발급 등)이 필요할 때 사용합니다.
# 즉, 회원가입과 동시에 여러 작업을 처리하거나, 예외처리, 커스텀 응답이 필요할 때 적합합니다.


class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        try:
            if serializer.is_valid():
                with transaction.atomic():  # 💥 여기!
                    user = serializer.save()
                    Cash.objects.create(user=user, balance=0)
                    # 회원가입 성공 시 JWT 토큰 발급
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        "message": "Registration successful",
                        "access_token": str(refresh.access_token),
                        "refresh_token": str(refresh)
                    }, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            return Response({"error": "이미 존재하는 이메일입니다."}, status=status.HTTP_400_BAD_REQUEST)


class MyPageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = MyPageSerializer(request.user)
        return Response(serializer.data)


# Create api_views.py module


# class CookieLoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')

#         user = authenticate(request, username=email, password=password)  # 또는 email=email
#         if user is not None:
#             refresh = RefreshToken.for_user(user)
#             request.session['otp_verified'] = False  # ✅ 세션에 OTP 상태 유지

#             response = JsonResponse({'message': '로그인 성공'})
#             response.set_cookie('access_token', str(refresh.access_token), httponly=True, secure=True, samesite='Lax', max_age=3600)
#             response.set_cookie('refresh_token', str(refresh), httponly=True, secure=True, samesite='Lax', max_age=7*24*3600)
#             return response
#         else:
#             return JsonResponse({'error': '이메일 또는 비밀번호가 틀렸습니다'}, status=401)


# logger = logging.getLogger("transaction")

# @csrf_exempt
# def health_check(request):
#     return HttpResponse("OK", content_type="text/plain", status=200)

# class MainAPIView(APIView):
#     def get(self, request):
#         return Response({"message": "Welcome to the API main endpoint."})


# class LoginAPIView(APIView):
# #     permission_classes = [AllowAny]

# #     def post(self, request):
# #         serializer = LoginSerializer(data=request.data)
        
# #         if serializer.is_valid():
# #             user = serializer.validated_data['user']
# #             refresh = RefreshToken.for_user(user)
# #             request.session['otp_verified'] = False  # OTP 인증 상태는 세션에 유지
            
# #             return Response({
# #                 'message': '로그인 성공!',
# #                 'access_token': str(refresh.access_token),
# #                 'refresh_token': str(refresh),
# #             }, status=200)
        
# #         return Response(serializer.errors, status=400)
        

# class PasswordChangeAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         # 사용자로부터 받은 데이터
#         current_password = request.data.get('current_password')
#         new_password = request.data.get('new_password')
#         confirm_password = request.data.get('confirm_password')

#         # 현재 비밀번호 확인
#         if not request.user.check_password(current_password):
#             return Response({"error": "현재 비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

#         # 새 비밀번호와 확인 비밀번호 일치 여부 확인
#         if new_password != confirm_password:
#             return Response({"error": "새 비밀번호와 확인 비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

#         # 비밀번호 변경
#         request.user.set_password(new_password)
#         request.user.save()

#         return Response({"message": "비밀번호가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)



# class OTPVerifyAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         user = request.user
#         otp_code = request.data.get('otp_code')

#         if not user.otp_secret:
#             return Response({"error": "OTP 설정이 안 되어 있습니다."}, status=400)

#         totp = pyotp.TOTP(user.otp_secret)

#         if totp.verify(otp_code):
#             # OTP 인증 성공 시 새로운 JWT 토큰 발급
#             refresh = RefreshToken.for_user(user)
#             # OTP 인증 여부를 토큰에 포함
#             refresh['otp_verified'] = True
            
#             return Response({
#                 "message": "인증 성공",
#                 "access_token": str(refresh.access_token),
#                 "refresh_token": str(refresh)
#             }, status=200)
#         else:
#             return Response({"error": "OTP 인증 실패"}, status=400)



# class UnregisterAPIView(APIView):
#     permission_classes = [IsAuthenticated]

#     def delete(self, request):
#         serializer = UnregisterPasswordCheckSerializer(data=request.data, context={'request': request})
#         serializer.is_valid(raise_exception=True)  # ❗ 여기서 비번 검증함

#         request.user.delete()
#         return Response({"message": "회원탈퇴 완료"}, status=status.HTTP_204_NO_CONTENT)
