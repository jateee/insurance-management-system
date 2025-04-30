from django.contrib.auth.forms import AuthenticationForm

from django.contrib.auth import login

from django.shortcuts import render,redirect, get_object_or_404

from .forms import CreateUserForm, LoginForm

from django.contrib.auth.decorators import login_required

from django.contrib.auth.decorators import user_passes_test

from django import forms

<<<<<<< HEAD:fedha/views.py
from .forms import CreateUserForm

=======
>>>>>>> 8433222 (Better):insu/fedha/views.py
from .models import Policy, Claim

from .forms import PolicyForm

from .forms import PolicyApplicationForm

from .forms import ClaimForm

from django.utils import timezone

from django.contrib import messages

from django.db import IntegrityError

from django.core.exceptions import ValidationError

from django.core.mail import send_mail
from django.conf import settings
from .forms import ContactForm

# Authentication models and functions

from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login, logout


def homepage (request):

    title = "Homepage - My Site"
    if request.user.is_authenticated:
        title = f"Welcome {request.user.username} - My Site"

    context = {
        'title': 'Fedha insurance management system',  
        'welcome_message': 'FEDHA INSURANCE MANAGEMENT SYSTEM'
    }

    return render(request, 'fedha/index.html', context)


def register(request):
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            
            return redirect("login")  # Redirect to the login page after successful registration
        else:
            return render(request, 'fedha/register.html', {'registerform': form})

<<<<<<< HEAD:fedha/views.py
    form = CreateUserForm()  # Initialize an empty form on GET request
    return render(request, 'fedha/register.html', {'registerform': form})
=======
            return redirect("login")
        


    context = {'registerform': form} 

    return render(request, 'fedha/register.html', context=context)
>>>>>>> 8433222 (Better):insu/fedha/views.py




def login (request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect("dashboard")
            

    context = {'Loginform':form}

    return render(request, 'fedha/login.html', context=context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard or another page after login
    else:
        form = AuthenticationForm()

    return render(request, 'fedha/login.html', {'form': form})


@login_required(login_url='login')
def dashboard_view (request):
    policies = Policy.objects.filter(user=request.user)  # Get all policies for the logged in user
  
  # Get all claims for the logged-in user
    claims = Claim.objects.filter(user=request.user) 

    return render(request, 'fedha/dashboard.html', {
        'policies': policies,
        'claims': claims
    })
   



@login_required
def dashboard(request):
    # Get all policies for the logged-in user
    policies = Policy.objects.filter(user=request.user)

    # Get all claims made by the user
    claims = Claim.objects.filter(policy__user=request.user)
    user_claims = Claim.objects.filter(user=request.user)

    return render(request, 'dashboard.html', {
        'policies': policies,
        'claims': claims,
        'user_claims': user_claims
    })



  


def user_logout(request):

    auth.logout(request)

    return redirect("")

def is_admin(user):
    return user.is_staff   

@login_required
@user_passes_test(is_admin)
def add_policy(request):
    if request.method == 'POST':
        form = PolicyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")  # redirect to the dashboard after adding
    else:
        form = PolicyForm()
    return render(request, 'fedha/add_policy.html', {'form': form})









def apply_policy(request):
    if request.method == 'POST':
        form = PolicyApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your policy application has been submitted successfully.')
            return redirect('dashboard')  # Redirect to the dashboard page (or another page as necessary)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PolicyApplicationForm()

    return render(request, 'apply_policy.html', {'form': form})


class PolicyApplicationForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = [
            'policy_number', 'policy_type', 'policy_holder_name', 'start_date',
            'end_date', 'premium_amount', 'coverage_amount', 'status'
        ]
    
    def clean_policy_number(self):
        policy_number = self.cleaned_data.get('policy_number')
        if Policy.objects.filter(policy_number=policy_number).exists():
            raise ValidationError(f"A policy with the number {policy_number} already exists.")
        return policy_number


def apply_policy(request):
    if request.method == 'POST':
        form = PolicyApplicationForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Your policy application has been submitted successfully.')
                return redirect('dashboard')  # Redirect to the dashboard
            except IntegrityError:
                messages.error(request, 'A policy with this number already exists.')
                return redirect('apply_policy')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PolicyApplicationForm()

    return render(request, 'apply_policy.html', {'form': form})

def apply_policy(request):
    if request.method == 'POST':
        # Handle the form submission and policy creation logic here.
        policy_type = request.POST['policy_type']
        policy_holder_name = request.POST['policy_holder_name']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        premium_amount = float(request.POST['premium_amount'])
        coverage_amount = request.POST['coverage_amount']
        status = request.POST['status']
        
        # Create the new policy
        new_policy = Policy.objects.create(
            user=request.user,
            policy_number='POL' + str(Policy.objects.count() + 1),  # Policy numbering logic
            policy_type=policy_type,
            start_date=start_date,
            end_date=end_date,
            premium_amount=premium_amount,
            coverage_amount=coverage_amount,
            status=status
        )
        
        return redirect('dashboard')  # After submitting, redirect to the dashboard (where policies are listed)
    
    # Fetch the available policies for the user
    user_policies = Policy.objects.filter(user=request.user)
    return render(request, 'apply_policy.html', {'user_policies': user_policies})


@login_required
def submit_claim(request, policy_id):
    #Get the policy object based on the policy ID
    policy = get_object_or_404(Policy, id=policy_id)

    # Check if the logged-in user owns the policy
    if policy.user != request.user:
        messages.error(request, "You do not have permission to make a claim for this policy.")
        return redirect('dashboard')  # Redirect if the user doesn't own this policy

    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            # Create a new claim and associate it with the policy
            claim = form.save(commit=False)
            claim.policy = policy
            claim.save()
            messages.success(request, "Your claim has been submitted successfully!")
            return redirect('dashboard')  # Redirect to the dashboard or claim details page
        else:
            messages.error(request, "There were errors in your form. Please try again.")
    else:
        form = ClaimForm()

    return render(request, 'submit_claim.html', {'form': form, 'policy': policy})


@user_passes_test(lambda u: u.is_staff)  # Ensures only admin users can access this
def review_claim(request, claim_id):
    claim = Claim.objects.get(id=claim_id)

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'approve':
            claim.status = 'approved'
        elif action == 'reject':
            claim.status = 'rejected'
        
        claim.save()
        messages.success(request, f"Claim {claim_id} has been {claim.status}.")
        return redirect('dashboard')  # Redirect to the dashboard or claims list

    return render(request, 'review_claim.html', {'claim': claim})


@login_required
def dashboard(request):
    # Filter policies to show only the ones that belong to the logged-in user
    policies = Policy.objects.filter(user=request.user)
    
    return render(request, 'dashboard.html', {'policies': policies})

def dashboard(request):
    if request.user.is_staff:  # Check if user is an admin
        # Fetch all policies for admin
        policies = Policy.objects.all()
    else:
        # For non-admin users, display only their own policies
        policies = Policy.objects.filter(user=request.user)

    return render(request, 'dashboard.html', {'policies': policies})





@login_required
def claims_view(request):
    # Fetch claims associated with the logged-in user's policies
    claims = Claim.objects.filter(policy__user=request.user)  # Filter claims based on user

    # Check if claims are being fetched properly (debugging purpose)
    print(claims)  # Add this to the console to see if claims are fetched

    return render(request, 'review_claim.html', {'claims': claims})





@login_required
def submit_claim(request, policy_id, claim_id=None):
    # Fetch the policy based on the ID provided, and check if it belongs to the logged-in user
    policy = get_object_or_404(Policy, id=policy_id)

    # Ensure that the logged-in user owns the policy
    if policy.user != request.user:
        return redirect('dashboard')  # Redirect to dashboard if the policy does not belong to the user

    if request.method == 'POST':
        # Process the claim form
        form = ClaimForm(request.POST)
        if form.is_valid():
            claim = form.save(commit=False)  # Don't save yet 
            claim.policy = policy  # Link claim to the specific policy
            claim.user = request.user # Assign the logged-in user
            claim.save()

            messages.success(request, "Claim submitted Successfully!")
            return redirect('claim_success')  # Redirect to claim success page or similar
        else:
            # For GET requests, if the claim_id exists, you're editing an existing claim
         if claim_id:
            claim = Claim.objects.get(id=claim_id)
            form = ClaimForm(instance=claim) 
    else:
        form = ClaimForm()

    return render(request, 'fedha/submit_claim.html', {'form': form, 'policy': policy})

def claim_success(request):
    # You can pass any context you want to display on the success page
    return render(request, 'fedha/claim_success.html')  



@login_required
def add_policy(request):
    if not request.user.is_staff:
        return redirect('home')  # If the user is not staff, redirect to home

    if request.method == 'POST':
        form = PolicyForm(request.POST)
        if form.is_valid():
            form.save()  # Save the policy to the database
            return redirect('policy_list')  # Redirect to a list of policies (adjust URL name)
    else:
        form = PolicyForm()

    return render(request, 'fedha/add_policy.html', {'form': form})




@login_required
def admin_update_claim_status(request, claim_id):
    # Ensure only admin can access this view
    if not request.user.is_staff:
        return redirect('dashboard')

    # Get the claim object
    claim = get_object_or_404(Claim, claim_id=claim_id)

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status == 'approved':
            claim.status = 'approved'
            claim.approval_date = timezone.now()
        elif new_status == 'rejected':
            claim.status = 'rejected'
            claim.rejection_date = timezone.now()

        claim.save()
        return redirect('dashboard')

    return render(request, 'admin_update_claim_status.html', {'claim': claim})


def contact_view(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the contact message to the database
            messages.success(request, "Your message has been sent successfully!")
            return redirect('thanks')  # Redirect to a 'thank you' page
    else:
        form = ContactForm()

    return render(request, 'contact/contact_form.html', {'form': form})

<<<<<<< HEAD:fedha/views.py
def thanks_view(request):
    return render(request, 'contact/thanks.html') 
=======

>>>>>>> 8433222 (Better):insu/fedha/views.py
