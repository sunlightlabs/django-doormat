from django.conf import settings
from doormat.models import DoorMat
from urlparse import urlparse
import re

IGNORED_REFERRERS = getattr(settings, 'DOORMAT_IGNORED_REFERRERS', [])
IGNORED_REFERRERS = [re.compile(d, re.I) for d in IGNORED_REFERRERS]

class DoorMatMiddleware(object):

    def process_request(self, request):

        request.doormat = None
    
        # check for manual doormat request
    
        if request.user.is_staff and 'referrer' in request.GET:
            
            ref = request.GET['referrer']
            if not ref.startswith('http://'):
                ref = "http://%s" % ref
        
            url_parts = urlparse(ref)
        
            request.doormat = DoorMat.objects.find_one(url_parts.netloc, url_parts.path)
        
        else:
    
            # these are all just test to see if we should bypass doormat
    
            referrer = request.META.get('HTTP_REFERER', None)
            if not referrer:
                return None # no referrer, so bail now
    
            if request.session.get('has_seen_doormat', False):
                return None # bail if user has seen doormat
    
            url_parts = urlparse(referrer)
    
            for domain_re in IGNORED_REFERRERS:
                if domain_re.match(url_parts.netloc):
                    return None # matched ignored referrer, so bail now
    
            # we made it through the tests so lets find a doormat
            request.doormat = DoorMat.objects.find_one(url_parts.netloc, url_parts.path)
            request.session['has_seen_doormat'] = True

        