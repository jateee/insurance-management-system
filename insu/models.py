from django.db import models
from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
import random
import string


# Create your models here.
# models.py


class Policy(models.Model):
    POLICY_TYPE_CHOICES = [
        ('life', 'Life Insurance'),
        ('health', 'Health Insurance'),
        ('auto', 'Auto Insurance'),
        ('home', 'Home Insurance'),
        ('travel', 'Travel Insurance'),
        ('rental', 'Rental Insurance'),
        ('disability', 'Disability Insurance'),
        ('pet', 'Pet Insurance'),
        ('business', 'Business Insurance'),
        ('marine', 'Marine Insurance'),
        ('property', 'Property Insurance'),
        ('liability', 'Liability Insurance'),
        ('critical_illness', 'Critical Illness Insurance'),
        ('workers_compensation', 'Workers Compensation Insurance'),
        ('long_term_care', 'Long-Term Care Insurance'),
        ('identity_theft', 'Identity Theft Insurance'),
        ('umbrella', 'Umbrella Insurance'),
        ('flood', 'Flood Insurance'),
        ('earthquake', 'Earthquake Insurance'),
        ('car_rental', 'Car Rental Insurance'),
        ('mobile', 'Mobile Phone Insurance'),
        ('cyber', 'Cyber Insurance'),

    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='insu_policies')  # Link policy to user
    policy_number = models.CharField(max_length=255)
    policy_holder_name = models.CharField(max_length=255)
    policy_type = models.CharField(max_length=50, choices=POLICY_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    premium_amount = models.DecimalField(max_digits=10, decimal_places=2)
    coverage_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.policy_number} - {self.policy_holder_name}"

    def save(self, *args, **kwargs):
        if not self.policy_number:
            self.policy_number = self.generate_policy_number()
        super().save(*args, **kwargs)
    
    def generate_policy_number(self):
        # You can modify this logic to meet your requirements
        # This method will generate a policy number such as 'POLICY-0001', 'POLICY-0002', etc.
        
        last_policy = Policy.objects.all().order_by('id').last()
        if last_policy:
            last_number = int(last_policy.policy_number.split('-')[1])
            new_number = last_number + 1
        else:
            new_number = 1
        
        # Format the new policy number, e.g., 'POLICY-0001'
        return f"POLICY-{new_number:04d}"
         
    def __str__(self):
        return f"Policy {self.policy_number} - {self.policy_holder_name}"
    
class Claim(models.Model):
    CLAIM_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='insu_claims')
    policy = models.ForeignKey(Policy, on_delete=models.CASCADE, related_name='claims')
    claim_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(choices=CLAIM_STATUS_CHOICES, default='pending', max_length=10)
    date_submitted = models.DateTimeField(auto_now_add=True)
    claim_reason = models.TextField()
    status = models.CharField(max_length=20, choices=CLAIM_STATUS_CHOICES, default='pending')
 

    def __str__(self):
        return f"Claim {self.id} for Policy {self.policy.policy_number}"
    


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the object is createdcls
    

    def __str__(self):
        return f"Message from {self.name}"




class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']






