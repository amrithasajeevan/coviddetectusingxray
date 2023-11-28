import re

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect

# Create your views here.
from cpapp.forms import LoginForm, PatientRegister, DoctorRegister, PharmacyRegister, Prescription, Scheduling, \
    Prescriptionform, Stock, ChatWithDoctor, chatform, selectmedicine, Billing, upload_form, Send_Result,ChatForm , CHATForm
from cpapp.models import PatientLogin, DoctorLogin, PharmacyLogin, DoctorSchedule, AddStock, DocChat, Bill, upload_img, \
    Login
from cpapp.prediction import model_predict
from .models import *


def home(request):
    return render(request, "frontpage.html")


def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        password = request.POST.get('pass')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('adminpage')
        elif user is not None and user.is_patient:
            login(request, user)
            return redirect('user_profile')
        elif user is not None and user.is_doctor:
            if user.doctor.status == True:
                login(request, user)
                return redirect('doctorpage')
            else:
                messages.info(request, 'you are not approved to login')
        elif user is not None and user.is_pharmacy:
            if user.pharmacy.status == True:
                login(request, user)
                return redirect('pharmacypage')
            else:
                messages.info(request, 'you are not approved to login')

        else:
            messages.info(request, 'Invalid Credentials')

    return render(request, "login.html")


def registerpage(request):
    user_form = LoginForm()
    patient_form = PatientRegister()
    if request.method == 'POST':
        user_form = LoginForm(request.POST)
        patient_form = PatientRegister(request.POST, request.FILES)
        if user_form.is_valid() and patient_form.is_valid():
            user = user_form.save(commit=False)
            user.is_patient = True
            user.save()
            patient = patient_form.save(commit=False)
            patient.user = user
            patient.save()
            messages.info(request, 'Registered Successfully')
            return redirect(loginpage)
    return render(request, 'register.html', {'user_form': user_form, 'patient_form': patient_form})


def doctor_regiseterpage(request):
    user_form = LoginForm()
    doctor_form = DoctorRegister()
    if request.method == 'POST':
        user_form = LoginForm(request.POST)
        doctor_form = DoctorRegister(request.POST, request.FILES)
        if user_form.is_valid() and doctor_form.is_valid():
            user = user_form.save(commit=False)
            user.is_doctor = True
            user.save()
            doctor = doctor_form.save(commit=False)
            doctor.user = user
            doctor.save()
            messages.info(request, 'Registered Successfully')
            return redirect(loginpage)
    return render(request, 'doctor_register.html', {'user_form': user_form, 'doctor_form': doctor_form})


def pharmacy_regiseterpage(request):
    user_form = LoginForm()
    pharmacy_form = PharmacyRegister()
    if request.method == 'POST':
        user_form = LoginForm(request.POST)
        pharmacy_form = PharmacyRegister(request.POST, request.FILES)
        if user_form.is_valid() and pharmacy_form.is_valid():
            user = user_form.save(commit=False)
            user.is_pharmacy = True
            user.save()
            pharmacy = pharmacy_form.save(commit=False)
            pharmacy.user = user
            pharmacy.save()
            messages.info(request, 'Registered Successfully')
            return redirect(loginpage)
    return render(request, 'pharmacy_register.html', {'user_form': user_form, 'pharmacy_form': pharmacy_form})


@login_required(login_url='loginpage')
def adminpage(request):
    return render(request, "adminwork/index_admin.html")


@login_required(login_url='loginpage')
def patientpage(request):
    return render(request, "userwork/userprofile.html")


@login_required(login_url='loginpage')
def doctorpage(request):
    return render(request, "doctorwork/index_doctor.html")


@login_required(login_url='loginpage')
def pharmacypage(request):
    return render(request, "pharmacywork/index_pharmacy.html")


@login_required(login_url='loginpage')
def view_user(request):
    data = PatientLogin.objects.all()
    return render(request, 'adminwork/view_user.html', {'data': data})
    # return render(request,"adminwork/view_user.html")


# delete_user
def remove_user(request, id):
    data = PatientLogin.objects.get(id=id)
    data.delete()
    return redirect('view_user')


@login_required(login_url='loginpage')
def view_doctor(request):
    data = DoctorLogin.objects.all()
    return render(request, 'adminwork/view_doctor.html', {'data': data})


# delete--doctor
def remove_doctor(request, id):
    data1 = DoctorLogin.objects.get(id=id)
    data = Login.objects.get(doctor=data1)
    if request.method == 'POST':
        data.delete()
        return redirect('view_doctor')
    else:
        return redirect('view_doctor')



# edit--doctor profile
@login_required(login_url='loginpage')
def update_doctor(request, id):
    data = DoctorLogin.objects.get(id=id)
    form = DoctorRegister(instance=data)
    if request.method == 'POST':
        form = DoctorRegister(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('doctor_profile')
    return render(request, 'doctorwork/edit_profile.html', {'form': form})


# pharmacy--view
@login_required(login_url='loginpage')
def view_pharmacy(request):
    data = PharmacyLogin.objects.all()
    return render(request, 'adminwork/view_pharmacy.html', {'data': data})


# remove--pharmacy
@login_required(login_url='loginpage')
def remove_pharmacy(request, id):
    data1 = PharmacyLogin.objects.get(id=id)
    data = Login.objects.get(pharmacy=data1)
    if request.method == 'POST':
        data.delete()
        return redirect('view_pharmacy')
    else:
        return redirect('view_pharmacy')


# edit--pharmacy profile
@login_required(login_url='loginpage')
def update_pharmacy(request, id):
    data = PharmacyLogin.objects.get(id=id)
    form = PharmacyRegister(instance=data)
    if request.method == 'POST':
        form = PharmacyRegister(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('pharmacy_profile')
    return render(request, 'pharmacywork/edit_pharmacy_profile.html', {'form': form})


# approve Doctor
@login_required(login_url='loginpage')
def approve_doctor(request, id):
    doctor = DoctorLogin.objects.get(user_id=id)
    doctor.status = True
    doctor.status = 1
    doctor.save()
    messages.info(request, 'accept Doctor login')
    return redirect('view_doctor')


# reject Doctor
@login_required(login_url='loginpage')
def reject_doctor(request, id):
    doctor = DoctorLogin.objects.get(user_id=id)
    if request.method == 'POST':
        doctor.status = 2
        # doctor.status = False
        doctor.save()
        messages.info(request, 'rejected Doctor login')
    return redirect('view_doctor')


# approve pharmacy
@login_required(login_url='loginpage')
def approve_pharmacy(request, id):
    pharmacy = PharmacyLogin.objects.get(user_id=id)
    pharmacy.status = True
    pharmacy.save()
    messages.info(request, 'accept Pharmacy login')
    return redirect('view_pharmacy')


# reject pharmacy
@login_required(login_url='loginpage')
def reject_pharmacy(request, id):
    pharmacy = PharmacyLogin.objects.get(user_id=id)
    if request.method == 'POST':
        pharmacy.status = False
        pharmacy.save()
        messages.info(request, 'rejected pharmacy login')
    return redirect('view_pharmacy')


# Send  prescription
@login_required(login_url='loginpage')
def prescriptionpage(request):
    form = Prescriptionform()
    u = request.user



    print(u)
    if request.method == 'POST':
        form = Prescriptionform(request.POST)
        if form.is_valid():
            p=form.save(commit=False)
            p.doctor = u
            p.save()
            print(p)
            messages.info(request,'Prescription generated')
            return redirect(view_prescription)
    return render(request,'doctorwork/send_prescription.html', {'form': form})


# def formp(request):
#     form = Prescriptionform()




# add stock to pharmacy
@login_required(login_url='loginpage')
def stockpage(request):
    stock_form = Stock()
    u = request.user
    print(u)
    if request.method == 'POST':
        stock_form = Stock(request.POST, request.FILES)
        if stock_form.is_valid():
            p = stock_form.save(commit=False)
            p.user= u
            p.save()
            print(p)

            messages.info(request, 'stock generated')
            return redirect(pharmacypage)
    return render(request, 'pharmacywork/add_stock.html', {'stock_form': stock_form})

# view prescription by doctor
@login_required(login_url='loginpage')
def view_prescription(request):
    data = Prescription.objects.all()
    return render(request, 'doctorwork/view_prescription.html', {'data': data})


# view prescription by user

@login_required(login_url='loginpage')
def view_prescriptions(request):
    p = PatientLogin.objects.get(user=request.user)
    data = Prescription.objects.filter(patient=p)
    return render(request, 'userwork/view_prescription1.html', {'data': data})


# doctor schedule
@login_required(login_url='loginpage')
def doctorschedule(request):
    schedule_form = Scheduling()
    if request.method == 'POST':
        schedule_form = Scheduling(request.POST, request.FILES)
        if schedule_form.is_valid():
            schedule_form.save()
            messages.info(request, 'Schedule generated')
            return redirect('doctorpage')
    return render(request, 'doctorwork/doctor_schedule.html', {'schedule_form': schedule_form})


# view Schedule by doctor
@login_required(login_url='loginpage')
def view_schedule(request):
    data = DoctorSchedule.objects.all()
    return render(request, 'doctorwork/view_schedule.html', {'data': data})


# view doctor as user
@login_required(login_url='loginpage')
def view_doctors(request):
    data = DoctorLogin.objects.all()
    return render(request, 'userwork/view_doctor.html', {'data': data})


# view pharmacy as user
@login_required(login_url='loginpage')
def view_pharmacies(request):
    data = PharmacyLogin.objects.all()
    return render(request, 'userwork/view_pharmacy1.html', {'data': data})


# view doctor schedule by user
@login_required(login_url='loginpage')
def view_doctorschedule(request):
    data = DoctorSchedule.objects.all()
    return render(request, 'userwork/view_doctorschedule.html', {'data': data})


# create doctor profile
@login_required(login_url='loginpage')
def doctor_profile(request):
    u = request.user
    data = DoctorLogin.objects.filter(user=u)
    return render(request, 'doctorwork/doctorprofile.html', {'data': data})


# pharmacy profile
@login_required(login_url='loginpage')
def pharmacy_profile(request):
    u = request.user
    data = PharmacyLogin.objects.filter(user=u)
    return render(request, 'pharmacywork/pharmacy_profile.html', {'data': data})





# view stock
@login_required(login_url='loginpage')
def view_stock(request):
    data = AddStock.objects.all()
    return render(request, 'pharmacywork/view_stock.html', {'data': data})


# update stock
@login_required(login_url='loginpage')
def update_stock(request, id):
    data = AddStock.objects.get(id=id)
    form = Stock(instance=data)
    if request.method == 'POST':
        form = Stock(request.POST or None,request.FILES or None, instance=data)
        if form.is_valid():
            form.save()
            return redirect('view_stock')
    return render(request, 'pharmacywork/update_stock.html', {'form': form})


# delete stock
@login_required(login_url='loginpage')
def remove_stock(request, id):
    data = AddStock.objects.get(id=id)
    data.delete()
    return redirect('view_stock')


@login_required(login_url='loginpage')
def chatwithdoctor(request):
    chat_form = ChatWithDoctor()
    user=request.user
    if request.method == 'POST':
        chat_form = ChatWithDoctor(request.POST, request.FILES)
        if chat_form.is_valid():
            chat_form.save()
            chat_form.user=user
            user.save()
            messages.info(request, 'chat with doctor')
            return redirect(patientpage)
    return render(request, 'userwork/chat_with_doctor.html', {'chat_form': chat_form})


# view  chat by doctor
@login_required(login_url='loginpage')
def chatview(request):

    data = DocChat.objects.filter(user=request.user)

    # patient=Login.objects.filter(is_patient=True)
    # print(patient)


    return render(request, 'doctorwork/view_chat.html', {'data': data})


# replay view
def replay_chat(request, id):
    f = PatientLogin.objects.get(id=id)
    if request.method == 'POST':
        r = request.POST.get('replay')
        f.replay = r
        f.save()
        messages.info(request, 'replay send for chat')
        return redirect('chatview')
    return render(request, 'doctorwork/view_chat.html')


def chat_add_user(request):
    form = chatform()
    u = request.user
    if request.method == 'POST':
        form = chatform(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            messages.info(request, 'chat successfull')
            return redirect('chatview')
    return render(request, 'doctorwork/view_chat.html', {'form': form})


@login_required(login_url='loginpage')
def select_medicines(request ):
    data = AddStock.objects.all()
    return render(request, 'userwork/medicine_selection.html', {'data': data})

# @login_required(login_url='loginpage')
# def buy_medicines(request ,id ):
#     if request.method=='POST':
#         data = buy_medicines.objects.all()
#         print(data)
#         data.status = 1
#         data.save()
#     return render(request, 'userwork/medicine_selection.html', {'data': data})

def buy_medicines(request,id):
    data = buy_medicines.objects.get(id=id)
    data.status = 0
    data.save()
    return redirect('select_medicines')

def cancel_medicines(request,id):
    data = buy_medicines.objects.get(id=id)
    data.status = 2
    data.save()
    return redirect('select_medicines')

@login_required(login_url='loginpage')
def bill_medicine(request, id):
    data = AddStock.objects.get(id=id)
    form = Billing(instance=data)
    if request.method == 'POST':
        form = Billing(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('select_medicines')
    return render(request, 'userwork/medicine_selection.html', {'form': form})


# def load_task(request):
#     return  render(request,)

@login_required(login_url='loginpage')
def load_upload_page(request):
    if request.method == "POST" and 'upload_btn' in request.POST:

        form = upload_form(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.error(request, "Image Uploaded Sucessfully!")
        else:
            form = upload_form()
            messages.error(request, "Image not Uploaded!")

    if request.method == "POST" and 'check_btn' in request.POST:
        obj = upload_img.objects.all().last()
        scr = obj.img_upload
        new_scr = 'media/' + str(scr)
        print("___________the scourse _----------- ")
        print(new_scr)
        get_prediction = model_predict(new_scr)
        print("____________ the prediction ______________")
        print(get_prediction)
        context = {
            "image": obj,
            "prediction": get_prediction
        }
        return render(request, 'userwork/upload_xray.html', context)

    if request.method == "POST" and 'log_out_btn' in request.POST:
        return redirect('log_out_load')

    return render(request, 'userwork/upload_xray.html')


# user_profile
@login_required(login_url='loginpage')
def user_profile(request):
    u = request.user
    data = PatientLogin.objects.filter(user=u)
    return render(request, 'userwork/userprofile.html', {'data': data})


# update--user
def update_userprofile(request, id):
    data = PatientLogin.objects.get(id=id)
    form = PatientRegister(instance=data)
    if request.method == 'POST':
        form = PatientRegister(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('user_profile')
    return render(request, 'userwork/update_user.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('loginpage')


@login_required(login_url='loginpage')
def edit_prescription(request, id):
    data = Prescription.objects.get(id=id)
    form = Prescriptionform(instance=data)
    if request.method == 'POST':
        form = Prescriptionform(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return redirect('view_prescription')
    return render(request, 'doctorwork/edit_prescription.html', {'form': form})


# view--user by doctor
@login_required(login_url='loginpage')
def view_userlist(request):
    data = PatientLogin.objects.all()
    return render(request, 'doctorwork/view_userlist.html', {'data': data})


# delete---prescription
def remove_prescription(request, id):
    data = Prescription.objects.get(id=id)
    data.delete()
    return redirect('view_prescription')
#send result to doctor
@login_required(login_url='loginpage')
def Report_form(request):
    form = Send_Result()
    u = request.user



    print(u)
    if request.method == 'POST':
        form = Send_Result(request.POST)
        if form.is_valid():
            p=form.save(commit=False)
            p.patient = u
            p.save()
            print(p)
            messages.info(request,'Result send')
            return redirect('patientpage')
    return render(request,'userwork/send_result_toDoc.html', {'form': form})

#received order

@login_required(login_url='loginpage')
def received_order(request):
    return render(request, "pharmacywork/order.html")


def chat_add(request):
    form = ChatForm()
    u = request.user
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            messages.info(request, 'Chat added Successfully')
            return redirect('chat_add')
    else:
        form = ChatForm()
    return render(request,'userwork/chat_add.html',{'form':form})

def chat_view(request):
    print('hi')
    chat = Chat.objects.all()
    print(chat)
    return render(request,'userwork/chat_view.html',{'chat':chat})

#user
def chat_add_user(request):
    form = CHATForm()
    u = request.user
    if request.method == 'POST':
        form = CHATForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.user = u
            obj.save()
            messages.info(request, 'Chat Added Successfully')
            return redirect('chat_view_user')
    return render(request, 'userwork/chat_addd.html', {'form': form})

def chat_view_user(request):
    f = Chat_add.objects.filter(user=request.user)
    return render(request, 'userwork/chat_vieww.html', {'feedback': f})

#doctor
def chat_doctor(request):
    f = Chat_add.objects.all()
    return render(request, 'doctorwork/chat_view.html', {'feedback': f})



def reply_chat(request, id):
    f = Chat_add.objects.get(id=id)
    if request.method == 'POST':
        r = request.POST.get('reply')
        f.reply = r
        f.save()
        messages.info(request, 'Reply send for chat')
        return redirect('chat_doctor')
    return render(request, 'doctorwork/reply_chat.html', {'feedback': f})
