from django.db.models import Count
from django.shortcuts import get_list_or_404, get_object_or_404, render_to_response
from django.template import RequestContext
from django.views.decorators.cache import cache_page
from models import Entry, Source

import datetime, calendar

NUM_ENTRIES = 20

@cache_page(60 * 15)
def stream_stats(request, year=None, month=None, template='vz_stream/stream_stats.html'):
    """
    Stream Stats
    
    total_entries: integer
    entries_by_source:
        {
            source: num_entries,
        }
    
    """
    sources = get_list_or_404(Source)
    num_entries = Entry.objects.all().count()

    data = Entry.objects.values('source__name').annotate(count=Count('source')).order_by().select_related()
    
    today = datetime.date.today()
    if year is None:
        year = today.year
    if month is None:
        month = today.month
    
    date = datetime.date(month=month, year=year, day=1)
    
    month_data = Entry.objects.filter(
        created_on__year=date.year,
        created_on__month=date.month
    ).values('source__name').annotate(count=Count('source')).order_by().select_related()

    day_data = dict()
    day_range = range(1, calendar.monthrange(date.year, date.month)[1]+1)
    for day in day_range:
        if day > 0:
            for source in sources:
                if source.name not in day_data:
                    day_data[source.name] = dict()
                day_data[source.name][day] = Entry.objects.filter(
                        source=source,
                        created_on__year=date.year,
                        created_on__month=date.month,
                        created_on__day=day
                    ).count()
            if 'all sources' not in day_data:
                day_data['all sources'] = dict()
            day_data['all sources'][day] = Entry.objects.filter(
                created_on__year=date.year,
                created_on__month=date.month,
                created_on__day=day
            ).count()            

    return render_to_response(
        'vz_stream/stream_stats.html',
        {
            'num_entries': num_entries,
            'sources': sources,
            'data': data,
            'date': date,
            'month_data': month_data,
            'day_data': day_data,
            'day_range': day_range
        },
        context_instance=RequestContext(request)
    )

@cache_page(60 * 15)
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
