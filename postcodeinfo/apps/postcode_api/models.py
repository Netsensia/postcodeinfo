from django.contrib.gis.db import models
from django.db.models import Count, signals
from django.dispatch import receiver

from .utils import AddressFormatter


class AddressManager(models.GeoManager):

    def bulk_create(self, objs, batch_size=None):
        for obj in objs:
            signals.pre_save.send(sender=Address, instance=obj)
        super(AddressManager, self).bulk_create(objs, batch_size=batch_size)


class Address(models.Model):
    uprn = models.CharField(max_length=12, primary_key=True)
    os_address_toid = models.CharField(max_length=20, default='', blank=True)
    rm_udprn = models.CharField(max_length=8)
    organisation_name = models.CharField(max_length=60, default='', blank=True)
    department_name = models.CharField(max_length=60, default='', blank=True)
    po_box_number = models.CharField(max_length=6, default='', blank=True)
    building_name = models.CharField(max_length=50, default='', blank=True)
    sub_building_name = models.CharField(max_length=30, default='', blank=True)
    building_number = models.PositiveSmallIntegerField(null=True, blank=True)
    dependent_thoroughfare_name = models.CharField(
        max_length=80, default='', blank=True)
    thoroughfare_name = models.CharField(max_length=80, default='', blank=True)
    post_town = models.CharField(max_length=30, default='', blank=True)
    double_dependent_locality = models.CharField(
        max_length=35, default='', blank=True)
    dependent_locality = models.CharField(
        max_length=35, default='', blank=True)
    point = models.PointField()
    postcode = models.CharField(max_length=8)
    postcode_index = models.CharField(max_length=7, db_index=True)
    postcode_area = models.CharField(
        max_length=4, db_index=True, blank=True, default='')
    postcode_type = models.CharField(max_length=1)
    rpc = models.PositiveSmallIntegerField()
    change_type = models.CharField(max_length=1)
    start_date = models.DateField()
    last_update_date = models.DateField()
    entry_date = models.DateField()
    primary_class = models.CharField(max_length=1)
    process_date = models.DateField()

    objects = AddressManager()

    def __unicode__(self):
        return u"%s - %s" % (self.uprn, self.postcode)

    class Meta:
        verbose_name_plural = 'addresses'
        ordering = ['building_number', 'building_name', 'sub_building_name']
        index_together = [
            ['postcode_index', 'uprn']
        ]
        
    @property
    def formatted_address(self):
        return AddressFormatter.format(self)


@receiver(signals.pre_save, sender=Address)
def address_pre_save(sender, instance, *args, **kwargs):
    instance.postcode_area = instance.postcode.split(' ')[0].lower()


class PostcodeGssCode(models.Model):
    postcode_index = models.CharField(
        max_length=7, db_index=True, primary_key=True)
    local_authority_gss_code = models.CharField(max_length=9, db_index=True)


class LocalAuthorityManager(models.Manager):

    def for_postcode(self, postcode):
        postcode_to_gss_code_mapping = PostcodeGssCode.objects.filter(
            postcode_index=postcode).first()
        if postcode_to_gss_code_mapping:
            gss_code = postcode_to_gss_code_mapping.local_authority_gss_code
            return self.filter(gss_code=gss_code).first()
        else:
            postcodes = Address.objects.filter(postcode_area=postcode)\
                .values_list('postcode_index', flat=True)\
                .distinct()
            gss_codes = PostcodeGssCode.objects.filter(
                postcode_index__in=postcodes).\
                values('local_authority_gss_code').\
                annotate(count=Count('local_authority_gss_code')).\
                order_by("-count")

            most_likely_gss_code = gss_codes.first()[
                'local_authority_gss_code']
            return self.filter(gss_code=most_likely_gss_code).first()


class LocalAuthority(models.Model):
    gss_code = models.CharField(max_length=9, db_index=True, primary_key=True)
    name = models.CharField(max_length=128, db_index=True)

    objects = LocalAuthorityManager()


class Download(models.Model):
    url = models.CharField(max_length=2048, db_index=True)
    last_modified = models.DateTimeField(auto_now=False, db_index=True)
    etag = models.CharField(max_length=2048, db_index=True, null=True)
    local_filepath = models.CharField(max_length=2048, db_index=True)
    state = models.CharField(max_length=16, db_index=True)
    last_state_change = models.DateTimeField(auto_now=False)
