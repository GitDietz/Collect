import logging

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db import DatabaseError
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect, Http404, redirect

from .models import Country


def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "upload_csv.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request, 'File is not CSV type')
            return HttpResponseRedirect(reverse("core:upload_csv"))
            # if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request, "Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("core:upload_csv"))

        file_data = csv_file.read().decode("utf-8")

        lines = file_data.split("\n")
        # loop over the lines and save them in db. If error , store as string and then display
        for line in lines:
            fields = line.split(",")
            data_dict = {"entity": fields[0], "currency": fields[1], "currency_code": fields[2]}
            try:
                Country.objects.create(name=data_dict["entity"], currency=data_dict["currency"],
                                       currency_code=data_dict["currency_code"])

            except Exception as e:
                logging.getLogger("error_logger").error(repr(e))
            pass

    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file. "+repr(e))
        messages.error(request, "Unable to upload file. "+repr(e))

    return HttpResponseRedirect(reverse("myapp:upload_csv"))


def admin(request):
    template = 'base_admin.html'
    context = {
    }
    return render(request, template, context)