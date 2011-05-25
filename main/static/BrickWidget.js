dojo.provide("whs.BrickWidget");


dojo.require("dijit._Widget");
dojo.require("dijit._Templated");


dojo.declare("whs.BrickWidget", [dijit._Widget, dijit._Templated], {
            label:'Loading...',
            BrickId:'',
            store:null,
//    avatar: dojo.moduleUrl("whs.BrickWidget", "images/defaultAvatar.png"),
            templateString:
                    dojo.cache("whs.BrickWidget", "templates/BrickWidget.html"),
            baseClass: "BrickWidget",
            constructor:function(attr) {
                this.BrickId = attr.BrickId;

            },
            _setBrickIdAttr:function(id) {
                if (id != '') {
                    this._set('BrickId', id);

                }
            },
            _setLabelAttr:function(label) {
                if (this.BrickId != '') {
                    this.label = label;
                    this.labelNode.innerHTML = label;
                }
            },

            postCreate: function() {
                var domNode = this.domNode;
                this.inherited(arguments);
                var set = dojo.hitch(this,'_setLabelAttr');
                dojo.when(brick.get(this.BrickId), function(data){
                    var b = data[0].fields;
                    var label='';
                    if (b.weight == 2) {
                        label='КР 2 '
                        label+= 'НФ/' + b.mark !=9000 ? b.mark : '';
                        label+=' ' + b.defect + ' ' + b.refuse + ' ' + b.features + ' ' + b.color_type;
                    }
                    else {
                        if (b.brick_class!=5){
                            label = 'К';
                            label+= b.weight=='1.4' ? 'У' : 'О';
                            label+=b.view+'ПУ';
                            label+=' '+ b.weight + ' ';
                            label+= b.mark==9000 ? 'НФ/1,4' : 'НФ/' + b.mark + '/1,4';
                            label+=' ' + b.defect + ' ' + b.refuse + ' ' + b.features + ' ' + b.color_type;
                        }
                        else {
                            label = 'КЕ ' + b.weight;
                            label+=  b.weight=='Л ' ? 'УЛ' : ' ';
                            label+= b.mark==9000 ? 'НФ/1,4/50' : 'НФ/' + b.mark + '/1,4';
                            label+=' ' + b.defect + ' ' + b.refuse + ' ' + b.features + ' ' + b.color_type;
                        }
                    }
                    set(label);
                });
            }
        })
