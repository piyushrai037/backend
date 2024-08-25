from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import StudentViewSet, TeacherViewSet, ClassroomViewSet, ResourceViewSet, LectureViewSet, AttendanceViewSet, get_current_user, LoginView
from . import views
from .views import check_username
from .views import ClassroomLecturesView, ClassroomResourcesView
from .views import BlogViewSet

router = DefaultRouter()
router.register(r'students', StudentViewSet, basename='student')
router.register(r'teachers', TeacherViewSet, basename='teacher')
router.register(r'classrooms', ClassroomViewSet, basename='classroom')
router.register(r'resources', ResourceViewSet, basename='resource')
router.register(r'lectures', LectureViewSet, basename='lecture')
router.register(r'attendances', AttendanceViewSet, basename='attendance')
router.register(r'blogs', BlogViewSet, basename='blog')
urlpatterns = [
    path('', include(router.urls)),
    path('current-user/', get_current_user, name='current-user'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('classrooms/<int:classroom_id>/students/', views.classroom_students),
    path('check_username/<str:username>/', check_username, name='check_username'),
    path('classrooms/<int:classroom_id>/lectures/', ClassroomLecturesView.as_view(), name='classroom-lectures'),
    path('classrooms/<int:classroom_id>/resources/', ClassroomResourcesView.as_view(), name='classroom-resources'),

    path('login/', LoginView.as_view({'post': 'create'}), name='login'),
]