from .serializers import SenderSerializer, MessageSerializer
from rest_framework import generics, viewsets, status
from rest_framework.response import Response
from .models import Sender, Message
from .utilities import send_html_email
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


# Main Contact form view.
class SenderView(generics.CreateAPIView):
    queryset = Sender.objects.all()
    serializer_class = SenderSerializer


""" CreateMessageAPIView takes the data from a Message record and adds the information to the database.
It overrides the generic create method to ensure proper handling of Message records in cases where
the associated email already exists in the database.
This prevents duplicate emails from being added and allows all messages sent from that
specific email to be queried more efficiently."""


class CreateMessageAPIView(generics.CreateAPIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Extract sender data from the request and create a new sender object.
            sender_name = request.data.get("name")
            sender_email = request.data.get("email")
            sender = Sender.objects.filter(email=sender_email).first()

            # If sender doesn't exist, create a new one
            if not sender:
                sender = Sender.objects.create(
                    name=sender_name,
                    email=sender_email,
                )

            # Save the message with the sender
            serializer.save(message_sender=sender)

            headers = self.get_success_headers(serializer.data)
            return Response(
                serializer.data, status=status.HTTP_201_CREATED, headers=headers
            )

        except Exception as e:
            # Handle any exceptions gracefully
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# This view takes the data from a Message record and sends reply email to the associated Contact record.
class SendReplyEmailAPIView(generics.CreateAPIView):
    queryset = Sender.objects.all()
    serializer_class = SenderSerializer

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            # Extract sender data from the request
            sender_name = serializer.validated_data.get("name")
            sender_email = serializer.validated_data.get("email")
            general_subject = "Thanks for visiting Ruffinweb!"
            email_template = "reply_email.html"

            # Context data for the email template
            email_context = {
                "sender_name": sender_name,
                "sender_email": sender_email,
                "subject": general_subject,
            }

            # Send the HTML email
            send_html_email(
                subject=general_subject,
                template_name=email_template,
                context=email_context,
                recipient_list=[sender_email],
            )

            # Return success response
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except Exception as e:
            # Handle any exceptions gracefully
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


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
