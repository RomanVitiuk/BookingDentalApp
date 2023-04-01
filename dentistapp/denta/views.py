from datetime import datetime

from django.db.models import Q
from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView

from .models import Client, DentistDoctor


class HomeView(TemplateView):
    template_name = 'denta/home.html'


class DoctorListCardView(ListView):
    model = DentistDoctor
    template_name = 'denta/team.html'
    context_object_name = 'doctors'


class DetaiDoctorInfoView(DetailView):
    model = DentistDoctor
    template_name = 'denta/doctor_info.html'
    context_object_name = 'doc'


class BookingDateView(CreateView):
    model = Client
    fields = '__all__'
    template_name = 'denta/booking_date.html'
    success_url = reverse_lazy('home')

    def dispatch(self, request):
        """
        I'm override dispatch method because I want to
        ensure the redirect will be only when post
        data was successful. To check this logic I'm
        defind __is_free_visit_time.
        """
        if 'doc' in request.POST and 'visit_date' in request.POST:
            doc = DentistDoctor.objects.get(pk=request.POST.get('doc'))
            date = datetime.fromisoformat(request.POST.get('visit_date'))

        if request.method == "POST" and self.__is_free_visit_time(doc, date):
            messages.success(
                request, 'Booking was successful! See you soon!!!'
            )
            return self.post(request)
        else:
            return self.get(request)

    def __is_free_visit_time(self, doc, v_date):
        """
        Check if doctor have free time to visit.
        We filter Client table records by doctor
        instance and prefer date to visit.
        """
        year = v_date.year
        month = v_date.month
        day = v_date.day
        hour = v_date.hour
        minute = v_date.minute
        tmp = Client.objects.filter(
            doc=doc,
            visit_date__year=year,
            visit_date__month=month,
            visit_date__day=day,
            visit_date__hour=hour,
            visit_date__minute=minute,
        ).count()
        return tmp == 0 and type(tmp) is int


def query_result(request):
    """
    Result of search query will be doctor card
    or message about missing data by query.
    We are filtering data by 3 parameters:
    - first name doctor;
    - last name doctor;
    - edication grade doctor.
    If we match one of these parameters we
    will get relevant search result.
    """
    query = request.GET.get("query")
    doctors = DentistDoctor.objects.filter(
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(edication_grade__icontains=query)
    )
    return render(request, 'denta/team.html', {'doctors': doctors})
