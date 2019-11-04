# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from models import CustomUser, Product
from forms import CustomUserCreationForm, CustomUserChangeForm, ProductCreationForm

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.decorators import login_required 
 
from datetime import datetime 

#Loggin
import logging
log=logging.getLogger('Trab2') 

#Entrada do site
def home(request):
    return render(request, 'MyBay/home.html')

#Registo de um novo utilizador
def register(request):
    if request.method=='POST':
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            log.info('{} is a new user!'.format(request.user.username)) 
            return redirect('home')
        else:
            form=CustomUserCreationForm() 
            log.info('Someone tried create profile!')
            args={
                'form':form, 
                'erro':"Try Again!",
                } 
            return render(request, 'account/signup.html', args) 
    else:
        form=CustomUserCreationForm() 
        args={
            'form':form, 
            'erro':"",
            }
        return render(request, 'account/signup.html', args) 

#Ver/Editar perfil de um utilizado autentificado
@login_required()
def edit_profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            log.info('{} changed profile!'.format(request.user.username))
            args={
                'form': CustomUserChangeForm(instance=request.user),
                'erro': "Profile changed",
                }
            return render(request, 'MyBay/myaccount.html', args)
        else:
            log.warning('{} tried change profile!'.format(request.user.username))  
            args={
                'form': CustomUserChangeForm(instance=request.user),
                'erro': "Try Again",
                }
            return render(request, 'MyBay/myaccount.html') 
    else:
        args={
            'form': CustomUserChangeForm(instance=request.user),
            'erro': "",
            }
        return render(request, 'MyBay/myaccount.html', args)

#Mudar password
@login_required()
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(data=request.POST, user=request.user) 
        if form.is_valid():
            form.save()
            log.info('{} changed password!'.format(request.user.username))  
            update_session_auth_hash(request, form.user)
            args={
                'form': CustomUserChangeForm(instance=request.user),
                'erro': "Password changed!",
                }
            return render(request, 'MyBay/myaccount.html', args)
        else: 
            log.warning('{} tried change password!'.format(request.user.username)) 
            args = {
                'form': PasswordChangeForm(user=request.user),
                'erro': "Try Again",
                }
            return render(request, 'MyBay/myaccount.html', args)   
    else:  
        args={
            'form': PasswordChangeForm(user=request.user),
            'erro': '',
            }
        return render(request, 'MyBay/myaccount.html', args)   

#Apagar conta
@login_required()
def deleteaccount(request):
    if request.method=='POST':
        request.user.delete()
        return redirect('home')
    else:
        context={
            'account':request.user,
            }
        return render(request, 'MyBay/deleteaccount.html', context)
   
#Listagem dos próprios produtos
@login_required()
def myproducts(request):
    args={
        'productList':Product.objects.filter(owner=request.user).order_by('created_date'),
        } 
    return render(request, 'MyBay/myproducts.html', args)

#Editar produto
@login_required()
def editproduct(request, id): 
    obj = Product.objects.get(id=id)
    if request.method=='POST':
        form=ProductCreationForm(request.POST, instance=obj)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.save() 
            context={
                'form':form,
                'error': "Product changed.",
                }
            log.info('{} changed product {}!'.format(request.user.username, id)) 
            return render(request, 'MyBay/editproduct.html', context)
        else:
            context={
                'form':form,
                'error': "The form was not updated successfully.",
                }
            log.warning('{} tried change product {}!'.format(request.user.username, id))     
            return render(request, 'MyBay/editproduct.html', context)
    else: 
        form=ProductCreationForm(instance=obj)
        context={
            'form':form,
            'error': "",
            }
        return render(request, 'MyBay/editproduct.html', context)

#Apagar produto
@login_required()
def deleteproduct(request, id):
    obj = Product.objects.get(id=id)
    if request.method=='POST':
        obj.delete()
        log.info('{} product {}!'.format(request.user.username, id))   
        args={
            'productList':Product.objects.filter(owner=request.user),
            }
        return render(request, 'MyBay/myproducts.html', args  )
    else:
        context={
            'product':obj,
            }
        return render(request, 'MyBay/deleteproduct.html', context)
   
#Criar produto
@login_required()
def createproduct(request):
    
    if request.method=='POST':
        form=ProductCreationForm(request.POST, request.FILES)
        if form.is_valid():
            obj=form.save(commit=False)
            obj.owner=request.user
            obj.save()
            log.info('{} created a new product: {}!'.format(request.user.username, id)) 
            args={
                'productList':Product.objects.filter(owner=request.user),
                }
            return render(request, 'MyBay/myproducts.html', args  )
        else: 
            log.warning('{} tried to create a new product!'.format(request.user.username))   
            context={
                'form':ProductCreationForm(request.POST, request.FILES),
                'error': "Product not created.",
                }
            return render(request, 'MyBay/createproduct.html', context)
    else: 
        context={
            'form':ProductCreationForm(request.POST, request.FILES),
            'error': "",
            }
        return render(request, 'MyBay/createproduct.html', context)



#Pesquisas
@login_required()
def searchproducts(request):
    from django.db.models.functions import Lower
    if request.method=='POST':
        prd=Product.objects.all()
        
        if request.POST['name']!="":
            prd=prd.filter(title__icontains = request.POST['name'])
        
        if 'countrypr' in request.POST: 
            prd=prd.filter(country = request.user.country) 
        
        if request.POST['minprice']!="":
            prd=prd.filter(price__gte = request.POST['minprice'])
            
        if request.POST['maxprice']!="":
            prd=prd.filter(price__lte = request.POST['maxprice'])
        
        import datetime
        if str(request.POST['afterdate'])!="":
            s=str(request.POST['afterdate'])
            afterdate=datetime.datetime.strptime(str(request.POST['afterdate']), "%Y-%m-%d").date()
            prd=prd.filter(created_date__gte = afterdate)
             
        if request.POST['category']!="":
            if request.POST['category']=="clothes":
                prd=prd.filter(category = 1)
            elif request.POST['category']=="comics":
                prd=prd.filter(category = 2)
            elif request.POST['category']=="figures":
                prd=prd.filter(category = 3)
            elif request.POST['category']=="games":
                prd=prd.filter(category = 4)
            elif request.POST['category']=="others":
                prd=prd.filter(category = 5)
        
        variavel=request.POST['variavel']
        if request.POST['order']=="desc":
            args={'productList':prd.order_by(Lower(variavel).desc())}
        else:
            args={'productList':prd.order_by(Lower(variavel).asc())}
            
        return render(request, 'MyBay/searchproducts.html', args)
        
    else:
        args={
            'productList':Product.objects.filter().order_by('-created_date'),
            } 
        return render(request, 'MyBay/searchproducts.html', args)

#Ver produto
@login_required()
def viewproduct(request, id): 
    obj = Product.objects.get(id=id)
    
    if request.method=='GET':
        args={
            'p':obj,
            } 
        return render(request, 'MyBay/viewproduct.html', args)
    else:
        args={
            'productList':Product.objects.filter().order_by('-created_date'),
            } 
        return render(request, 'MyBay/searchproducts.html', args) 
 
 
 