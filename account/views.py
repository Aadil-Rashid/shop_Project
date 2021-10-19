from django.shortcuts import render, redirect

from django.contrib.auth import login, logout
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.decorators import login_required
from django.contrib import messages


from django.template.loader import render_to_string


from django.utils.encoding import force_text,force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from .token import account_activation_token 
from .forms import (UserRegisterForm, UserEditForm, UserAddressForm)
from .models import Customer, Address

# messages.debug, messages.info, message.success, message.error, message.warning


# Registration Page
def registerView(request):
    # if request.user.is_authenticated:
    #     return redirect('home-page')

    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('user_name')
            user_email = form.cleaned_data.get('email')

            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()

            # SetUp email
            current_site = get_current_site(request)
            subject = 'Activate your Palav-Poshak Account'
            message = render_to_string('account/account_activation_email.html',  {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })

            user.email_user(subject=subject, message=message)

            messages.success(request, f"Activation link has been sent to you.")
            context = {'userName': user_name, 'userEmail':user_email}
            return render(request, 'account/registerEmailConfirm.html', context)
            # return redirect('account:login')

        # else:
        #     messages.warning(request, "some error occurred")

    else:
        form = UserRegisterForm()

    context={'form': form,   }
    return render(request, 'account/register.html', context)


# Account activation token
def accountActivateView(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except():
        pass

    if (user is not None) and (account_activation_token.check_token(user, token)):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/activation_invalid.html')


@login_required
def dashboardView(request):
    # orders = user_orders(request)
    # context = {'section': 'profile', 'orders': orders}
    return render(request, 'account/dashboard.html',)
 

@login_required
def userEditView(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)

    context = {'user_form': user_form}

    return render(request, 'account/userEditDetails.html', context)


@login_required
def userDeleteView(request):
    user = Customer.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete-confirmation')


# Addresses
@login_required
def addressView(request):
    addresses = Address.objects.filter(customer=request.user)
    context = {'addresses': addresses}
    return render(request, 'account/address/addresses.html', context)


@login_required
def addAddressView(request):
    if request.method == "POST":
        form = UserAddressForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.customer = request.user
            form.save()
            return redirect('account:addresses')
    else:
        form = UserAddressForm()
    return render(request, 'account/address/editAddress.html', {'form':form})
    

@login_required
def editAddressView(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return redirect('account:addresses')
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, "account/address/editAddress.html", {"form": address_form})


@login_required
def deleteAddressView(request, id):
    Address.objects.get(pk=id, customer=request.user).delete()
    return redirect('account:addresses')

@login_required
def defaultAddressView(request, id):
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, customer=request.user,).update(default=True)
    return redirect('account:addresses')
    