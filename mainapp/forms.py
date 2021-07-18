from django import forms


class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    mobile_no1 = forms.CharField(max_length=14)
    mobile_no2 = forms.CharField(max_length=14, required=False)
    address_1 = forms.CharField(max_length=51)
    address_2 = forms.CharField(max_length=51, required=False)
    country = forms.CharField(max_length=30)
    state = forms.CharField(max_length=30)
    city = forms.CharField(max_length=30)
    zipcode = forms.CharField(max_length=30)
