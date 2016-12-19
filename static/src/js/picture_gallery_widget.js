openerp.picture_gallery = function (instance,local)
{   
    local.upload_pictures = instance.web.form.FormWidget.extend({
        events: {
            "click .oe_picture_gallery": "load_input",
        },
        start: function() {
            var sup = this._super();
            return sup;
        },
        load_input: function(){
            var self = this;
            if (!this.view.datarecord.id){
                $(".oe_form_button_save").click();
                var rec_id = false;
                var rec_id = this.view.datarecord.id;
                if (!rec_id){
                    setTimeout(function(){ self.load_input(); }, 500);
                    return;
                }
            } else {
                var rec_id = this.view.datarecord.id;
            }
            if ( $("#picture_upload").length == 0 ){
                var input = "<input type='file' id='picture_upload' style='display:none;' multiple/>";
                this.$el.append(input);
            }
            $("#picture_upload").on('change',function(){ self.upload_files() });
            $("#picture_upload").click();
        },
        upload_files: function(){
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
                            });
                        }
                    });
                }
            }
        },
        upload_file: function(file,index){
            var self = this;
            return new Promise(function(resolve,reject){
                var reader = new FileReader();
                var data = {};
                reader.addEventListener("loadend", function(){
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
