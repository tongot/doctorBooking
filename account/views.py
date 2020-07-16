from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponseRedirect
from .forms import RegisterForm, DependenciesForm, LoginForm
from .models import Account
from django.contrib.auth import authenticate, login, logout
from bookings.models import Dependencies, Patient

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name =  form.cleaned_data['last_name']
            date_of_birth =  form.cleaned_data['date_of_birth']
            gender =  form.cleaned_data['gender']
            email = form.cleaned_data['email']
            password1 =  form.cleaned_data['password1']
            medical_aid = form.cleaned_data['medical_aid']
            phone=form.cleaned_data['phone_number']
            medical_number= form.cleaned_data['medical_aid_number']

            user_new =Account.objects.create_user_external(email,first_name,last_name, date_of_birth, gender, phone, password1)
            
            patient = Patient(user=user_new, medical_aid=medical_aid,medical_aid_number=medical_number)
            patient.save()

            return HttpResponseRedirect('/account/login')
        return render(request, 'register.htm', {'form': form})      
    else:
        context = RegisterForm()
        return render(request, 'register.htm', {'form': context})

def register_dependent(request):
    if request.user.is_anonymous==False:

        if request.method == 'POST':
            form = DependenciesForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/account/register_dependent')
            else:
                return render(request, 'dependent_register.htm', {'form':form})
        else:
            patient = Patient.objects.get(user_id=request.user.id)
            data = Dependencies()
            data.patient=patient
            form = DependenciesForm(instance=data)
            context = {
                'form': form,
                'dependencies_list': Dependencies.objects.filter(patient_id=patient.id)
            }
            return render(request, 'dependent_register.htm', context)
    else:
        return HttpResponseRedirect('/account/login')

def login_user(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email,password=password)

        if user is not None:
            login(request,user)
            if user.is_admin:
                return HttpResponseRedirect('/booking/booking_list')
            else:
                return HttpResponseRedirect('/account/register_dependent')
        else:
            return render(request, 'login.htm', {'Error': 'Incorrect user name or password'})
    else:
        context = LoginForm()
        return render(request, 'login.htm', {'form': context})

def logout_user(request):

    if request.user is not None:
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')

def delete_dependence(request,id=1):
    if request.user.is_anonymous==False:
        if request.method=='POST':
            Dep = get_object_or_404(Dependencies, id = id)
            Dep.delete()
            return HttpResponseRedirect('/account/register_dependent')
        else:
            context={
                'details': get_object_or_404(Dependencies, id = id)
            }
            return render(request, 'dependend_delete.htm', context)
    else:
        redirect('/account/login')

def update_dependence(request,id=1):
    if request.user.is_anonymous==False:
        dependent = get_object_or_404(Dependencies, id=id)
        form = DependenciesForm(instance=dependent)

        if request.method=='POST':
            form = DependenciesForm(request.POST,instance=dependent)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/account/register_dependent')
        else:
            context={
                'form':form,
                'action':'Edit'
            }
            return render(request,'dependent_add_edit.htm',context)