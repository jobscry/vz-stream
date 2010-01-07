from django.db import models

from jogging import logging

from pprint import pprint

USER_AGENT = 'vz_stream/0.1 +http://jobscry.net'

class Source(models.Model):
    """
    Source
    
    A unique URL to retireve entries from.  If the last updated is a success
    the datetime is updated in last_update, if not, last_update_successful is
    set to False and the error message is saved in error_message for trouble-
    shooting purposes.
    """
    name  = models.CharField(blank=True, max_length=100)
    url = models.URLField(unique=True, verify_exists=True)
    etag = models.CharField(blank=True, null=True, max_length=255)
    last_modified = models.DateTimeField(blank=True, null=True)
    last_status_code = models.IntegerField(blank=True, null=True)
    last_update_successful = models.BooleanField(default=False)
    error_message = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(editable=False, auto_now_add=True)
    modified = models.DateTimeField(editable=False, auto_now=True)


    def update(self):
        """
        Update
        
        Uses FeedParser to grab and parse feed.
        
        
        """
        from utils import feedparser
        import datetime
        
        if self.last_modified:
            modified = self.last_modified.timetuple()
        else:
            modified = None

        data = feedparser.parse(self.url, etag=self.etag,
            modified=modified, agent=USER_AGENT)

        if data.bozo != 1:
            if data.status != 304:
                while data.entries:
                    dentry = data.entries.pop()

                    if dentry.has_key('published'):
                        created_on = datetime.datetime(*dentry.published_parsed[0:6])
                    else:
                        created_on = datetime.datetime(*dentry.updated_parsed[0:6])

                    if self.last_modified and (created_on < self.last_modified):
                        break

                    if dentry.has_key('summary'):
                        text = dentry.summary
                    elif dentry.has_key('title'):
                        text = dentry.title
                    else:
                        dentry.get('content', 'None')

                    Entry.objects.create(
                        source=self,
                        url=dentry.link,
                        text=text,
                        created_on=created_on
                    )

            if data.has_key('etag'):
                self.etag = data.etag
            if data.has_key('modified'):
                self.last_modified = datetime.datetime(*data.modified[0:6])
            else:
                self.last_modified = datetime.datetime.now()

            self.last_update_successful = True
            self.last_status_code = data.status
        else:
            self.last_update_successful = False
            self.error_message = pprint(data.bozo_exception)
        self.save()


    def __unicode__(self):
        return u"%s"%(self.name)

class Entry(models.Model):
    """
    Entry
    
    An individual entry from a Source.
    """
    source = models.ForeignKey(Source)
    url = models.URLField(verify_exists=False)
    text = models.TextField()
    created_on = models.DateTimeField(editable=False)
    retrieved_on = models.DateTimeField(editable=False, auto_now_add=True)


    class Meta:
        verbose_name_plural = 'Entries'


    def __unicode__(self):
        return u"From %s on %s"%(self.source, self.retrieved_on.strftime('%d %b %y @ %H:%M:%S'))
