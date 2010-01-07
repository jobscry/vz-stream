from django.shortcuts import get_list_or_404
from models import Source


def update(request, pk):
    if pk is None:
        sources = get_list_or_404(Source)
    else:
        sources = get_list_or_404(Source, pk=pk)
        
    for source in sources:
        source.update()
    return ''
