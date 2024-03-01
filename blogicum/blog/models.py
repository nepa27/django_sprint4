from django.contrib.auth import get_user_model
from django.db import models

from .constants import SIZE_CUT_TITLE, MAX_LENGTH

User = get_user_model()


class CreatedAt(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Добавлено'
    )

    class Meta:
        abstract = True


class IsPublishModel(CreatedAt):
    is_published = models.BooleanField(
        default=True,
        verbose_name='Опубликовано',
        help_text='Снимите галочку, '
                  'чтобы скрыть публикацию.'
    )

    class Meta:
        abstract = True
        ordering = ('-pub_date',)


class Post(IsPublishModel):
    title = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Заголовок'
    )
    text = models.TextField(
        verbose_name='Текст')
    pub_date = models.DateTimeField(
        verbose_name='Дата и время публикации',
        help_text='Если установить дату и время в будущем'
                  ' — можно делать отложенные публикации.'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        'Location',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Категория'
    )

    image = models.ImageField(
        'Фото',
        upload_to='posts_images',
        blank=True
    )

    class Meta:
        default_related_name = 'posts'
        verbose_name_plural = 'Публикации'
        verbose_name = 'публикация'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.title[:SIZE_CUT_TITLE]


class Category(IsPublishModel):
    title = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Заголовок'
    )
    description = models.TextField(
        verbose_name='Описание'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Идентификатор',
        help_text='Идентификатор страницы для URL;'
                  ' разрешены символы латиницы, цифры,'
                  ' дефис и подчёркивание.'
    )

    class Meta(CreatedAt.Meta):
        verbose_name_plural = 'Категории'
        verbose_name = 'категория'

    def __str__(self):
        return self.title[:SIZE_CUT_TITLE]


class Location(IsPublishModel):
    name = models.CharField(
        max_length=MAX_LENGTH,
        verbose_name='Название места'
    )

    class Meta(CreatedAt.Meta):
        verbose_name_plural = 'Местоположения'
        verbose_name = 'местоположение'

    def __str__(self):
        return self.name[:SIZE_CUT_TITLE]


class Comment(CreatedAt):
    text = models.TextField(
        verbose_name='Текст комментария',
    )
    post = models.ForeignKey(
        'Post',
        on_delete=models.CASCADE,
        null=True,
        verbose_name='Пост',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Автор комментария',
    )

    class Meta(CreatedAt.Meta):
        default_related_name = 'comments'
        verbose_name_plural = 'Комментарии'
        verbose_name = 'комментарий'

    def __str__(self):
        return self.text[:SIZE_CUT_TITLE]
