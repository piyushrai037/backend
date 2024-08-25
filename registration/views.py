from django.contrib.auth import authenticate
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Student, Teacher
from .serializers import StudentSerializer, TeacherSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import viewsets, permissions
from .models import Student, Teacher, Classroom, Resource, Lecture, Attendance
from .serializers import StudentSerializer, TeacherSerializer, ClassroomSerializer, ResourceSerializer, LectureSerializer, AttendanceSerializer
from rest_framework.decorators import action
from rest_framework import status
from django.http import JsonResponse
from .models import Classroom, Student
from django.http import JsonResponse
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Classroom, Lecture, Resource
from .serializers import LectureSerializer, ResourceSerializer
from django.http import Http404
from rest_framework import viewsets
from .models import Blog
from .serializers import BlogSerializer

class BlogViewSet(viewsets.ModelViewSet):
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        print('get_queryset called')
        queryset = Blog.objects.all()
        print('Initial queryset:', queryset)
        author = self.request.query_params.get('author', None)
        print('Author query param:', author)
        if author is not None:
            queryset = queryset.filter(author__username=author.strip())
        print('Filtered queryset:', queryset)
        return queryset

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class ClassroomLecturesView(APIView):
    def get(self, request, classroom_id):
        try:
            classroom = Classroom.objects.get(id=classroom_id)
        except Classroom.DoesNotExist:
            raise Http404

        lectures = Lecture.objects.filter(classroom=classroom)
        serializer = LectureSerializer(lectures, many=True)
        return Response(serializer.data)

class ClassroomResourcesView(APIView):
    def get(self, request, classroom_id):
        try:
            classroom = Classroom.objects.get(id=classroom_id)
        except Classroom.DoesNotExist:
            raise Http404

        resources = Resource.objects.filter(classroom=classroom)
        serializer = ResourceSerializer(resources, many=True)
        return Response(serializer.data)
def check_username(request, username):
    if User.objects.filter(username=username).exists():
        return JsonResponse({'exists': True})
    else:
        return JsonResponse({'exists': False})
def classroom_students(request, classroom_id):
    try:
        classroom = Classroom.objects.get(id=classroom_id)
        students = list(classroom.students.values())
        print("Students:", students)  # Print the students data
        return JsonResponse(students, safe=False)
    except Classroom.DoesNotExist:
        print("Classroom not found")  # Print the error message
        return JsonResponse({'error': 'Classroom not found'}, status=404)
class ClassroomViewSet(viewsets.ModelViewSet):
    serializer_class = ClassroomSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.AllowAny()]
        elif self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]
    def get_queryset(self):
        username = self.request.query_params.get('teacher__user__username', None)
        if username is not None:
            teacher = Teacher.objects.get(user__username=username)
            return Classroom.objects.filter(teacher=teacher)
        else:
            return Classroom.objects.all()

    def perform_create(self, serializer):
        serializer.save(teacher=self.request.user.teacher)
class ResourceViewSet(viewsets.ModelViewSet):
    serializer_class = ResourceSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if hasattr(self.request.user, 'teacher'):
            return Resource.objects.filter(classroom__in=self.request.user.teacher.classrooms.all())
        else:
            return Resource.objects.filter(classroom__in=self.request.user.student.classroom_set.all())

class LectureViewSet(viewsets.ModelViewSet):
    serializer_class = LectureSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if hasattr(self.request.user, 'teacher'):
            return Lecture.objects.filter(classroom__in=self.request.user.teacher.classrooms.all())
        else:
            return Lecture.objects.filter(classroom__in=self.request.user.student.classroom_set.all())
class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_teacher:
            return Attendance.objects.filter(classroom__in=self.request.user.teacher.classrooms.all())
        else:
            return Attendance.objects.filter(student=self.request.user.student)
class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return Student.objects.filter(user=self.request.user)
    @action(detail=True, methods=['get'])
    def classrooms(self, request, pk=None):
        student = self.get_object()
        classrooms = student.classroom_set.all()
        serializer = ClassroomSerializer(classrooms, many=True)
        return Response(serializer.data)
    @action(detail=True, methods=['post'])
    def join_classroom(self, request, pk=None):
        student = self.get_object()
        classroom_code = request.data.get('classroom_code')
        try:
            classroom = Classroom.objects.get(code=classroom_code)
        except Classroom.DoesNotExist:
            return Response({'status': 'Classroom not found'}, status=status.HTTP_404_NOT_FOUND)
        classroom.students.add(student)
        return Response({'status': 'Classroom joined'}, status=status.HTTP_200_OK)


class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        return Teacher.objects.filter(user=self.request.user)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(viewsets.ViewSet):
    permission_classes = [permissions.AllowAny]

    def create(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_type = 'student' if hasattr(user, 'student') else 'teacher'
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user_type': user_type,
                'user_id': user.id,  # Add this line

                'status': 'Logged in',
            })
        else:
            return Response({"status": "Invalid credentials"}, status=400)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_current_user(request):
    user = request.user
    if hasattr(user, 'student'):
        serializer = StudentSerializer(user.student)
    else:
        serializer = TeacherSerializer(user.teacher)
    return Response(serializer.data)