from django.shortcuts import render, reverse, redirect
from django.http import JsonResponse
from app.models import Location
from django.contrib.auth.models import User
from django.contrib import messages
import random
from django.core.mail import send_mail
from django.contrib import auth
from app.models import Mechanic, RepairRequest,ProblemSubmission,Feedback
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.shortcuts import render
from .models import Mechanic
from django.http import HttpResponseNotFound
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from app.forms import FeedbackForm,CustomUserCreationForm

# Create your views here.
def home(request):
    return render(request, 'vmshomepage.html')

def base(request):
    return render(request, 'base.html')



def regsub(request):
    return render(request, 'regsub.html')

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from app.forms import LocationForm
from app.models import Location

class LocationCreateView(LoginRequiredMixin, CreateView):
    model = Location
    form_class = LocationForm
    template_name = 'location.html'
    success_url = reverse_lazy('app:location_success')

    def form_valid(self, form):
        # Assign the currently logged-in user to the 'user' field
        form.instance.user = self.request.user
        return super().form_valid(form)


def customerhome(request):
    return render(request,'customerhome.html')

@csrf_exempt
def save_location(request):
    if request.method == 'POST':
        url= request.POST.get('url')
        location = Location.objects.create(url=url)
        print(location)
        return JsonResponse({'message': 'Location saved successfully.'})
    else:
        return JsonResponse({'error': 'Method not allowed.'}, status=405)

# Authentication
def send_otp(email, otp):
    subject = 'OTP Verification'
    message = f'Your OTP for registration is: {otp}'
    send_mail(subject, message, None, [email])

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        password2 = request.POST["password2"]
        mobile=request.POST["number"]
        print("#####################################################")
        print(mobile)
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('app:register')

        otp_number = random.randint(1000, 9999)
        otp = str(otp_number)

        send_otp(email, otp)
        request.session['username'] = username
        request.session['email'] = email
        request.session['password'] = password
        request.session['otp'] = otp
        request.session['mobile']=mobile

        return HttpResponseRedirect(reverse('app:otp', args=[otp, username, password, email,mobile]))
    else:
        return render(request, 'register.html')

def otp(request, otp, username, password, email,mobile):
    if request.method == "POST":
        uotp = request.POST['otp']
        otp_from_session = request.session.get('otp')

        if uotp == otp_from_session:
            username = request.session.get('username')
            email = request.session.get('email')
            password = request.session.get('password')
            mobile=request.session.get('mobile')

            user = User.objects.create_user(username=username, password=password, email=email)
            user.save()
            return redirect('app:login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('app:otp', otp=otp, username=username, password=password, email=email,mobile=mobile)

    return render(request, 'otp.html', {'otp': otp, 'username': username, 'password': password, 'email': email,'mobile':mobile})

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('app:customerhome')
        else:
            messages.info(request, 'Invalid user credentials')
            return redirect('app:login')
    else:
        return render(request, 'login.html')

def user_logout(request):
    auth.logout(request)
    return redirect('/')



def mechanic_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('app:mechanichome')  # Redirect to mechanic home page after login
    else:
        form = AuthenticationForm()
    return render(request, 'mechanic_login.html', {'form': form})

def mechanic_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'You have successfully applied for the job!')
            return redirect('app:regsub')  # Redirect to mechanic home page after registration
    else:
        form = CustomUserCreationForm()
    return render(request, 'mechanic_register.html', {'form': form})

from django.contrib.auth import logout
def mechanic_logout(request):
    logout(request)
    return redirect('app:home')

def mechanichome(request):
    # Retrieve all repair requests
    repair_requests = RepairRequest.objects.all()


    # Pass repair requests to the template
    return render(request, 'mechanichome.html', {'repair_requests': repair_requests})

def mechanic_list(request):
    mechanics = Mechanic.objects.all()
    user_id = request.user.id  
    locations = Location.objects.filter(user_id=user_id)  # Filter locations based on user's ID
    return render(request, 'mechanic_list.html', {'mechanics': mechanics, 'locations': locations})

from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from app.models import Mechanic, RepairRequest, Location
from app.forms import LocationForm

def request_repair(request, mechanic_id):
    if request.method == 'POST':
        mechanic = get_object_or_404(Mechanic, pk=mechanic_id)
        
        # Assuming location_id is submitted via POST
        location_form = LocationForm(request.POST)
        if location_form.is_valid():
            location = location_form.save(commit=False)
            location.user = request.user  # Associate user with the location
            location.save()
            
            RepairRequest.objects.create(
                mechanic=mechanic,
                requested_by=request.user,
                location=location
            )
            messages.success(request, 'Repair request sent successfully.')
            return redirect('app:mechanic_list')
        else:
            # Print form errors for debugging
            print(location_form.errors)
            # Add error message to display in the template
            messages.error(request, 'Error occurred while processing the request. Please check the form data.')
    else:
        # If the request method is not POST, create an empty form
        location_form = LocationForm()
    
    return redirect('app:mechanic_list')





def repair_request_detail(request, request_id):
    repair_request = RepairRequest.objects.get(pk=request_id)
    return render(request, 'repair_request_detail.html', {'repair_request': repair_request})

def accept_repair_request(request, request_id):
    repair_request = RepairRequest.objects.get(pk=request_id)
    customer_email = repair_request.requested_by.email  # Retrieve customer's email
    repair_request.status = 'Accepted'
    repair_request.save()

    # Send email to the customer
    subject = 'Your Repair Request has been Accepted'
    message = 'Your repair request has been accepted. We will proceed with the necessary repairs.'
    sender_email = 'your_email@example.com'  # Replace with your email address
    send_mail(subject, message, sender_email, [customer_email])

    messages.success(request, 'Repair request accepted successfully and email sent to the customer.')
    return redirect('app:mechanichome')


def reject_repair_request(request, request_id):
    repair_request = RepairRequest.objects.get(pk=request_id)
    repair_request.status = 'Rejected'
    repair_request.save()
    messages.success(request, 'Repair request rejected successfully.')
    return redirect('app:mechanichome')

def cancel_request(request, mechanic_id):
    messages.success(request, 'Repair request cancelled successfully.')
    return redirect('app:mechanic_list')

def mechanic_repair_request_detail(request, request_id):
    try:
        repair_request = RepairRequest.objects.get(pk=request_id, mechanic__user=request.user)
        return render(request, 'mechanic_repair_request_detail.html', {'repair_request': repair_request})
    except RepairRequest.DoesNotExist:
        return HttpResponseNotFound("Repair request not found")

def customer_repair_request_detail(request, request_id):
    try:
        repair_request = RepairRequest.objects.get(pk=request_id, requested_by=request.user)
        return render(request, 'customer_repair_request_detail.html', {'repair_request': repair_request})
    except RepairRequest.DoesNotExist:
        return HttpResponseNotFound("Repair request not found")



def problem_submission(request):
    if request.method == 'POST':
        # Extract form data
        name = request.POST.get('name')
        vehicle_number = request.POST.get('vehicle_number')
        location = request.POST.get('location')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        problem_statement = request.POST.get('problem_statement')
        bill = request.POST.get('bill')

        # Create a new problem submission object
        problem_submission = ProblemSubmission(
            name=name,
            vehicle_number=vehicle_number,
            location=location,
            city=city,
            state=state,
            pincode=pincode,
            problem_statement=problem_statement,
            bill=bill
        )

        # Save the problem submission to the database
        problem_submission.save()

        # You can optionally redirect to a success page
        return HttpResponse('Problem submitted successfully!')
    else:
        # Render the form template for GET requests
        return render(request, 'problem_submission.html')

def bill(request):
    P = ProblemSubmission.objects.all()
    print(P)
    return render(request, 'bill.html', {'P': P})

# views.py

import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

stripe.api_key = settings.STRIPE_SECRET_KEY


def process_payment(request):
    return render(request,'card.html')


def cash(request):
    return render(request,'cash.html')
def feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('app:feedback_thankyou')
    else:
        form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})

def feedback_thankyou(request):
    return render(request, 'feedback_thankyou.html')

def displayfeedbacks(request):
    f=Feedback.objects.all()
    return render(request,'displayfeedbacks.html',{'f':f})

def ourservices(request):

    return render(request,'ourservices.html')


def location_success(request):
    return render(request, 'location_success.html')
