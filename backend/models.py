from django.db import models


# Website user who sent the contact message.
class Sender(models.Model):
    name = models.CharField(max_length=200, null=False, default="")
    # Emails could be hashed before saving.
    email = models.EmailField(max_length=200, default="")


# The contact message sent by a website user.
class Message(models.Model):
    message = models.CharField(max_length=200, default="")
    email = models.ForeignKey(
        Sender, on_delete=models.CASCADE
    )
    date = models.DateTimeField(auto_now_add=True, blank=True)
    reply = models.BooleanField(default=True)
