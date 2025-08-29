import logging

from rest_framework import status
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

from .exceptions import TokeExpiredError, TokenAlreadyUsedError, TokenNotFound
from .models import ExamAccessToken
from .serializers import AccessExamSerializer, GenerateExamTokenaSerializer
from .services.exam_service import ExamService
from .tasks import send_token

logger = logging.getLogger(__name__)


class GenerateExamTokenAPIView(APIView):
    """
    API endpoint for admins to generate an exam access token for a student.
    Sends token via email asynchronously
    """

    permission_classes = [IsAdminUser]

    def post(self, request, exam_id):
        try:
            serializer = GenerateExamTokenaSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            student_id, valid_minutes = request.data.get(
                "student_id"
            ), request.data.get("valid_minutes")
            token, student = ExamService.generate_token(
                exam_id, student_id, valid_minutes
            )
            send_token.delay(token, student.email)
            return Response(
                {"token": token, "message": "Token generated successfully"},
                status=status.HTTP_201_CREATED,
            )
        except ValueError as e:
            logger.error(
                f"Token generation faild for exam_id={exam_id}=>{e}", exc_info=True
            )
            return Response({"details": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(
                f"Unexpected error in generating exam token=>{e}", exc_info=True
            )
            return Response(
                {"details": "An unexpected error occurred"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


@api_view(["GET"])
@throttle_classes([AnonRateThrottle])
def AccessExamView(request, token):
    """
    API endpoint to validate and access an exam using token
    """
    try:
        validate, tokenObj = ExamService.token_related_validation(token)
        if validate:
            serializer = AccessExamSerializer(tokenObj)
            return Response(serializer.data)
    except TokenNotFound as e:
        logger.warning(f"Token not found: {token}=>{e}", exc_info=True)
        return Response({"message": str(e)}, status=status.HTTP_404_NOT_FOUND)
    except TokenAlreadyUsedError as e:
        logger.warning(f"Token already used: {token}=>{e}", exc_info=True)
        return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except TokeExpiredError as e:
        logger.warning(f"Token expired: {token}=>{e}", exc_info=True)
        return Response({"message": str(e)}, status=status.HTTP_410_GONE)
    except Exception as e:
        logger.exception(
            f"Unexpected error occure during accessing token", exc_info=True
        )
        return Response(
            {"message": "Internal server error"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
