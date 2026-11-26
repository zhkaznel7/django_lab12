from django.urls import path

from . import views

urlpatterns = [
    path("", views.ticket_list, name="ticket_list"),
    path("tickets/new/", views.ticket_form, name="ticket_create"),
    path("tickets/<int:pk>/edit/", views.ticket_form, name="ticket_edit"),
    path("tickets/<int:pk>/delete/", views.ticket_delete, name="ticket_delete"),
]
