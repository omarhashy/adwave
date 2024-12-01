from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .mongo_conection import *


@login_required(login_url="login")
def index(request):

    return render(request, "index/index.html")


@login_required(login_url="login")
def upload_products(request):
    try:
        if request.method == "POST" and "file" in request.FILES:
            file = request.FILES["file"]
            if file.name.endswith(".csv"):
                re = load_products_data(file, request.user.username)
                if re != None:
                    messages.error(
                        request,
                        re,
                    )
                    return redirect("upload_data")
                messages.success(request, "Your file has been uploaded.")
                return redirect("index")
            else:
                messages.error(
                    request,
                    "Please upload an .csv file.",
                )
            return redirect("upload_data")
    except:
        messages.error(
            request,
            "error",
        )

    return render(request, "index/upload_d.html")


@login_required(login_url="login")
def upload_sales(request):
    if request.method == "POST" and "file" in request.FILES:
        file = request.FILES["file"]
        if file.name.endswith(".csv"):
            re = feed_the_graph(file, request.user.username)
            if re != None:
                messages.error(
                    request,
                    re,
                )
                return redirect("upload_data")

            messages.success(request, "Your file has been uploaded.")
            return redirect("index")

        else:
            messages.error(
                request,
                "Please upload an .csv file.",
            )

    return render(request, "index/upload_sales.html")


@login_required(login_url="login")
def send_emails(request):
    recomend(request.user.username)
    messages.success(request, "emails sent successfully.")
    return redirect("index")
