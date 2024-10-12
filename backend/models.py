from django.db import models


# Website user who sent the contact message.
class Sender(models.Model):
    # Emails could be hashed before saving.
    email = models.EmailField(max_length=200, default="")
    name = models.CharField(max_length=200, null=False, default="")


# The contact message sent by a website user.
class Message(models.Model):
    message = models.CharField(max_length=200, default="")
    message_sender = models.ForeignKey(
        Sender, on_delete=models.CASCADE,  default=1
    )  # A primary key NOT a string/email
    date = models.DateTimeField(auto_now_add=True, blank=True)

