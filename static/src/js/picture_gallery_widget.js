openerp.picture_gallery = function (instance,local)
{   
    var _t = instance.web._t,
    _lt = instance.web._lt;
    local.upload_pictures = instance.web.form.FormWidget.extend({
        events: {
            "click .oe_picture_gallery": "load_input",
        },
        start: function() {
            var sup = this._super();
            return sup;
        },
        load_input: function(){
            if (this.view.get('actual_mode') == 'view'){
                return;
            }
            var self = this;
            if (!this.view.datarecord.id){
                var e = new Event('save');
                this.view.on_button_save(e)
            } else {
                var rec_id = this.view.datarecord.id;
            }
            if ( $("#picture_upload").length == 0 ){
                var html = "<input type='file' id='picture_upload' style='display:none;' accept='image/*'  multiple/>";
                this.$el.append(html);
                $("#picture_upload").on('change',function(){ self.upload_files() });
            }
            $("#picture_upload").click();
        },
        upload_files: function(){
            if (this.view.get('actual_mode') == 'view'){
                $(".oe_form_button_edit").click();
            }
            instance.web.blockUI()
            var input = $("#picture_upload")[0];
            var self = this;
            if (input.files.length > 0){
                for (var i=0; i<input.files.length; i++){
                    self.upload_file(input.files[i],i)
                    .then(function(data){
                        if (data['index'] == input.files.length -1){
                            var pg = new instance.web.Model('picture_gallery.pictures')
                            pg.query(['picture_ids'])
                            .filter([['gallery_id','=', self.view.datarecord.id]])
                            .all()
                            .then(function(picture_ids){ 
                                var data = [];
                                for (var x=0; x<picture_ids.length; x++){
                                    data.push([4,picture_ids[x]['id'],false]);
                                }
                                self.view.fields.picture_ids.set_value(data);
                                instance.web.unblockUI()
                            });
                        }
                    })
                    .catch(function(error){
                         console.log("ERROR");
                         instance.web.unblockUI()
                         alert(_t(error));
                    })
                }
            }
        },
        upload_file: function(file,index){
            var self = this;
            return new Promise(function(resolve,reject){
                var reader = new FileReader();
                var data = {};
                reader.addEventListener("loadend", function(){
                    if (reader.result.split(',')[0].indexOf('image')==-1){
                        reject("One of the files you have selected is not an image");
                    }
                    data['gallery_id'] = self.view.datarecord.id;
                    data['name'] = file.name;
                    data['image'] = reader.result.split(',')[1];
                    $.ajax({
                            type: "POST",
                            url: '/web/dataset/call_kw',
                            dataType: 'json',
                            async: true,
                            data: JSON.stringify({'jsonrpc':'2.0',
                                                  'method':'call',
                                                  'params':{
                                                            'model':'picture_gallery.pictures',
                                                            'args':[data],
                                                            'context':{},
                                                            'kwargs':{},
                                                            'method':'create'
                                                            },
                                                  'id': 1}),
                            contentType: "application/json; charset=utf-8",
                            success: function(data){
                                if (data.hasOwnProperty('error')){
                                    reject(data.error.data.message);
                                }
                                data['index'] = index;
                                resolve(data);
                            },
                            failure: function(data){
                                reject(index);
                            }
                    });                    
                });
                reader.readAsDataURL(file);
            });
        },
    });

    instance.web.form.custom_widgets.add('upload_pictures', 'instance.picture_gallery.upload_pictures');

}
