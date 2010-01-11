from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response
from django.template import RequestContext
from models import Entry, Source

NUM_ENTRIES = 20

def view_stream(request, pk):
    """
    View Stream
    
    Grabs last NUM_ENTRIES entries for specified source, identified by pk (primary key).
    If pk is None, grab NUM_ENTRIES entries for all sources.
    """
    if pk is None:
        source = None
        entries = get_list_or_404(Entry)
    else:
        source = get_object_or_404(Source, pk=pk)
        entries = get_list_or_404(Entry, source=source)
    return render_to_response(
        'vz_stream/stream_view.html',
        { 'entries': entries[0:20], 'source': source, },
        context_instance=RequestContext(request)
    )
        
def update(request, pk):
    if pk is None:
        sources = get_list_or_404(Source)
    else:
        sources = get_list_or_404(Source, pk=pk)
        
    for source in sources:
        source.update()
    return ''
