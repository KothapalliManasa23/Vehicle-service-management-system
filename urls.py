from django.urls import path
from django.conf.urls.static import static
from app.views import *


app_name = "app"

urlpatterns = [
    path('location/success/', location_success, name='location_success'),  # Define the location success URL
    path('', home, name='home'),  # Home page URL
    path('register/', register, name='register'),  # Registration page URL
    path('login/', login_user, name='login'),  # Login page URL
    path('logout/', user_logout, name='user_logout'),  # Logout page URL
    
    path('location/', LocationCreateView.as_view(), name='location'),  # Location page URL
    path('save_location/', save_location, name='save_location'),  # Save location URL
    path('otp/<str:otp>/<str:username>/<str:password>/<str:email>/<str:mobile>/', otp, name='otp'),  # OTP verification URL
    path('mechlogin/', mechanic_login, name='mechanic_login'),  # Mechanic login URL
    path('mechregister/', mechanic_register, name='mechanic_register'),  # Mechanic register URL
    path('mechome/', mechanichome, name='mechanichome'),  # Mechanic home URL
    path('mechanics/', mechanic_list, name='mechanic_list'),  # Mechanic list URL
    path('mechanics/<int:mechanic_id>/request_repair/',request_repair, name='request_repair'),  # Request repair URL
    path('mechanics/<int:mechanic_id>/cancel_request/', cancel_request, name='cancel_request'),  # Cancel request URL
    path('base/', base, name='base'),  # Base URL
    path('mechanics/<int:mechanic_id>/repair_request_detail/<int:request_id>/', repair_request_detail, name='repair_request_detail'),
    path('mechanics/<int:mechanic_id>/repair_request_detail/<int:request_id>/', mechanic_repair_request_detail, name='mechanic_repair_request_detail'),
    path('repair_request_detail/<int:request_id>/', customer_repair_request_detail, name='customer_repair_request_detail'),  # Repair request detail URL for customers
    path('accept_repair_request/<int:request_id>/', accept_repair_request, name='accept_repair_request'),
    path('reject_repair_request/<int:request_id>/', reject_repair_request, name='reject_repair_request'),
    path('submit-problem/', problem_submission, name='problem_submission'),
    path('bill/',bill,name='bill'),
    path('mechlogout/', mechanic_logout, name='mechanic_logout'),
    path('process_payment/', process_payment, name='process_payment'),
    path('feedback/',feedback, name='feedback'),
    path('feedback/thankyou/', feedback_thankyou, name='feedback_thankyou'),
    path('displayfeed/',displayfeedbacks,name='displayfeedbacks'),
    path('our/',ourservices,name='ourservices'),
    path('cushome/',customerhome,name='customerhome'),
    path('r/',regsub,name='regsub'),
    path('cash/',cash,name='cash')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)