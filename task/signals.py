from django.core.mail import send_mail
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
User = get_user_model()

#for register
@receiver(post_save,sender=User)
def send_welcome_email(sender,instance,created,**kwargs):
    if created:
        send_mail(
            subject='Welcome to Task Manager!',
            message=f'Hello {instance.email}, thank you for registering.',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[instance.email],
            fail_silently=False,
        )

#for task details
from .models import Task
@receiver(post_save,sender=Task)
def send_task_notification(sender,instance,created,**kwargs):
    if created:
        print("Task owner:",instance.owner)
        print("Task owner type:",type(instance.owner))
        print("Task owner email:",repr(getattr(instance.owner,'email', None)))
        subject = f"New Task Created:{instance.title}"
        message = (
            f"Hello {getattr(instance.owner,'email','User')},\n\n"
            f"Your task has been created successfully!\n\n"
            f"Title:{instance.title}\n"
            f"Description:{instance.description}\n"
            f"Due Date:{instance.due_date}\n\n"
            "Please make sure to complete it before the due date."
        )
        recipient=getattr(instance.owner,'email',None)
        if recipient:
            send_mail(
                subject,
                message,
                'spmacavity@example.com',
                [recipient],
                fail_silently=False,
            )
            print(f"email sent to: {recipient}")
        else:
            print(" email not sent.")



