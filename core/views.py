import time
from django.http import HttpResponse


# Create your views here.
def home(request):
    # time.sleep(2)  # Simulate a delay of 2 seconds
    return HttpResponse("Hello, World!")


def private(request):
    return HttpResponse("This is a private page. You are logged in.")
