from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from .serializers import GenerateExamTokenaSerializer
from .services.exam_service import ExamService
from rest_framework import status

class GenerateExamTokenAPIView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, exam_id):
        try:
            serializer = GenerateExamTokenaSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            student_id, valid_minutes = request.data.get("student_id"), request.data.get("valid_minutes")
            token = ExamService.generate_token(exam_id, student_id, valid_minutes)

            return Response(
                {
                    "token": token,
                    "message": "Token generated successfully"
                },
                status = status.HTTP_201_CREATED
            )
        except ValueError as e:
            return Response(
                {"details": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


    
