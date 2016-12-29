# __openerp__.py
# -*- coding: utf-8 -*-
{
    'name': "Bildergalerie",
    'version': '1.03',
    'description': """
Bildergalerie
=============
        
Bildergalerie mit folgenden Features:
-------------------------------------
* Gleichzeitiger Upload von mehreren Bildern
* Ablage der Bilder in Datenbank
* EXIF-Daten (wie Kamerahersteller, Kameramodell usw.) werden ausgelesen
* Archive im rechten Block der Bildergalerieübersicht ein-/ausblendbar
* Anzeige der Bilder im Slider - als Slider wird Fotorama 4.6.4 (http://fotorama.io) unter MIT Lizent (http://fotorama.io/license/) verwendet
* Counter wie oft ein Bild angezeigt wurde
* Option Fullscreenmodus im Sliders
* Speicheroptimierter Upload der Bilder - nicht mehr benötigter RAM wird automatisch wieder freigegeben
* Verfügbar in Englisch und Deutscher Sprache
        """,
    'author': 'Leo',
    'website': 'http://www.leo-guggenberger.at',
    'category': 'Generic Modules/Others',
    'price': 49.90,
    'currency': 'EUR',
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
