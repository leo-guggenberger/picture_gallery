# picture_gallery_controller.py
# -*- coding: utf-8 -*-

import datetime
import werkzeug

from openerp import tools
from openerp.addons.web import http
from openerp.addons.web.http import request
from openerp.addons.website.models.website import slug, unslug
from openerp.osv.orm import browse_record

class QueryURL(object):
    def __init__(self, path='', path_args=None, **args):
        self.path = path
        self.args = args
        self.path_args = set(path_args or [])
    
    def __call__(self, path=None, path_args=None, **kw):
        path = path or self.path
        for k, v in self.args.items():
            kw.setdefault(k, v)
        path_args = set(path_args or []).union(self.path_args)
        paths, fragments = [], []
        for key, value in kw.items():
            if value and key in path_args:
                if isinstance(value, browse_record):
                    paths.append((key, slug(value)))
                else:
                    paths.append((key, value))
            elif value:
                if isinstance(value, list) or isinstance(value, set):
                    fragments.append(werkzeug.url_encode([(key, item) for item in value]))
                else:
                    fragments.append(werkzeug.url_encode([(key, value)]))
        for key, value in paths:
            path += '/' + key + '/%s' % value
        if fragments:
            path += '?' + '&'.join(fragments)
        return path

class PictureGallery(http.Controller):
    _galleries_per_page = 20
    
    def nav_list(self):
        galleries_obj = request.registry['picture_gallery.galleries']
        groups = galleries_obj.read_group(
            request.cr, request.uid, [], ['name', 'date'],
            groupby="date", orderby="date desc", context=request.context)
        for group in groups:
            begin_date = datetime.datetime.strptime(group['__domain'][0][2], tools.DEFAULT_SERVER_DATE_FORMAT).date()
            end_date = datetime.datetime.strptime(group['__domain'][1][2], tools.DEFAULT_SERVER_DATE_FORMAT).date()
            group['date_begin'] = '%s' % datetime.date.strftime(begin_date, tools.DEFAULT_SERVER_DATE_FORMAT)
            group['date_end'] = '%s' % datetime.date.strftime(end_date, tools.DEFAULT_SERVER_DATE_FORMAT)
        return groups
    
    @http.route([
        '/gallery',
        '/gallery/page/<int:page>',
    ], type='http', auth="public", website=True)
    def galleries(self, page=1, **opt):
        """ Prepare all values to display the gallery.
            :return dict values: values for the templates, containing
            - 'gallery': browse of the current gallery
            - 'galleries': all picture galleries
            - 'pager': pager of posts
            - 'nav_list': a dict [year][month] for archives navigation
            - 'date': date_begin optional parameter, used in archives navigation
            - 'gallery_url': help object to create URLs
            """
        date_begin, date_end = opt.get('date_begin'), opt.get('date_end')
        
        cr, uid, context = request.cr, request.uid, request.context
        domain = []
        if date_begin and date_end:
            domain += [("date", ">=", date_begin), ("date", "<=", date_end)]
        
        galleries_obj = request.registry['picture_gallery.galleries']
        total = galleries_obj.search(cr, uid, domain, count=True, context=context)
        pager = request.website.pager(
            url='/gallery',
            total=total,
            page=page,
            step=self._galleries_per_page,
        )
        
        galleries_ids = galleries_obj.search(cr, uid, domain, order="date desc", offset=(page-1)*self._galleries_per_page, limit=self._galleries_per_page, context=context)
        galleries = galleries_obj.browse(cr, uid, galleries_ids, context=context)
        gallery_url = QueryURL('', [])
        
        values = {
            'galleries': galleries,
            'pager': pager,
            'nav_list': self.nav_list(),
            'date': date_begin,
            'gallery_url': gallery_url,
        }
        response = request.website.render("website.galleries", values)
        return response

    @http.route([
        '''/gallery/post/<model("picture_gallery.galleries"):gallery_post>''',
    ], type='http', auth="public", website=True)
    def galleries_post(self, gallery_post):
        cr, uid, context = request.cr, request.uid, request.context
        picture_obj = request.registry['picture_gallery.pictures']
        picture_ids = picture_obj.search(cr, uid, [('gallery_id', '=', gallery_post.id)], order="name asc", context=context)
        pictures = picture_obj.browse(cr, uid, picture_ids, context=context)
        
        values = {
            'gallery_post': gallery_post,
            'pictures': pictures,
        }
        response = request.website.render("website.gallery_post", values)
        return response