VZ Stream
=========

A Django powered life stream app.

Requirements
------------

* [Django 1.2+](http://www.djangoproject.com/ "Django Project")
* [Universal FeedParser](http://www.feedparser.org/ "Universal FeedParser")
* [jQuery 1.3+](http://jquery.com/ "jQuery") 
* [jQuery Visualize Plugin](http://www.filamentgroup.com/lab/jquery_visualize_plugin_accessible_charts_graphs_from_tables_html5_canvas/ "jQuery Visualize Plugin")

TODO
----

* templates
  * <del>view all entries</del>
  * <del>view entries by source</del>
  * view entries by date
  * <del>stream stats</del>
* search/filter entries
* <del>cron job script</del>

Features
--------

* *Smart* updating:  uses E-Tag or last-modified from headers to determine if source should be updated or not.  For feeds that have neither, only add entries newer than the source's last entry.
* Twitter parsing, if the feed is a twitter feed *@USER* is converted to a link, as well as *#TOPIC*.

Settings
--------

You can put *STREAM\_NUM\_ENTIRES* in your settings.py, this should be an integer.  This defines how many entries to get in the *stream\_view* view.  Defaults to 20.

Templates
---------

Templates follow the [Django Best Practices](http://lincolnloop.com/django-best-practices/apps/modules/templates.html "Django Best Practices").

Template Blocks for __stream\_view.html__

* extends _base.html_
* _content\_title_
* _content_

Template Blocks for __stream\_stats.html__

* extends _base.html_
* _extra\_head_ - only if you want the jQuery Visualize graphs
* _content\_title_
* _content_

Updating Your Life Stream
-------------------------

Included is a [custom Django-Admin Command](http://docs.djangoproject.com/en/dev/howto/custom-management-commands/#writing-custom-django-admin-commands) that will update your life stream.  This can be added to a cron task.

`python path/to/project/manage.py stream_update`
