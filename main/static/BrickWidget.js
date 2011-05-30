dojo.provide("whs.BrickWidget");


dojo.require("dijit._Widget");
dojo.require("dijit._Templated");


dojo.declare("whs.BrickWidget", [dijit._Widget, dijit._Templated], {
            label:'Loading...',
            BrickId:null,
            weight:null,
            _loaded:false,
            templateString:
                    dojo.cache("whs.BrickWidget", "templates/BrickWidget.html"),
            baseClass: "BrickWidget",
            constructor:function(args) {
                var _setlabel = dojo.hitch(this,'_setLabelAttr');
//                var _loaded = dojo.hitch(this._loaded);
                this.BrickId=args.BrickId;
                dojo.when(brick.get(args.BrickId), function(data) {
                    var _loaded = true
                    console.log('loaded!',this._loaded);
                    _setlabel(data[0]);

                    
                    console.log(data[0].fields)

                },function(){})
            },
            _setBrickIdAttr:function(id) {
                this._set('BrickId', id);
            },
            _setLabelAttr:function(data) {
                    console.log('loaded?',this._loaded);
                if (this._loaded) {
                    console.log('id',this.BrickId);
                    b = data.fields;

                    var label = '';
//                    BrickClass(b.brick_class);
//                    BrickColor(b.color);
                    console.log('b.weight',b.weight);
                    if (b.weight == 2) {
                        label = 'КР 2 ';
                        label += b.mark != 9000 ? b.mark : '';
                        label += ' ' + b.defect + ' ' + b.refuse + ' ' + b.features + ' ' + b.color_type;
                    }
                    else {
                        
                        if (b.brick_class != 5) {
                            label = 'К';
                            label += b.weight == '1.4' ? 'У' : 'О';
                            label += b.view + 'ПУ';
                            label += ' ' + b.weight + ' ';
                            label += b.mark == 9000 ? '' : '' + b.mark + '/1,4';
                            label += ' ' + b.defect + ' ' + b.refuse + ' ' + b.features + ' ' + b.color_type;
                        }
                        else {
                            label = 'КЕ ' + b.weight;
                            label += b.weight == 'Л ' ? 'УЛ' : ' ';
                            label += b.mark == 9000 ? '' : 'НФ/' + b.mark + '/1,4';
                            label += ' ' + b.defect + ' ' + b.refuse + ' ' + b.features + ' ' + b.color_type;
                        }
                    }
                    label=dojo.trim(label);
                    this.label = label;
                    this.labelNode.innerHTML = label;
                    console.log(label);
                    this.domNode.title = label;
                    return label;
                } else {
                    return this.label;
                }
            },

            _setBrickClassAttr:function(attr) {
//                dojo.addClass(this.labelNode,BrickClass[attr]);
            },
            _setBrickColorAttr:function(attr) {
//                dojo.addClass(this.labelNode,BrickColor[attr]);
            },
            postCreate: function() {
//                var domNode = this.domNode;
//                var id = this.BrickId;
                this.inherited(arguments);
//                var set = dojo.hitch(this, '_setLabelAttr');
//                var class = dojo.hitch(this, '_setBrickClassAttr');
//                var color = dojo.hitch(this, '_setBrickColorAttr');

            }
        });
