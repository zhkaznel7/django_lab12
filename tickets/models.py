from django.db import models


class Ticket(models.Model):
    class Priority(models.TextChoices):
        LOW = "low", "Төмен"
        NORMAL = "normal", "Орташа"
        HIGH = "high", "Жоғары"

    class Status(models.TextChoices):
        NEW = "new", "Жаңа"

    title = models.CharField("Тақырып", max_length=150)
    description = models.TextField("Сипаттама")
    priority = models.CharField("Басымдық", max_length=6, choices=Priority.choices, default=Priority.NORMAL)
    status = models.CharField("Күйі", max_length=3, choices=Status.choices, default=Status.NEW)

    def __str__(self):
        return self.title
