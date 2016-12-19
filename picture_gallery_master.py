# picture_gallery_master.py
# -*- coding: utf-8 -*-

from openerp import models, fields, api, tools
from datetime import datetime
from StringIO import StringIO
import random
import PIL

# Table galleries
class galleries(models.Model):
    _name = 'picture_gallery.galleries'
    _descrition = 'Picture Galleries'
    
    name = fields.Char('Description', required=True)
    date = fields.Date('Gallery Date', required=True)
    description = fields.Text('Description')
    photographer = fields.Char('Photographer')
    picture_ids = fields.One2many('picture_gallery.pictures', 'gallery_id', 'Gallery ID')
    picture_number = fields.Integer('Number of pictures', compute='_get_picture_number', store=True, readonly=True)
    
    @api.one
    @api.depends('picture_ids')
    def _get_picture_number(self):
        self.picture_number = len(self.picture_ids)

# Table pictures
class pictures(models.Model):
    _name = 'picture_gallery.pictures'
    _descrition = 'Pictures'
    
    gallery_id = fields.Many2one('picture_gallery.galleries',ondelete='cascade',string='Gallery ID')
    name = fields.Char('Filename')
    image = fields.Binary('Image')
    image_big = fields.Binary('Image Big', compute='_compute_image_picture', store=True)
    image_medium = fields.Binary('Image Medium', compute='_compute_image_picture', store=True)
    image_small = fields.Binary('Image Small', compute='_compute_image_picture', store=True)
    image_alt = fields.Char('Image Label')
    size = fields.Integer('Size', compute='_compute_image_details', store=True, readonly=True)
    image_make = fields.Char('Manufacturer of the recording equipment', compute='_compute_image_details', store=True, readonly=True)
    image_model = fields.Char('Model name or model number of the equipment', compute='_compute_image_details', store=True, readonly=True)
    image_resolution = fields.Char('Resolution', compute='_compute_image_details', store=True, readonly=True)
    visits = fields.Integer('No of Views', readonly=True)
    ranking = fields.Float('Ranking', compute='_compute_ranking', store=True, readonly=True)
    
    @api.one
    @api.depends('image')
    def _compute_image_picture(self):
        image_content = self.image
        
        # Image Big
        self.image_big = tools.image_resize_image_big(image_content)
        
        # Image Medium
        self.image_medium = tools.image_resize_image_medium(image_content)
        
        # Image Small
        self.image_small = tools.image_resize_image_small(image_content)
    
        del image_content
    
    @api.one
    @api.depends('image')
    def _compute_image_details(self):
        if self.image:
            image_content = self.image.decode('base64')
            
            # File size
            self.size = len(image_content)
            
            # EXIF tags can get with the numeric code.
            # A list of this codes can be found at exiv2.org/tags.html
            try:
                image = PIL.Image.open(StringIO(image_content))
                exif_tags = image._getexif()
            
                # Image make from EXIF tag 0x010f
                self.image_make = exif_tags.get(0x010f)
            
                # Image model from EXIF tag 0x0110
                self.image_model = exif_tags.get(0x0110)
            except:
                pass
        
            # Image resolution
            width, height = image.size
            self.image_resolution = str(width) + ' x ' + str(height)

            del image_content
            del image
    
    @api.one
    @api.depends('visits')
    def _compute_ranking(self):
        age = datetime.now() - datetime.strptime(self.create_date, tools.DEFAULT_SERVER_DATETIME_FORMAT)
        self.ranking = self.visits * (0.5+random.random()) / max(3, age.days)


