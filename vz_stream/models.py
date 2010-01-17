from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from pprint import pprint
from string import find
import re

from utils import feedparser
import datetime

USER_AGENT = 'vz_stream/0.1 +http://jobscry.net'

TWITTER_AT = re.compile(r'@([^\s]+)')
TWITTER_AT_REPLACE = r'<a href="http://twitter.com/\1" title="\1 twitter feed">@\1</a>'
TWITTER_HASH = re.compile(r'#([^\s]+)')
URL = re.compile(r'(http://[^\s\)]+)', re.I)

class Source(models.Model):
    """
    Source
    
    A unique URL to retireve entries from.  If the last updated is a success
    the datetime is updated in last_update, if not, last_update_successful is
    set to False and the error message is saved in error_message for trouble-
    shooting purposes.
    """
    TYPE_CHOICES = (
        ('o', 'Other'),
        ('t', 'Twitter'),
    )

    name  = models.CharField(blank=True, max_length=100)
    feed_type = models.CharField(max_length=2, choices=TYPE_CHOICES)
    url = models.URLField(unique=True, verify_exists=True)
    enabled = models.BooleanField(default=True)
    auto_link = models.BooleanField(default=False, help_text="Auto Link URLS in feed's entries?")
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
        
        if self.enabled is False:
            return

        if self.last_modified:
            modified = self.last_modified.timetuple()
        else:
            modified = None

        data = feedparser.parse(self.url, etag=self.etag,
            modified=modified, agent=USER_AGENT)

        if data.bozo != 1:
            if data.status != 304:
                data.entries.reverse()
                while data.entries:
                    dentry = data.entries.pop()

                    if dentry.has_key('published'):
                        created_on = datetime.datetime(*dentry.published_parsed[0:6])
                    else:
                        created_on = datetime.datetime(*dentry.updated_parsed[0:6])

                    if self.last_modified is not None and (created_on < self.last_modified):
                        break

                    if dentry.has_key('title'):
                        text = dentry.title
                    elif dentry.has_key('summary'):
                        text = dentry.summary
                    else:
                        dentry.get('content', 'None')

                    if self.auto_link:
                        text = self._auto_link(text)

                    if self.feed_type == 't':
                        text = self._twitter_parser(text)

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
                    try:
                        latest = Entry.objects.filter(source=self).latest('created_on')
                        self.last_modified = latest.created_on
                    except ObjectDoesNotExist:
                        pass

            self.last_update_successful = True
            self.last_status_code = data.status
        else:
            self.last_update_successful = False
            self.error_message = pprint(data.bozo_exception)
        self.save()


    def _twitter_parser(self, text):
        """
        Twitter Parser
        
        Special parsing for twitter feeds.
        
        First, remove USERNAME: from text.  This is characters 0 to n, where n is the first
        occurence of ":".
        
        Second, replace any @USERNAME with <a href="http://twitter.com/USERNAME"
        title="USERNAME's twitter feed">USERNAME</a>.
        
        Third, replace #TOPIC with <a href="http://twitter.com/#search?q=%23TOPIC" title="#TOPIC">
        #TOPIC</a>.
        """
        username = find(text, ':')
        if username > -1:
            text = text[username+2:]
        
        text = TWITTER_AT.sub(TWITTER_AT_REPLACE, text)
        text = TWITTER_HASH.sub(r'<a href="http://twitter.com/#search?q=%23\1" title="\1">#\1</a>', text)
        
        return text


    def _auto_link(self, text):
        """
        Auto Link

        If the source's auto_link option is True, turn urls into links.
        """
        return URL.sub(r'<a href="\1">\1</a>', text)


    def __unicode__(self):
        return self.name

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
        ordering = ['-created_on']


    def __unicode__(self):
        return u"From %s on %s"%(self.source, self.retrieved_on.strftime('%d %b %y @ %H:%M:%S'))
