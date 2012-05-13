from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from boxes.models import Box, BoxItem
import datetime

class Terms(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    timeframe = models.CharField(max_length=50)
    type = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "terms"

    def __unicode__(self):
        return self.name

class Account(models.Model):

    terms = models.ForeignKey(Terms)
    slug = models.CharField(max_length=10, help_text="Enter a code to describe account. (e.g. MTF) <em>max 10</em>")
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=30)
    zip = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    email = models.CharField(max_length=100)

    def next_location(self):

        # Get the latest box based on its id
        box = Box.objects.filter(account=self.id).latest('id')

        # Num of empty locations given by empty accession fields
        empty_locations = BoxItem.objects.filter(used=False, box=box.id).count()

        # If box is full, create a new one
        if not empty_locations:
            latest_box = Box.objects.filter(account=self.id).latest('id')
            box = Box()
            box.account = self
            box.number = int(latest_box.number) + 1
            box.save()

            next_location = BoxItem.objects.get(box=box.id, slot='A1')

            return int(next_location.id)

        # Get the highest location value as an integer
        last_location_id = BoxItem.objects.filter(box=box.id).latest('id')
        last_location_id = int(last_location_id.id)

        # Next location_id value is last_location - empty_locations + 1
        next_location = last_location_id - empty_locations + 1

        return next_location

    def append(self, user, num_serum, num_plasma, accession, donor_id = None):

        if num_serum > 0:
            for i in range(num_serum):
                # Get next location id for account
                next_location = self.next_location()
                print 'Next Location: ' + str(next_location)

                # Create BoxItem object based on next_location
                location = BoxItem.objects.get(id=next_location)

                # Set location data and save to database
                location.accession  = accession
                location.donor_id   = donor_id
                location.tube_type  = 'serum'
                location.user       = user
                location.date       = datetime.datetime.today()
                location.used       = True
                location.save()

        if num_plasma > 0:
            for i in range(num_plasma):
                # Get next location id for account
                next_location = self.next_location()

                # Create BoxItem object based on next_location
                location = BoxItem.objects.get(id=next_location)

                # Set location data and save to database
                location.accession  = accession
                location.donor_id   = donor_id
                location.tube_type  = 'plasma'
                location.user       = user
                location.date       = datetime.datetime.today()
                location.used       = True
                location.save()

    def settings(self):
        settings = Settings.objects.get(account_id=self.id)
        return settings

    def __unicode__(self):
        return self.name


# Create first box if new account is created
@receiver(post_save,  sender=Account)
def account_receive(sender, **kwargs):

    # If instance is new and not updated
    created = kwargs.get('created')
    if created:
        name = kwargs.get('instance') # Instance = account name (unicode def in Account)
        account = Account.objects.get(name=name)

        # create first box
        box = Box()
        box.account_id = account.id
        box.number = 1
        box.save()

class Settings(models.Model):
    account = models.ForeignKey(Account, primary_key=True)
    require_donor_id = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'settings'

class Current(models.Model):
    account_id = models.ForeignKey(Account, primary_key=True)
    box_id = models.ForeignKey('boxes.Box')
    location_id = models.ForeignKey('boxes.BoxItem')

    def __unicode__(self):
        return self.location_id