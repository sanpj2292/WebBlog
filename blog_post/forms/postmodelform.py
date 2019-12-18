from django import forms
from blog_post.models import Post as PostModel


class PostModelForm(forms.ModelForm):

    class Meta:
        model = PostModel
        fields = ['title', 'content', 'publish', 'author']

    def __init__(self, *args, **kwargs):
        super(PostModelForm, self).__init__(*args, **kwargs)
        self.fields['content'].required = False
        self.fields['author'].required = False

    def clean_title(self):
        if not self.cleaned_data.get('title'):
            raise forms.ValidationError(message='No Title Provided, please provided a Title for Post')
        title = self.cleaned_data.get('title')
        if len(title) > 200:
            raise forms.ValidationError(
                message='Character count exceeds the limit value of 200, reduce the character count')
        return title
