import logging

from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from .forms import TicketForm
from .models import Ticket

logger = logging.getLogger(__name__)


def ticket_list(request):
    return render(request, "list.html", {"tickets": Ticket.objects.order_by("-pk")})


@require_http_methods(["GET", "POST"])
def ticket_form(request, pk=None):
    ticket = get_object_or_404(Ticket, pk=pk) if pk is not None else None
    form = TicketForm(request.POST if request.method == "POST" else None, instance=ticket)
    if request.method == "POST":
        if form.is_valid():
            ticket = form.save()
            logger.info("Өтінім сақталды (ID=%s)", ticket.pk)
            return redirect("ticket_list")
        logger.warning("Өтінім формасы тексеруден өтпеді")
    heading = "Өтінімді өңдеу" if ticket else "Жаңа өтінім"
    return render(request, "form.html", {"form": form, "heading": heading})


@require_http_methods(["GET", "POST"])
def ticket_delete(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == "POST":
        ticket.delete()
        return redirect("ticket_list")
    return render(request, "delete.html", {"ticket": ticket})
