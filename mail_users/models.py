from django.db import models


class MailUser(models.Model):
    email = models.EmailField(verbose_name="Email сотрудника для отправки уведомлений", unique=True)

    def __str__(self):
        return self.email
