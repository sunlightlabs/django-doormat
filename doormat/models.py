from django.db import models
import datetime
import doormat

# models

class DoorMatManager(models.Manager):
    
    def find_one(self, domain, path=''):
        
        # prep parameters
        domain = doormat.clean_domain(domain)
        path = doormat.clean_path(path)
        
        # get basic queryset
        qs = DoorMat.objects.filter(domain=domain, is_enabled=True)
        
        for dm in qs.order_by('-path'):
            if path.startswith(dm.path):
                return dm

class DoorMat(models.Model):
    objects = DoorMatManager()
    domain = models.CharField(max_length=128)
    path = models.CharField(max_length=255, default="", blank=True)
    is_enabled = models.BooleanField(default=False)
    content = models.TextField(blank=True)
    last_published = models.DateTimeField(blank=True, null=True)
    
    class Meta:
        get_latest_by = 'last_published'
        ordering = ('domain','path')
    
    def __unicode__(self):
        return u"%s%s" % (self.domain, self.path)
    
    def save(self, **kwargs):
        
        self.domain = doormat.clean_domain(self.domain)
        self.path = doormat.clean_path(self.path)
        
        if not self.is_enabled:
            self.last_published = None
        elif self.is_enabled and self.last_published is None:
            self.last_published = datetime.datetime.utcnow()
        
        super(DoorMat, self).save(**kwargs)