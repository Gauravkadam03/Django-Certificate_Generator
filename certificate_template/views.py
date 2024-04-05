from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
import pandas as pd

from main import settings
# from .models import Student
import cv2
import os



# Create your views here.
@login_required
def first(request):
    return render(request,'generator/index.html ')


def signin(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        usrname = request.POST['username']
        passwd = request.POST['password']
        user = authenticate(request, username = usrname, password = passwd) #None
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request,'Invalid Login Credentials!!')
            return render(request,'generator/signin.html ')
        
    return render(request,'generator/signin.html ')


def upload_excel(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        
        # Read Excel file into a pandas DataFrame
        df = pd.read_excel(file)
        print(df.columns)
        
        # Iterate over each row and create Student objects
        for index, row in df.iterrows():
            name = row['name']
            course = row['course']
            # Student.objects.create(name=name, course=course)
        
        return HttpResponse('wow')
    

def generate_certificate_image(name):
    # Generate the certificate
    
    certificate_template_image = cv2.imread("C:\\Users\\acer\\Desktop\\python\\certificate_generator\\certificate_template\\certificate-template.jpg")
    cv2.putText(certificate_template_image, name.strip(), (815, 1500), cv2.FONT_HERSHEY_SIMPLEX, 3, (0, 0, 250), 5, cv2.LINE_AA)
    return certificate_template_image

def send_certificate_email(request):
    if request.method == 'GET':
        name = 'garry'
        certificate_image = generate_certificate_image(name)
        
        # Save the generated certificate image temporarily
        temp_image_path = os.path.join(settings.MEDIA_ROOT, 'temp_certificate.jpg')
        cv2.imwrite(temp_image_path, certificate_image)
        
        # Create EmailMessage object
        email = EmailMessage(
        'Certificate',
        'Attached is your certificate.',
        settings.EMAIL_HOST_USER,  # Sender's email address
        ['8600766907gaurav@gmail.com']  # Recipient's email address
        )

        # Attach the certificate image
        with open(temp_image_path, 'rb') as file:
            email.attach(f'{name}-certificate.jpg', file.read(), 'image/jpeg')

        # Send the email
        email.send()
            
            # Delete the temporary image file
        os.remove(temp_image_path)
        
        return HttpResponse('Certificate sent successfully!')
        
    
    # return render(request, 'send_certificate.html')