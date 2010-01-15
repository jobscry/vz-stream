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

Templates
---------

Templates follow the [Django Best Practices](http://lincolnloop.com/django-best-practices/apps/modules/templates.html "Django Best Practices").

Template Blocks for __stream\_view.html__

* extends _base.html_
* _content\_title
* _content_

Template Blocks for __stream\_stats.html__

* extends _base.html_
* _extra\_head_ - only if you want the jQuery Visualize graphs
* _content\_title
* _content_