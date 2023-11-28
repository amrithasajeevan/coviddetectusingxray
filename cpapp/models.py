from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class Login(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_pharmacy = models.BooleanField(default=False)


class PatientLogin(models.Model):
    user = models.OneToOneField(Login, on_delete=models.CASCADE,related_name="patient")
    name = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    contact_no = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.name


class DoctorLogin(models.Model):
    user = models.OneToOneField(Login, on_delete=models.CASCADE,related_name='doctor')
    name = models.CharField(max_length=100)
    qualification = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100)
    email = models.EmailField()
    pic = models.FileField(upload_to='pics/')
    status = models.IntegerField(default=0)

    # def __str__(self):
    #     return self.name


class PharmacyLogin(models.Model):
    user = models.OneToOneField(Login, on_delete=models.CASCADE, related_name='pharmacy')
    registration_no = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    Location = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_no = models.CharField(max_length=100)
    email = models.EmailField()
    pic = models.ImageField(upload_to='pics')
    status = models.IntegerField(default=0)
    def __str__(self):
        return self.name

#prescription

class Prescription(models.Model):
    doctor = models.ForeignKey(Login, on_delete=models.DO_NOTHING,null=True)
    patient = models.ForeignKey(PatientLogin, on_delete=models.DO_NOTHING,unique=False)
    date=models.DateField()
    medicine_details=models.TextField(max_length=100)

    # def __str__(self):
    #     return self.name


class DoctorSchedule(models.Model):
    date=models.DateField()
    doctor_name=models.CharField(max_length=100)
    start_time = models.TimeField(max_length=100)
    end_time = models.TimeField(max_length=100)
    def __str__(self):
        return self.doctor_name
#add stock to pharmacy
class AddStock(models.Model):
    pharmacy_name=models.ForeignKey(PharmacyLogin,on_delete=models.CASCADE,null=True,blank=True)
    medicine_name=models.CharField(max_length=100)
    batch_no=models.CharField(max_length=100)
    number_of_tablets=models.CharField(max_length=100)
    arrival_date = models.DateField()
    expiry_date=models.DateField()
    price=models.CharField(max_length=100)
    photo=models.ImageField(upload_to='pic_med')
    def __str__(self):
        return self.medicine_name
class DocChat(models.Model):
    user=models.ForeignKey(Login,on_delete=models.DO_NOTHING)
    chat=models.CharField(max_length=100)
    date=models.DateField()
    message=models.TextField(null=True,blank=True)
    def __str__(self):
        return self.user

class MedicineSelect(models.Model):
    medicine_image=models.ImageField(upload_to='medpic')
    medicine_name=models.CharField(max_length=100)
    price=models.FloatField()
    status = models.IntegerField(default=0)
    pharmacy_name = models.ForeignKey(PharmacyLogin, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.medicine_name


class buy_medicines(models.Model):
    user=models.ForeignKey(Login,on_delete=models.CASCADE,related_name='but_medicines')
    medicine=models.ForeignKey(MedicineSelect,on_delete=models.CASCADE)

    status=models.IntegerField(default=0)


class Bill(models.Model):
    medicine_name=models.CharField(max_length=100)
    number_of_strips=models.IntegerField()
    amount=models.FloatField()
    def __str__(self):
        return self.medicine_name

class upload_img(models.Model):
    img_upload=models.ImageField(upload_to='img')

DISEASES_CHOICES = {
                 ('Covid','Covid'),
                 ('Pneumonia','Pneumonia')

}


class Sendtest_result(models.Model):
    date=models.DateField()
    patient = models.ForeignKey(Login,on_delete=models.DO_NOTHING, null=True)
    doctor_name = models.ForeignKey(DoctorLogin,on_delete=models.DO_NOTHING, unique=False)
    xray = models.ImageField(upload_to='pic_xray')
    disease=models.CharField(max_length=100,choices=DISEASES_CHOICES)

class Chat(models.Model):
    user = models.ForeignKey(Login,on_delete=models.CASCADE,null=True)
    desc = models.TextField()


class Chat_add(models.Model):
    user = models.ForeignKey(Login, on_delete=models.DO_NOTHING)
    subject = models.CharField(max_length=200)
    Enquiry = models.TextField()
    date = models.DateField()
    reply = models.TextField(null=True, blank=True)