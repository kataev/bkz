dojo.provide("whs.select.Brick");

dojo.require('dijit.form._FormWidget')
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
                if (this.store.get(value)) {
                    console.log(this.store.get(value))
                    this._setLabelAttr(this.store.get(value).title);
                }

            },
            _getBrickAttr: function() {
                return this.store.get(this.value);
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

                dojo.query('option.brick', this.containerNode).forEach(function(node, i) {
                    var pk = parseInt(dojo.attr(node, 'value'));
                    var title = node.innerHTML;
                    store.put({id:pk,
                                title:title,
                                'class':dojo.attr(node, 'cl'),
                                mark:dojo.attr(node, 'mark'),
                                view:dojo.attr(node, 'vi'),
                                weight:dojo.attr(node, 'we'),
                                color:dojo.attr(node, 'color'),
                                total:dojo.attr(node, 'total'),
                                css:dojo.attr(node, 'class')
                            });
                    dojo.destroy(node);
                });
                var content = dojo.byId('bricksform');

//                this.brickform = new dijit.form.Form(null,content);

//                console.log(dijit.byId('bricksform'));

//                dojo.query('#bricksform select', this.containerNode).forEach(function(node, i) {
//                    console.log(node,content);
//                    var a= dojo.place(node,content)
//                    dojo.destroy(node);
//                    dojo.parser.parse(a);
//                });
//                dojo.place('bricksform', content)

                var table = dojo.create('table', null, content);
                dojo.attr(table, 'id', 'brickselect');
                store.query().forEach(function(el) {
                    var tr = dojo.create('tr', {'class':el['css']}, table);
                    dojo.attr(tr, 'pk', el['id']);
                    for (a in el) {
                        if (a != 'css') {
                            dojo.create('td', {innerHTML:el[a]}, tr);
                        }
                    }

                });
//
                var dialog = new dijit.Dialog({title:'Выбор кирпича','content':content,style:'width:600px;',draggable:false});
                dojo.query('tr', table).connect('onclick', function(e) {
                    console.log(e.target.parentElement);
                    var value = dojo.attr(e.target.parentElement, 'pk');
                    setValue(value);
                    dialog.hide();
                });
                dojo.connect(this.containerNode, 'onclick', function(e) {
                    dialog.show();
                });
                console.log('ok')

            }
        });