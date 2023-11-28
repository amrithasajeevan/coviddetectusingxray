from django.urls import path

from cpapp import views

urlpatterns=[
    path("",views.home,name="home"),
    path('loginpage',views.loginpage,name="loginpage"),
    path('registerpage',views.registerpage,name="registerpage"),
    path('doctor_regiseterpage', views.doctor_regiseterpage, name="doctor_registerpage"),

    path('adminpage',views.adminpage,name="adminpage"),
    path('patientpage',views.patientpage,name="patientpage"),
    path('doctorpage', views.doctorpage, name="doctorpage"),

    path('view_user',views.view_user, name="view_user"),
    path('view_doctor', views.view_doctor,name="view_doctor"),

    path('approve_doctor/<int:id>/',views.approve_doctor,name="approve_doctor"),
    path('reject_doctor/<int:id>/',views.reject_doctor,name="reject_doctor"),
    path('remove_doctor/<int:id>/', views.remove_doctor, name="remove_doctor"),
    path('update_userprofile/<int:id>/', views.update_userprofile, name="update_userprofile"),
    path('remove_user/<int:id>/', views.remove_user, name="remove_user"),

    path('prescriptionpage', views.prescriptionpage, name="prescriptionpage"),
    path('doctorschedule', views.doctorschedule, name="doctorschedule"),
    path('view_schedule', views.view_schedule, name="view_schedule"),
    path('view_doctors', views.view_doctors, name="view_doctors"),
    path('view_pharmacies',views.view_pharmacies,name="view_pharmacies"),
    path('view_doctorschedule',views.view_doctorschedule,name="view_doctorschedule"),
    path('view_prescription', views.view_prescription, name="view_prescription"),
    path('doctor_profile', views.doctor_profile, name="doctor_profile"),
    path('update_doctor/<int:id>/', views.update_doctor, name="update_doctor"),

    path('stockpage',views.stockpage, name="stockpage"),
    path('view_stock',views.view_stock, name="view_stock"),
    path('update_stock/<int:id>/', views.update_stock, name="update_stock"),
    path('remove_stock/<int:id>/', views.remove_stock, name="remove_stock"),
    path('chatwithdoctor',views.chatwithdoctor,name='chatwithdoctor'),
    path('chatview', views.chatview, name="chatview"),
    path(' chat_add_user', views. chat_add_user, name="chat_add_user"),
    path('select_medicines',views.select_medicines,name="select_medicines"),
    path('cancel_medicines',views.cancel_medicines,name="cancel_medicines"),
    path('bill_medicine/<int:id>/',views.bill_medicine,name="bill_medicine"),
    path('buy_medicines/<int:id>/',views.buy_medicines,name="buy_medicines"),
    path('load_upload_page',views.load_upload_page,name="load_upload_page"),
    path('user_profile',views.user_profile,name="user_profile"),
    path('logout_view',views.logout_view,name="logout_view"),
    path('view_prescriptions', views.view_prescriptions, name="view_prescriptions"),
    path('edit_prescription/<int:id>/', views.edit_prescription, name="edit_prescription"),
    path('view_userlist',views.view_userlist,name="view_userlist"),
    path('remove_prescription/<int:id>/', views.remove_prescription, name="remove_prescription"),
    path('received_order', views.received_order, name="received_order"),
    path('chat_add', views.chat_add, name="chat_add"),
    path('chat_add_user', views.chat_add_user, name="chat_add_user"),
    path('chat_view_user', views.chat_view_user, name="chat_view_user"),
    path('chat_doctor', views.chat_doctor, name="chat_doctor"),
    path('reply_chat<int:id>/', views.reply_chat, name="reply_chat"),







]