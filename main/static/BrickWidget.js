dojo.provide("whs.BrickWidget");


dojo.require("dijit._Widget");
dojo.require("dijit._Templated");


dojo.declare("whs.BrickWidget", [dijit._Widget, dijit._Templated], {
            label:'Loading...',
            BrickId:null,
            IsLoaded : false,
            templateString:
                    dojo.cache("whs.BrickWidget", "templates/BrickWidget.html"),
            baseClass: "BrickWidget",

            loaded:function(label) {
                this.labelNode.innerHTML = label;
                this.domNode.title = label;
                this.label = label;
            },

            constructor:function(args) {
                this.BrickId = args.BrickId;
            },
//            _setBrickIdAttr:function(id) {
//                this._set('BrickId', id);
//            },
            _setLabelAttr:function(data) {
//                var _setlabel = dojo.hitch(this, '_setLabelAttr');
                var _loaded = dojo.hitch(this, 'loaded');

                dojo.when(brick.get(this.BrickId), function(data) {
                    var b = data[0].fields;
                    var label = '';
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
//                    console.log(this.labelNode);
                    label = dojo.trim(label.replace('  ', ' '));
//                    this.label = label;
                    _loaded(label);
//                    return label;


                }, function() {
                });


            },

            _setBrickClassAttr:function(attr) {
                dojo.addClass(this.labelNode,BrickClass[attr]);
            },
            _setBrickColorAttr:function(attr) {
                dojo.addClass(this.labelNode,BrickColor[attr]);
            },
            postCreate: function() {
                var domNode= this.domNode;
                var BrickId = this.BrickId;
                var pMenu = new dijit.Menu({
                            targetNodeIds: [domNode]
                        });

                pMenu.addChild(new dijit.MenuItem({
                            label: "Операции с этим кирпичем",
                            onClick: function() {
                                alert('not work yet');
                            }
                        }));
                pMenu.addChild(new dijit.MenuItem({
                            label: "Изменить в новой вкладке",
                            iconClass: "dijitEditorIcon dijitEditorIconCut",
                            onClick: function() {
                                new whs.Form('bricks',BrickId);
                            }
                        }));

//                pMenu.addChild(new dijit.MenuSeparator());

                pMenu.startup();

            }
        });
