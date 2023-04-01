from django.urls import path
from .views import (
    BookingDateView, DetaiDoctorInfoView,
    DoctorListCardView, HomeView, query_result
)


urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('team/', DoctorListCardView.as_view(), name='team'),
    path('doctor-info/<int:pk>/', DetaiDoctorInfoView.as_view(), name='doc_info'),
    path('query-result/', query_result, name='query_result'),
    path('booking-date/', BookingDateView.as_view(), name='booking_date'),
]
