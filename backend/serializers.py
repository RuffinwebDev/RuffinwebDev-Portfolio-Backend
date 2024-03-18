from rest_framework import serializers
from .models import Sender, Message


"""The create method of SenderSerializer resolves the 400 error response that occurs as soon as the form is submitted.
This error only occurs when I include the unique constraint on the email field.
I still need to investigate how I can bypass this error message and use the constraint normally.
The message in the error console: 'sender with this email already exists.' """


class SenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sender
        fields = ("first_name", "last_name", "email")

    def create(self, validated_data):
        email = validated_data.get("email")
        sender = Sender.objects.filter(email=email).first()
        if sender:
            # If sender exists, return the existing instance
            return sender

        return super().create(validated_data)


class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ("message", "reply", "date", "message_sender")
