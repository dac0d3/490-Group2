from django.shortcuts import render

# Create your views here.


def open_index(request):
    return render(request,"index.html")