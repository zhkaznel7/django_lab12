from django.test import TestCase
from django.urls import reverse

from .models import Ticket


class TicketViewsTests(TestCase):
    def setUp(self):
        self.url = reverse("ticket_create")
        self.data = {"title": "Желі істемейді", "description": "Сынақ сипаттамасы", "priority": "high"}

    def test_creation_and_display(self):
        self.assertContains(self.client.get(self.url), "Жаңа өтінім")
        with self.assertLogs("tickets.views", "INFO") as logs:
            response = self.client.post(self.url, self.data)
        ticket = Ticket.objects.get()
        self.assertRedirects(response, reverse("ticket_list"))
        self.assertEqual(ticket.status, Ticket.Status.NEW)
        self.assertIn(f"Өтінім сақталды (ID={ticket.pk})", logs.output[0])
        self.assertNotIn(self.data["description"], logs.output[0])
        for label in (ticket.title, "Жаңа", "Жоғары"):
            self.assertContains(self.client.get(reverse("ticket_list")), label)

    def test_short_title_is_rejected(self):
        with self.assertLogs("tickets.views", "WARNING") as logs:
            response = self.client.post(self.url, {**self.data, "title": "abc"})
        self.assertContains(response, "Тақырып кемінде 5 таңбадан тұруы керек.")
        self.assertFalse(Ticket.objects.exists())
        self.assertIn("Өтінім формасы тексеруден өтпеді", logs.output[0])

    def test_edit_and_delete(self):
        ticket = Ticket.objects.create(**self.data)
        edit = reverse("ticket_edit", args=[ticket.pk])
        delete = reverse("ticket_delete", args=[ticket.pk])
        self.assertContains(self.client.get(edit), ticket.title)
        with self.assertLogs("tickets.views", "INFO"):
            self.assertRedirects(self.client.post(edit, {**self.data, "title": "Желі баяу жұмыс істейді"}), "/")
        ticket.refresh_from_db()
        self.assertEqual(ticket.title, "Желі баяу жұмыс істейді")
        self.assertContains(self.client.get(delete), ticket.title)
        self.assertTrue(Ticket.objects.filter(pk=ticket.pk).exists())
        self.assertRedirects(self.client.post(delete), "/")
        self.assertFalse(Ticket.objects.filter(pk=ticket.pk).exists())
        self.assertEqual(self.client.get(edit).status_code, 404)

    def test_disallowed_host_is_logged(self):
        with self.settings(DEBUG=False, ALLOWED_HOSTS=["localhost"]):
            with self.assertLogs("django.security.DisallowedHost", "ERROR"):
                self.assertEqual(self.client.get("/", headers={"host": "127.0.0.1"}).status_code, 400)
            self.assertEqual(self.client.get("/", headers={"host": "localhost"}).status_code, 200)
