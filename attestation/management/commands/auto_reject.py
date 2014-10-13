# -*- coding: utf-8 -*-
from django.core.mail.message import EmailMessage
from django.core.management.base import BaseCommand

from attestation.models import RequestFlow, Request, RequestStatus
from datetime import datetime, timedelta


class Command(BaseCommand):
    help = 'Auto reject requests'

    def handle(self, *args, **options):
        reqs = Request.objects.filter(status__is_new=True, doc_date__isnull=True)

        flows = RequestFlow.objects.select_related('status', 'request').filter(
            request__in=reqs,
            date__gte=datetime(2014, 10, 1, 0)  # routine enable date
        )

        by_request = {}
        for f in flows:
            by_request.setdefault(f.request, []).append(f)

        for request in by_request.keys():
            print request.pk
            request_flows = by_request[request]
            if len(request_flows) == 1:
                fl = request_flows[0]
                if fl.status.is_new and datetime.today() - fl.date > timedelta(days=16):
                    self.stdout.write(u'ID: %s, fio: %s' % (request.id, request.fio()))
                    status = RequestStatus.objects.filter(is_rejected=True)[0]
                    new_flow = RequestFlow()
                    new_flow.request = request
                    new_flow.status = status
                    new_flow.save()
                    request.status = status
                    request.save()
                elif fl.status.is_new and datetime.today() - fl.date >= timedelta(days=10):
                    # send caution message
                    due_date = fl.date + timedelta(days=16)
                    msg = EmailMessage(
                        subject=u'Аттестация',
                        body=u'Внимание!\nПоследний срок сдачи документов по Вашему заявлению в аттестационную комиссию'
                             u' %s. Документы необходимо отправить на электронный адрес att@iro86.ru.\n\n' %
                             due_date.strftime('%d.%m.%Y') +
                             u'Если документы не будут получены, заявление будет автоматически отклонено!',
                        to=(request.email, ),
                        from_email='att@iro86.ru'
                    )
                    msg.send(fail_silently=True)