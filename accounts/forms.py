from django import forms

from django.contrib.auth import (
authenticate,
get_user_model,
login,
logout,
)

User = get_user_model()

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                 raise forms.ValidationError("This user does not exist")
            if not user.check_password(password):

                raise forms.ValidationError("Incorrect password")
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active")
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField(label='Email address')
    password_rep = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'password_rep'


        ]

    # def clean_password(self):
    #     password = self.cleaned_data.get('password')
    #     if len(str(self.cleaned_data['password'])) < 6:
    #         raise forms.ValidationError("Password must been more then 6 symbols")
    #     elif len(str(self.cleaned_data['password'])) > 15:
    #         raise forms.ValidationError("Password must been less 15 symbols")
    #     return password
    #
    # def clean_password_rep(self):
    #     password_rep = self.cleaned_data.get('password_rep')
    #     if len(str(self.cleaned_data['password_rep'])) < 6:
    #         raise forms.ValidationError("Password must been more then 6 symbols")
    #     elif len(str(self.cleaned_data['password_rep'])) > 15:
    #         raise forms.ValidationError("Password must been less 15 symbols")
    #     return password_rep

    def clean(self):
        super(UserRegisterForm, self).clean()
        data = self.cleaned_data

        print(data)

        password = self.cleaned_data.get('password')
        if len(str(self.cleaned_data['password'])) < 6:
            raise forms.ValidationError("Password must been more then 6 symbols")
        elif len(str(self.cleaned_data['password'])) > 15:
            raise forms.ValidationError("Password must been less 15 symbols")
        password_rep = self.cleaned_data.get('password_rep')
        if len(str(self.cleaned_data['password_rep'])) < 6:
            raise forms.ValidationError("Password must been more then 6 symbols")
        elif len(str(self.cleaned_data['password_rep'])) > 15:
            raise forms.ValidationError("Password must been less 15 symbols")


        if data["password"] != data["password_rep"]:
            raise forms.ValidationError("Password must been are equal")
        return data

    # def clean_password_rep(self):
    #     password = forms.CharField(widget=forms.PasswordInput)
    #     password_rep = forms.CharField(widget=forms.PasswordInput)
    #     if password != password_rep:
    #         raise forms.ValidationError("Password must much")
    #
    #     return password

