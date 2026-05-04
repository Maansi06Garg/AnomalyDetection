from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import requests
import json

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.mail import send_mail
from datetime import timedelta

from config import settings
from .forms import LoginForm, SignupForm
from .models import User

def signup_view(request):
    form = SignupForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        return redirect('login')

    return render(request, 'detector/signup.html', {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            return redirect('home')

    return render(request, 'detector/login.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
def home(request):
    return render(request, 'detector/home.html', {
        'user': request.user
    })

@csrf_exempt
@login_required
def predict_api(request):

    if request.method != "POST":
        return JsonResponse({
            "error": "Only POST requests are allowed"
        }, status=405)

    try:
        data = json.loads(request.body)

        sequence = data.get("sequence")

        if sequence is None:
            return JsonResponse({
                "error": "Sequence is required"
            }, status=400)

        response = requests.post(
            "https://maximum-unzip-goggles.ngrok-free.dev/predict",
            json={"sequence": sequence},
            timeout=10
        )

        result = response.json()

        probability = result.get("anomaly_probability", 0)
        

        if probability > 70:
            status = "Critical Alert"
        elif probability > 50:
            status = "Warning"
        else:
            status = "Normal"
        send_alert_if_needed(request.user, probability)

        return JsonResponse({
            "sequence_length": len(sequence),
            "probability": round(probability, 2),
            "status": status
        })

    except requests.exceptions.RequestException as e:
        return JsonResponse({
            "error": "Failed to connect to ML server",
            "details": str(e)
        }, status=500)

    except json.JSONDecodeError:
        return JsonResponse({
            "error": "Invalid JSON format"
        }, status=400)

    except Exception as e:
        return JsonResponse({
            "error": "Unexpected server error",
            "details": str(e)
        }, status=500)

def send_alert_if_needed(user, anomaly_percentage):
    if anomaly_percentage < 70:  # threshold
        return

    now = timezone.now()

    if user.last_alert_sent:
        diff = now - user.last_alert_sent
        if diff < timedelta(hours=1):
            return  # ⛔ skip sending

    # ✅ send email
    send_mail(
        subject="⚠️ Critical Anomaly Alert",
        message=f"Critical anomaly detected: {anomaly_percentage}%",
        from_email=None,
        recipient_list=[user.email],
    )

    # ✅ update last sent time
    user.last_alert_sent = now
    user.save()
