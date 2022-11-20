from django.conf import settings
from django.core.validators import MinLengthValidator
from django.db import models


class Ad(models.Model):
    title = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(8),
        ],
        verbose_name="Наименование"
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ads',
        verbose_name="Автор объявления"
    )
    price = models.PositiveIntegerField(verbose_name="Цена")
    description = models.CharField(
        max_length=1000,
        null=True,
        blank=True,
        verbose_name="Описание"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания объявления"
    )
    image = models.ImageField(
        upload_to='ads/',
        null=True,
        blank=True,
        verbose_name="Фото")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'
        ordering = ('-created_at',)


class Comment(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Автор комментария"
    )
    text = models.CharField(
        max_length=1000,
        validators=[
            MinLengthValidator(8),
        ],
        verbose_name="Комментарий"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания комментария"
    )
    ad = models.ForeignKey(
        Ad,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name="Объявление"
    )

    def __str__(self):
        return self.text[:50]

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-created_at',)
