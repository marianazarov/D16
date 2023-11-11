from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)


class Ad(models.Model):
    CATEGORY_CHOICES = [
        ('Tanks', 'Танки'),
        ('Healers', 'Хилы'),
        ('DD', 'ДД'),
        ('Merchants', 'Торговцы'),
        ('Guild Masters', 'Гилдмастеры'),
        ('Quest Givers', 'Квестгиверы'),
        ('Blacksmiths', 'Кузнецы'),
        ('Tanners', 'Кожевники'),
        ('Potion Makers', 'Зельевары'),
        ('Spell Masters', 'Мастера заклинаний'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='uploads/', blank=True, null=False)
    upload = models.FileField(upload_to='uploads/', blank=True, null=False)

    def __str__(self):
        return f'{self.title}{self.text[:50000]}{self.author}{self.category}'

    def get_absolute_url(self):
        return reverse('ad', kwargs={'pk': self.pk})


class Response(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    message = models.TextField()
    is_accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"Response to: {self.ad.title}"
