from django import forms
from django.contrib.auth import get_user_model
User = get_user_model()


class CommentForm(forms.Form):
    comment = forms.CharField(widget=forms.Textarea)


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        username = self.cleaned_data['username']

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователя с таким логином не существует')





class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = {
            'username',
            'password',
            'first_name',
            'last_name',
            'email'
        }

    def clean(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('Пользователь с таким именем уже существует')
