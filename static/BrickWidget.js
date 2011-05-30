dojo.provide("whs.BrickWidget");


dojo.require("dijit._Widget");
dojo.require("dijit._Templated");


dojo.declare("whs.BrickWidget", [dijit._Widget, dijit._Templated], {
            label:'Loading...',
            BrickId:null,
//    avatar: dojo.moduleUrl("whs.BrickWidget", "images/defaultAvatar.png"),
            templateString:
                    dojo.cache("whs.BrickWidget", "templates/BrickWidget.html"),
            baseClass: "BrickWidget",
            constructor:function(id) {
                this.BrickId = id;
                console.log(id);

            },
            _setBrickIdAttr:function(id) {
                if (id != '') {
                    this._set('BrickId', id);

                }
            },
            _setLabelAttr:function(label) {
                if (this.BrickId) {
                    this.label = label;
                    this.labelNode.innerHTML = label;
                    this.domNode.title=label;
                }
            },

            _setBrickClassAttr:function(attr) {
                dojo.addClass(this.labelNode,BrickClass[attr]);
            },
            _setBrickColorAttr:function(attr) {
                dojo.addClass(this.labelNode,BrickColor[attr]);
            },

            postCreate: function() {
                var domNode = this.domNode;
                this.inherited(arguments);
                var set = dojo.hitch(this,'_setLabelAttr');
                var class = dojo.hitch(this,'_setBrickClassAttr');
                var color = dojo.hitch(this,'_setBrickColorAttr');
                console.log('as')
                return this.BrickId ? dojo.when(brick.get(this.BrickId), function(data){
                    var b = data[0].fields;
                    var label='';

                    class(b.brick_class);
                    color(b.color);

                    if (b.weight == 2) {
                        label='КР 2 '
                        label+= b.mark !=9000 ? b.mark : '';
                        label+=' ' + b.defect + ' ' + b.refuse + ' ' + b.features + ' ' + b.color_type;
                    }
                    else {
                        if (b.brick_class!=5){
                            label = 'К';
                            label+= b.weight=='1.4' ? 'У' : 'О';
                            label+=b.view+'ПУ';
                            label+=' '+ b.weight + ' ';
                            label+= b.mark==9000 ? '' : '' + b.mark + '/1,4';
                            label+=' ' + b.defect + ' ' + b.refuse + ' ' + b.features + ' ' + b.color_type;
                        }
                        else {
                            label = 'КЕ ' + b.weight;
                            label+=  b.weight=='Л ' ? 'УЛ' : ' ';
                            label+= b.mark==9000 ? '' : 'НФ/' + b.mark + '/1,4';
                            label+=' ' + b.defect + ' ' + b.refuse + ' ' + b.features + ' ' + b.color_type;
                        }
                    }
                    set(label);
                }) : undefined;
            }
        })
