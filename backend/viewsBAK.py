import sys

from .serializers import SenderSerializer, MessageSerializer
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from .models import Sender, Message
from .utilities import send_html_email
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
import logging

# logger = logging.getLogger(__name__)
logger = logging.getLogger("backend")


# Main Contact form view.
class SenderView(generics.CreateAPIView):
    queryset = Sender.objects.all()
    serializer_class = SenderSerializer


""" CreateMessageAPIView takes the data from a Message record and adds the information to the database.
It overrides the generic create method to ensure proper handling of Message records in cases where
the associated email already exists in the database.
This prevents duplicate emails from being added and allows all messages sent from that
specific email to be queried more efficiently."""
#
#
# class CreateMessageAPIView(generics.CreateAPIView):
#     queryset = Message.objects.all()
#     serializer_class = MessageSerializer
#
#     def create(self, request, *args, **kwargs):
#         print("Create method reached")
#         try:
#             # Extract data from the request
#             sender_name = request.data.get("name")
#             sender_email = request.data.get("email")
#             message_content = request.data.get("message")
#
#             if not sender_email or not message_content:
#                 return Response({"detail": "Email and message are required."}, status=status.HTTP_400_BAD_REQUEST)
#
#             # Get or create the Sender object based on email
#             sender, created = Sender.objects.get_or_create(email=sender_email, defaults={'name': sender_name})
#
#             # Create the message using the sender as the foreign key
#             message = Message.objects.create(
#                 message=message_content,
#                 message_sender=sender  # Pass the actual sender object here, not the ID
#             )
#
#
#             logger.debug("Debug message: Sender data is %s", sender)
#             logger.info("Info message: Message was successfully created.")
#             logger.error("Error message: Something went wrong with %s", sender)
#             print(sender)
#
#             # Serialize the message for the response
#             serializer = self.get_serializer(message)
#             headers = self.get_success_headers(serializer.data)
#             return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
#
#         except Exception as e:
#             # Handle any exceptions gracefully
#             return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#


class CreateMessageAPIView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        try:
            # Extract data from the request
            sender_name = request.data.get("name")
            sender_email = request.data.get("email")
            message_content = request.data.get("message")

            if not sender_email or not message_content:
                return Response({"detail": "Email and message are required."}, status=status.HTTP_400_BAD_REQUEST)

            # Get or create the Sender object based on email
            sender, created = Sender.objects.get_or_create(email=sender_email, defaults={'name': sender_name})

            # Create the message using the sender as the foreign key
            message = Message.objects.create(
                message=message_content,
                message_sender=sender  # Pass the actual sender object here, not the ID
            )


            logger.debug("Debug message: Sender data is %s", sender)
            logger.info("Info message: Message was successfully created.")
            logger.error("Error message: Something went wrong with %s", sender)
            print(sender)

            # Serialize the message for the response
            serializer = self.get_serializer(message)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

        except Exception as e:
            # Handle any exceptions gracefully
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


""" SenderViewSet handles CRUD operations for the Sender model,
providing endpoints to create, retrieve, update, and delete sender information.
It includes additional methods to ensure proper handling of new sender creation
and returns error responses gracefully in case of validation or database errors."""


class SenderViewSet(viewsets.ModelViewSet):
    queryset = Sender.objects.all()
    serializer_class = SenderSerializer

    def perform_create(self, serializer):
        serializer.save()

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )

        except Exception as e:
            # Handle any exceptions gracefully
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
