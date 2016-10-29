from django.http import JsonResponse, Http404
from functools import wraps
import json, re

def locations(request):
	"""Generate list of term data source files
    Returns:
        if contains invalid queryString key, it will raise exception.
    """
	return JsonResponse({}, safe=False)

