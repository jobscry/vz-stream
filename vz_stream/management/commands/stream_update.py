from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):
    help = 'Meant to be run as a Cron Job, checks for new entries on all enabled sources'

    def handle_noargs(self, **options):
        from vz_stream.models import Source
        verbosity = int(options.get('verbosity', 1))
        sources = Source.objects.filter(enabled=True)
        if verbosity >= 2:
            print 'found %s sources'%sources.count()
        for source in sources:
            if verbosity >= 2:
                print 'updating %s'%source
            source.update()
        if verbosity >= 2:
            print 'done'
        