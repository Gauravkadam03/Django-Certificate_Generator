from django.core.mail import EmailMessage
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
import pandas as pd

from main import settings
from .models import Student
import cv2
import os
from datetime import date


@login_required
def index(request):
    return render(request, 'generator/index.html ')


def signin(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        usrname = request.POST['username']
        passwd = request.POST['password']
        user = authenticate(request, username=usrname, password=passwd)  # None
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Invalid Login Credentials!!')
            return render(request, 'generator/signin.html ')

    return render(request, 'generator/signin.html ')


@login_required
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
            email = row['email']
            Student.objects.create(name=name, course=course, email=email)
        data = Student.objects.filter(date_added=date.today())
        return render(request, 'generator/table.html', {'data': data})


@login_required
def list(request):
    data = Student.objects.all().order_by('-id')
    return render(request, 'generator/table.html', {'data': data})


def generate_certificate_image(name):
    certificate_template_image = cv2.imread(os.path.join(
        settings.IMAGE_ROOT, 'certificate-template.jpg'))
    text_size, _ = cv2.getTextSize(
        name.strip(), cv2.FONT_HERSHEY_TRIPLEX, 3, 5)
    text_width = text_size[0]
    text_height = text_size[1]
    # Center horizontally
    position_x = (certificate_template_image.shape[1] - text_width) // 2
    # Center vertically
    position_y = (certificate_template_image.shape[0] + text_height+200) // 2
    cv2.putText(certificate_template_image, name.strip(), (position_x,
                position_y), cv2.FONT_HERSHEY_TRIPLEX, 3, (8, 8, 8), 2, cv2.LINE_AA)
    return certificate_template_image


@login_required
def send_certificate_email(request, id):
    if request.method == 'POST':

        data = Student.objects.get(id=id)
        name = data.name
        certificate_image = generate_certificate_image(name)

        # Save the generated certificate image temporarily
        temp_image_path = os.path.join(
            settings.MEDIA_ROOT, 'temp_certificate.jpg')
        cv2.imwrite(temp_image_path, certificate_image)

        # Create EmailMessage object
        email = EmailMessage(
            f'Certificate {data.course}',
            'Attached is your certificate.',
            settings.EMAIL_HOST_USER,  # Sender's email address
            [data.email]  # Recipient's email address
        )

        # Attach the certificate image
        with open(temp_image_path, 'rb') as file:
            email.attach(f'{name}-certificate.jpg', file.read(), 'image/jpeg')

        # Send the email
        email.send()

        # Delete the temporary image file
        os.remove(temp_image_path)
        messages.success(
            request, f'Certificate Sent to {data.email} successfully.')
        return redirect('list')


def student_index(request):
    if request.method == 'POST':
        try:
            data = Student.objects.get(email=request.POST.get('email'))
            name = data.name
            certificate_image = generate_certificate_image(name)

            # Save the generated certificate image temporarily
            temp_image_path = os.path.join(
                settings.MEDIA_ROOT, 'temp_certificate.jpg')
            cv2.imwrite(temp_image_path, certificate_image)

            # Create EmailMessage object
            email = EmailMessage(
                f'Certificate {data.course}',
                'Attached is your certificate.',
                settings.EMAIL_HOST_USER,  # Sender's email address
                [data.email]  # Recipient's email address
            )

            # Attach the certificate image
            with open(temp_image_path, 'rb') as file:
                email.attach(f'{name}-certificate.jpg', file.read(), 'image/jpeg')

            # Send the email
            email.send()

            # Delete the temporary image file
            os.remove(temp_image_path)
            messages.success(
                request, f'Certificate Sent to {data.email} successfully.')
        except:
            messages.error(
                request, f'Enter valid email id ')
    return render(request, 'generator/s_index.html')


