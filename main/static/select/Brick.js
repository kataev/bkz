dojo.provide("whs.select.Brick");

dojo.require('dijit.form._FormWidget')
//dojo.require("dijit._Templated");
dojo.require("dojo.store.Memory");
dojo.require("dijit.Dialog");

dojo.declare("whs.select.Brick", [dijit.form._FormValueWidget], {
            baseClass: 'selectBrick',
    className:'sb',
            templateString: dojo.cache("whs.select.Brick", "Brick.html"),
            store : new dojo.store.Memory({data:[]}),
            value:'',
            label:'Щелкните для выбора кирпича',
            name:'brick',


            _getValueAttr: function() {
                return this.value;
            },
            _setValueAttr: function(value) {
                this.value = value;
                dojo.attr(this.inputNode, 'value', value);
                if (this.store.get(value))
                {
                    console.log(this.store.get(value))
                    this._setLabelAttr(this.store.get(value).title);
                }

            },
            _getLabelAttr: function() {
                return this.label;
            },
            _setLabelAttr: function(value) {
                this.label = value;
                this.labelNode.innerHTML = value;
            },



            postCreate: function() {
//                var selectNode = this.selectNode;
                var store = this.store;
                var setValue = dojo.hitch(this, '_setValueAttr');
                var setLabel = dojo.hitch(this, '_setLabelAttr');
                dojo.query('option[selected]', this.containerNode).forEach(function(node, i) {
                    setValue(parseInt(dojo.attr(node, 'value')));
                    setLabel(node.innerHTML);
                });

//                dojo.query('div', this.containerNode).forEach(function(node, i) {
//                    console.log(node);
//                })
//                this.dojo.byId('BrickSelect')

                dojo.query('option', this.containerNode).forEach(function(node, i) {
                    var pk = parseInt(dojo.attr(node, 'value'));
                    var title = node.innerHTML;
                    store.put({id:pk,
                                title:title,
                                'class':dojo.attr(node, 'cl'),
                                mark:dojo.attr(node, 'mark'),
                                view:dojo.attr(node, 'vi'),
                                weight:dojo.attr(node, 'we'),
                                color:dojo.attr(node, 'color'),
                                total:dojo.attr(node, 'total')
                            });
                    dojo.destroy(node);
                });



                var table = dojo.create('table');
                store.query().forEach(function(el){
                    var tr = dojo.create('tr',null,table);
                    dojo.attr(tr,'pk',el['id']);
                    for (a in el){
                        dojo.create('td',{innerHTML:el[a]},tr);
                    }

                });
//
                var dialog = new dijit.Dialog({title:'Выбор кирпича','content':table,style:'width:600px;',draggable:false});
                dojo.query('tr',table).connect('onclick',function(e){
                    console.log(e.target.parentElement);
                    var value = dojo.attr(e.target.parentElement,'pk');

                    setValue(value);
                    dialog.hide();
                });
                dojo.connect(this.containerNode, 'onclick', function(e){
                    dialog.show();
                });


            }
        });
