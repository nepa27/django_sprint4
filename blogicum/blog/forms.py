import datetime
from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        now_date = datetime.date.today().strftime('%Y-%m-%d')
        now_time = datetime.datetime.now().time().strftime('%H:%M')
        kwargs.update(initial={
            'pub_date': f'{now_date} {now_time}'
        })
        super(PostForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'pub_date': forms.DateTimeInput(
                attrs={'type': 'datetime'},
                format='%Y-%m-%d %H:%M',
            )
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text', )
