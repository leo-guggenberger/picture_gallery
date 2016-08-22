openerp.picture_gallery = function (instance)
{
    instance.web.form.widgets.add('upload_pictures', 'instance.upload_pictures.upload_pictures');
    instance.upload_pictures.upload_pictures = instance.web.form.FieldBinaryImage.extend({
        template : "upload_pictures",
        init: function (view, code) {
            this._super(view, code);
            console.log('loading...');
        }
    });
}