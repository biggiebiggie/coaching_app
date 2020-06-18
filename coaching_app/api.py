from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from .models import Student, Coach, Team
from .serialize import StudentSerializer, CoachSerializer, TeamSerializer

class StudentList(APIView):
    serializer_class = StudentSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "coaching_app/student_list.html"

    def get(self, request):
        queryset = Student.objects.all()
        return Response({'students': queryset})

class StudentDetail(APIView):
    serializer_class = StudentSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "coaching_app/student_detail.html"

    def get(self, request):
        queryset = Student.objects.all()
        return Response({'students': queryset})

class CoachList(generics.ListAPIView):
    serializer_class = CoachSerializer

    def get_queryset(self):
        queryset = Coach.objects.all()
        return queryset

class TeamList(generics.ListAPIView):
    serializer_class = TeamSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = "coaching_app/team_list.html"

    def get_queryset(self):
        queryset = Team.objects.all()
        return queryset

class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

    def get_queryset(self):
        queryset = Team.objects.all()
        return queryset

    #     queryset = Team.objects.all()
    #     obj_id = self.request.query_params.get('id')
    #     if obj_id:
    #         self.queryset = queryset.filter(id=obj_id)
    #     return queryset

    # def get_object(self):
    #     queryset = self.get_queryset()
    #     obj_id = self.request.get('id')
    #     print(self.request.query_params.get('id'))
    #     if obj_id:
    #         self.queryset = queryset.filter(id=obj_id)
    #     return queryset