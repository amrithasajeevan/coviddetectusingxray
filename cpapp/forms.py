import re
from datetime import date

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from cpapp.models import PatientLogin, Login, DoctorLogin, PharmacyLogin, Prescription, DoctorSchedule, AddStock, \
    DocChat, MedicineSelect, Bill, upload_img, Sendtest_result ,Chat , Chat_add


class LoginForm(UserCreationForm):
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput, label="password")
    password2 = forms.CharField(widget=forms.PasswordInput, label=" Confirm password")

    class Meta:
        model = Login
        fields = ("username", "password1", "password2")

#phone number validations
def phone_number_validator(value):
    if not re.compile(r'^[6-9]\d{9}$').match(value):
        raise ValidationError('This is invalid Phone Number')

class PatientRegister(forms.ModelForm):
    contact_no=forms.CharField(validators=[phone_number_validator])
    class Meta:
        model = PatientLogin
        fields = ('name', 'age', 'gender', 'address', 'contact_no', 'email')


class DoctorRegister(forms.ModelForm):
    phone_no = forms.CharField(validators=[phone_number_validator])
    class Meta:
        model = DoctorLogin
        fields = ('name','qualification','experience','address','phone_no','email','pic')


class PharmacyRegister(forms.ModelForm):
    phone_no = forms.CharField(validators=[phone_number_validator])
    class Meta:
        model = PharmacyLogin
        fields = ('registration_no', 'name','Location', 'address', 'phone_no', 'email','pic')

class DateInput(forms.DateInput):
    input_type = 'date'
#prescription
class Prescriptionform(forms.ModelForm):
    date = forms.DateField(widget=DateInput)
    class Meta:
        model = Prescription
        fields = ('patient','date','medicine_details')
#Scheduling
class Scheduling(forms.ModelForm):
    date = forms.DateField(widget=DateInput)
    class Meta:
        model = DoctorSchedule
        fields = ('date','doctor_name','start_time','end_time')
#add stock to pharmacy
class Stock(forms.ModelForm):
    arrival_date = forms.DateField(widget=DateInput)
    expiry_date = forms.DateField(widget=DateInput)
    class Meta:
        model = AddStock
        fields = ('medicine_name','batch_no','number_of_tablets','arrival_date','expiry_date','price','photo')
        #send result to doctor
class Send_Result(forms.ModelForm):
    date=forms.DateField(widget=DateInput)
    class Meta:
        model = Sendtest_result
        fields = ('date','doctor_name','xray','disease')

class DateInput(forms.DateInput):
    input_type = 'date'
#chatwithdoctor
class ChatWithDoctor(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=Login.objects.filter(is_doctor=True))
    date = forms.DateField(widget=DateInput)
    class Meta:
        model = DocChat
        fields = ('user','date','message')




class chatform(forms.ModelForm):
    date=forms.DateField(widget=DateInput)
    class Meta:
        model =DocChat
        fields=('chat','date')

#select medicine
class selectmedicine(forms.ModelForm):
    class Meta:
        model = MedicineSelect
        fields = ('medicine_image','medicine_name','price','pharmacy_name')

class Billing(forms.ModelForm):
    class Meta:
        model=Bill
        fields = ('medicine_name','number_of_strips','amount')

class upload_form(forms.ModelForm):
    class Meta:
        model= upload_img
        fields=['img_upload']


class ChatForm(forms.ModelForm):
    class Meta:
        model = Chat
        fields = ('desc',)

class CHATForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput)
    class Meta:
        model = Chat_add
        fields = ('subject', 'Enquiry', 'date')