from ipware import get_client_ip
from django.utils.deprecation import MiddlewareMixin
from django.contrib.gis.geoip2 import GeoIP2


"""
This file holds all the middlewares associated with user accounts.
"""


class RegionMiddleware(MiddlewareMixin):
    def process_request(self, request):
        ip, _ = get_client_ip(request)
        if ip is not None:
            try:
                g = GeoIP2()
                country = g.country(ip)
                request.region_code = country['country_code']
            except Exception as _:
                request.region_code = None
        else:
            request.region_code = None
