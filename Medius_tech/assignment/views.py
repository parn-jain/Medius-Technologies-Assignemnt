from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.conf import settings
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from django.core.mail import send_mail
from .forms import FileUploadForm
import  os
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', 'default_password')

def home(request):
    form = FileUploadForm()
    return render(request, 'home.html', {'form': form})

def upload_file(request):   
    context = {}
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            file_type = file.name.split('.')[-1].lower()
            
            if file_type in ['xlsx', 'xls']:
                data = pd.read_excel(file)
            elif file_type == 'csv':
                data = pd.read_csv(file)
            else:
                context['error'] = 'Unsupported file type'
                return render(request, 'home.html', context)

    
            summary = generate_summary(data)
            request.session['summary'] = summary
            context['summary'] = summary
            
            context['success'] = 'File uploaded and email sent!'
        else:
            context['error'] = 'Form is not valid'

    return render(request, 'uploads.html', context)

def generate_summary(data):
    data = data.groupby(['Cust State', 'Cust Pin']).count().reset_index()[['Cust State', 'Cust Pin', 'DPD']]
    summary = data.to_html(classes='table table-striped', border=0)
    return summary






def send_summary_email(request):
    if request.method == 'POST':
        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        sender_email = 'pjisvgreat@gmail.com'
        receiver_email = 'tech@themedius.ai'
        cc_email = 'yash@themedius.ai'
        password = EMAIL_PASSWORD
        
        subject = 'Python Assignment - Parn Jain 9399374451'
        summary = request.session.get('summary', 'No summary available') 

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Cc'] = cc_email
        message['Subject'] = subject
        message.attach(MIMEText(summary, 'html'))  
        server = None
        
        try:
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()  
            server.login(sender_email, password)  
            text = message.as_string()  
            all_recipients = [receiver_email] + [cc_email]
            server.sendmail(sender_email, all_recipients, text)
            print('Email sent successfully!')
        except Exception as e:
            print(f'Failed to send email: {e}')
        finally:
            server.quit() 
        
        return redirect('home-page') 

    return render(request, 'home.html')