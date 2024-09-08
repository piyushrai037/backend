from rest_framework import serializers, viewsets, permissions
from django.contrib.auth.models import User
from .models import Student, Teacher
from rest_framework import serializers, viewsets, permissions
from django.contrib.auth.models import User
from .models import Student, Teacher, Classroom, Resource, Lecture, Attendance
from rest_framework import serializers
from .models import Blog
from rest_framework import serializers
from .models import Blog, User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email', 'first_name', 'last_name']  # Add 'first_name' and 'last_name'

class BlogSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)

    class Meta:
        model = Blog
        fields = ['id', 'title', 'content', 'author', 'created_at', 'updated_at', 'title_image']  # Include title_image field
class ClassroomSerializer(serializers.ModelSerializer):
    students = serializers.PrimaryKeyRelatedField(many=True, queryset=Student.objects.all(), required=False)

    class Meta:
        model = Classroom
        fields = '__all__'

class ResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = '__all__'

class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lecture
        fields = '__all__'

class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']  # Add 'first_name' and 'last_name'
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank.")
        return value

    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank.")
        return value

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank.")
        return value

class StudentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Student
        fields = ['user', 'enrollment', 'photo', 'branch','id']

    def validate_enrollment(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank.")
        return value

    def validate_branch(self, value):
        if not value:
            raise serializers.ValidationError("This field may not be blank.")
        return value


    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        return Student.objects.create(user=user, **validated_data)

class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:
        model = Teacher
        fields = ['id','user', 'department']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        return Teacher.objects.create(user=user, **validated_data)
class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    permission_classes = [permissions.IsAuthenticated]
    # rest of the code

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer
    permission_classes = [permissions.IsAuthenticated]
   
