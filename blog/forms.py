from django import forms

from .models import News
from .models import Comment


class NewsCreateForm(forms.ModelForm):
    """
    Форма добавления статей на сайте
    """

    class Meta:
        model = News
        fields = ('title', 'slug', 'category', 'short_content', 'content', 'photo', 'is_published')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'uk-form-control',
                'autocomplete': 'off'
            })


class NewsUpdateForm(NewsCreateForm):
    """
    Форма обновления статьи на сайте, наследуем форму создания статьи и прибавляем к ней доп поля
    """

    class Meta:
        model = News
        fields = NewsCreateForm.Meta.fields + ('updater', 'fixed')

    def __init__(self, *args, **kwargs):
        """
        Обновление стилей формы под Bootstrap
        """
        super().__init__(*args, **kwargs)

        self.fields['fixed'].widget.attrs.update({
            'class': 'uk-form-check-input'
        })


class CommentCreateForm(forms.ModelForm):
    """
    Форма добавления комментариев к статьям
    """
    parent = forms.IntegerField(widget=forms.HiddenInput, required=False)
    content = forms.CharField(label='', widget=forms.Textarea(
        attrs={'cols': 30, 'rows': 5, 'placeholder': 'Комментарий', 'class': 'uk-form-control'}))

    class Meta:
        model = Comment
        fields = ('content',)
