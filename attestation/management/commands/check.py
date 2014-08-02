# -*- coding: utf-8 -*-
import datetime
from django.core.management.base import BaseCommand, CommandError
from django.db.models.signals import post_save

from attestation.models import RequestFlow, RequestStatus, Request, status_changed_slot


class Command(BaseCommand):
    help = 'Checks statuses for errors'

    def handle(self, *args, **options):
        requests = Request.objects.all()
        empty = []
        without_reg = []
        many_reg = []

        self.stdout.write("Gathering information about requests...\n")
        for r in requests:
            if r.requestflow_set.count() == 0:
                empty.append(r)
            else:
                isnew = r.requestflow_set.filter(status__is_new=True).all()
                if len(isnew) == 0:
                    without_reg.append(r)
                if len(isnew) > 1:
                    many_reg.append(r)


        i = 1
        for e in empty:
            self.stdout.write(
                "%s. Request #%s has %s flows and must be destroyed\n" % (i, e.pk, e.requestflow_set.count()))
            assert e.requestflow_set.count() == 0
            e.delete()
            i += 1
        self.stdout.write("\n")

        post_save.disconnect(status_changed_slot, sender=RequestFlow, dispatch_uid='request_flow_created_email')
        i = 1
        for w in without_reg:
            self.stdout.write("%s. Request #%s has no is_new statuses, new status must be created\n" % (i, w.pk))
            d = w.requestflow_set.order_by('date')[0].date
            self.stdout.write("\tlatest date: %s\n" % d)
            ns = RequestStatus.objects.get(is_new=True)
            new_rf = RequestFlow.objects.create(request=w, status=ns)
            new_rf.date = d - datetime.timedelta(days=1)
            new_rf.save()
            self.stdout.write("\tnew date:    %s\n" % new_rf.date)
            assert new_rf in w.requestflow_set.all()
            i += 1
        post_save.connect(status_changed_slot, sender=RequestFlow, dispatch_uid='request_flow_created_email')
        self.stdout.write("\n")

        ii = 1
        for m in many_reg:
            self.stdout.write("%s. Request #%s has many is_new statuses, only first status must be live\n" % (ii, m.pk))
            new_sts = m.requestflow_set.filter(status__is_new=True).order_by('date')
            for i in range(1, len(new_sts)):
                new_sts[i].delete()

            assert m.requestflow_set.filter(status__is_new=True).count() == 1
            ii += 1
        self.stdout.write("\n")