from django import forms

from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "body"]
        widgets = {"body": forms.Textarea(attrs={"rows": 4})}
