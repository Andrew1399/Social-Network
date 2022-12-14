from django import forms
from posts.models import Post, Comment


class PostModelForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}))
    class Meta:
        model = Post
        fields = ('content', 'image')


class CommentModelForm(forms.ModelForm):
    content = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Add a comment'}))
    class Meta:
        model = Comment
        fields = ('content',)
