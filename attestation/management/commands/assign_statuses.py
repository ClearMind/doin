# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from attestation.models import RequestFlow


class Command(BaseCommand):
    help = 'Denormalize statuses'

    def handle(self, *args, **options):

        flows = RequestFlow.objects.select_related('status', 'request').order_by('date')

        by_request = {}
        for f in flows:
            by_request.setdefault(f.request, []).append(f)

        count = len(by_request.keys())
        print 'Requests: %s' % count
        every = count / 100

        i = 0
        percent = 0
        for request in by_request.keys():
            request.status = by_request[request][-1].status
            request.save()
            i += 1
            if i % every == 0:
                percent += 1
                print '%s%%' % percent