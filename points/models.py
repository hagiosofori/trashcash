from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

# Create your models here.

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    wallet = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    phone_number = models.PositiveSmallIntegerField(default=0)


    @receiver(post_save, sender=User)
    def create_or_update_client(sender, instance, created, **kwargs):
        if created:
            Client.objects.create(user=instance)
        instance.client.save()

    def __str__(self):
        return self.user.username


class Rate(models.Model):
    name = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name



class Trash_Submission(models.Model):
    weight = models.DecimalField(max_digits=10, decimal_places=3, default=0.00)
    user = models.ForeignKey(Client, on_delete=models.CASCADE)
    earning = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'submission by {0} on {1}'.format(self.user, self.created_on)
    

    # @receiver(post_save, sender=Trash_Submission)
    # def send_sms_to_client(sender, instance, created, **kwargs):
    #     if created:
    #         rate = Rate.objects.get(name="TC rate").value
    #         trash_submission.earning = trash_submission.weight * rate
    #         trash_submission.user.wallet += trash_submission.earning
    #         trash_submission.save()
    #         trash_submission.user.save()

    #         Client.objects.create(user=instance)
    #     instance.client.save()