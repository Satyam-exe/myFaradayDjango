from django import forms


class LoginForm(forms.Form):
    email = forms.EmailField(
        label='Email'
    )
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )


class SignupForm(forms.Form):
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
             attrs={
                 'class': 'form-control'
             }
        )
    )

    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control'
            }
        )
    )

    mobile_number = forms.CharField(
        max_length=10,
        required=True
    )

    password = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        )
    )


class ResetPasswordForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address'
            }
        )
    )


class ConfirmResetPasswordForm(forms.Form):
    password = forms.CharField(
        max_length=254,
        required=True,
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Please enter your new password'
            }
        )
    )
