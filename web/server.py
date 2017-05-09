#!/usr/bin/env python
from __future__ import print_function

from collections import OrderedDict
import logging
import operator

from flask import Flask, make_response, render_template, request, url_for
from flask_flatpages import FlatPages
from raven.contrib.flask import Sentry


FLATPAGES_EXTENSION = '.md'


logging.basicConfig(format='%(asctime)-15s %(levelname)-6s %(message)s')

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# TODO: investigate flask-frozen
app = Flask(__name__, static_url_path='')
flatpages = FlatPages(app)
app.config.from_object(__name__)
sentry = Sentry(app, logging=True, level=logging.WARNING)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/blog')
def blog():
    posts = [p for p in flatpages]
    posts.sort(key=operator.itemgetter('date'), reverse=True)

    by_date = OrderedDict()
    by_tag = dict()
    for post in posts:
        for tag in post.meta.get('tags', '').split(', '):
            tag = tag or 'Untagged'
            by_tag[tag] = by_tag.get(tag, list())
            by_tag[tag].append(post)

        by_date[post['date'].year] = by_date.get(post['date'].year, list())
        by_date[post['date'].year].append(post)

    filter_tag = request.args.get('tag')
    if by_tag.get(filter_tag):
        return render_template('blog.html', by_date=by_date, by_tag=by_tag,
                               filter_tag=filter_tag,
                               recent=by_tag[filter_tag])
    # TODO: handle bad tag filter
    # elif filter_tag: flask.abort(404)

    return render_template('blog.html', by_date=by_date, by_tag=by_tag,
                           filter_tag=None, recent=posts[:6])

@app.route('/blog/<name>/')
def blog_page(name):
    post = flatpages.get_or_404(name)
    post.meta['tag_list'] = post.meta.get('tags', '').split(', ')
    return render_template(url_for('static', filename='post.html'), post=post)

@app.route('/feed.xml')
def blog_rss():
    posts = [p for p in flatpages]
    posts.sort(key=operator.itemgetter('date'), reverse=True)
    for post in posts:
        post.meta['pub_date'] = post.meta['date'].strftime(
            '%a, %d %b %Y 12:%M:%S GMT')

        post.meta['description'] = post.meta.get('description', post.body)

    feed = render_template('feed.xml', posts=posts[:10])
    response = make_response(feed)
    response.headers['Content-Type'] = 'application/xml'
    return response

@app.route('/hexclock')
def hexclock():
    return render_template('hexclock.html')

@app.route('/ping')
def ping():
    return 'ok'

@app.route('/projects')
def projects():
    return render_template('projects.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0')