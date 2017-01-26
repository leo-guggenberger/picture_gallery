# __openerp__.py
# -*- coding: utf-8 -*-
{
    'name': "Website Picture Gallery",
    'version': '8.03',
    'description': """
Website Picture Gallery
=============
        
Picture Gallery administration with following features:
-------------------------------------
* Multiple image upload
* Storage of images in database
* Automatical cull of EXIF-data (such as camera manufacturer, camera model, etc.)
* Counter how often a picture was shown
* Memory-optimized upload of the images - unused memory is automatically released again
* Language support: English, German
* Odoo version support: v8

Picture Gallery presentation on website with following features:
-------------------------------------
* Display / hide archives in the right block of the image gallery overview
* Show pictures as slider on the website
  - Slider Fotorama 4.6.4 (http://fotorama.io) with MIT license (http://fotorama.io/license/) is used
* Option to show slider in fullscreen mode
        """,
    'author': 'Leo',
    'website': 'http://www.leo-guggenberger.at',
    'category': 'Generic Modules/Others',
    'price': 49.90,
    'currency': 'EUR',
    'images': ['static/description/main_screenshot.png'],
    'depends': ['website', 'document'],
    'data': ['data/garbage_collector.xml',
             'data/javascript_import.xml',
             'views/picture_gallery.xml',
             'views/picture_gallery_templates.xml',
             'views/picture_gallery_views.xml',
             'views/picture_gallery_report.xml',
             'security/security.xml',
             'security/ir.model.access.csv'],
             'demo': [],
             'qweb': [],
             'js': ['static/src/js/picture_gallery_widget.js'],
             'installable': True,
             'auto_install': False,
}
