from django import forms

class LoginForm(forms.Form):
    serial_no = forms.CharField(max_length=100, label="Serial Number")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")