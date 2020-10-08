from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView
)
from services.views import (
    ContractListView,
    ContractCreateView,
    ReportListCreateView,
    ChatRoomView
)
from users.views import (
    ProfileView, UserView, ProfileLanguageView,
    ProfileServicesView, ProfileDetailView,
    TokenPairByEmailUser
)
from utils.messaging import ChatConsumer

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api-auth/', include('rest_framework.urls')),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path(
        'api/login',
        TokenPairByEmailUser.as_view(), name='token_obtain_pair'),
    path(
        'api/token/refresh/',
         TokenRefreshView.as_view(), name='token_refresh'),
    path('api/contracts/create',
        ContractCreateView.as_view(), name='contracts_create'),
    re_path(r'^api/contracts', ContractListView.as_view(), name='contracts'),
    path('api/profiles/profile/<int:pk>/',
         ProfileDetailView.as_view(), name='profile_detail'),
    re_path(r'^api/profiles/$', ProfileView.as_view(), name='profiles'),
    path('api/reports', ReportListCreateView.as_view(), name='reports'),
    path('api/users', UserView.as_view(), name='users'),
    path(
        'api/name/languages/',
        ProfileLanguageView.as_view(), name='languages'),
    path(
        'api/name/services/',
        ProfileServicesView.as_view(), name='services'),
    path('api/chatroom/<str:from_profile>/<str:to_profile>/',
         ChatRoomView.as_view()),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
