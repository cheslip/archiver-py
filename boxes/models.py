from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
import datetime

box_locations = [
    "A1","A2","A3","A4","A5","A6","A7","A8","A9",
    "B1","B2","B3","B4","B5","B6","B7","B8","B9",
    "C1","C2","C3","C4","C5","C6","C7","C8","C9",
    "D1","D2","D3","D4","D5","D6","D7","D8","D9",
    "E1","E2","E3","E4","E5","E6","E7","E8","E9",
    "F1","F2","F3","F4","F5","F6","F7","F8","F9",
    "G1","G2","G3","G4","G5","G6","G7","G8","G9",
    "H1","H2","H3","H4","H5","H6","H7","H8","H9",
    "I1","I2","I3","I4","I5","I6","I7","I8","I9"
]

class Box(models.Model):
    account = models.ForeignKey('accounts.Account')
    number = models.IntegerField()

    class Meta:
        verbose_name_plural = "boxes"

    def create(self, account_id):
        box = Box()



    def __unicode__(self):
        return "Box " + str(self.number) + " (" + self.account.name + ")"

# Populate box if it was just created
@receiver(post_save, sender=Box)
def box_save_receive(sender, **kwargs):
    created = kwargs.get('created')
    if created:
        box = Box.objects.latest('id')
        boxItem = BoxItem()
        boxItem.populate(box.id)


class BoxItem(models.Model):
    box = models.ForeignKey(Box)
    slot = models.CharField(max_length=10)
    accession = models.CharField(max_length=20, blank=True)
    donor_id = models.CharField(max_length=100, blank=True)
    tube_type = models.CharField(max_length=100, blank=True)
    user = models.IntegerField(blank=True)
    date = models.DateTimeField(blank=True)
    used = models.BooleanField()

    def populate(self, box_id):

        global box_locations

        for i in box_locations:
            location = BoxItem()
            location.box_id = box_id
            location.slot = i
            location.save()


    def __unicode__(self):
        return str(self.id) + " - " + str(self.slot)


def get_datetime():
    date = datetime.datetime.today()
    date = date.strftime('%Y-%m-%d %H:%M:%S')

    return date
