dojo.provide("whs.select.Brick");

dojo.require('dijit.form._FormWidget');
dojo.require("dojo.store.Memory");
dojo.require("dijit.Dialog");


dojo.provide("whs.select.Brick");

dojo.require('dijit._Widget');
dojo.require('dijit._Templated');
dojo.require('dijit.Menu');


dojo.declare("whs.br", [dijit._Widget,dijit._Templated], {
    baseClass:'br',
    title:'',
    pk:0,
    templateString:'<span class="${baseClass} ${class}">${title}</span>',
    _setnameAttr : function(val){
        this.name = val;
        this.domNode.innerHTML = val;

    },
    postCreate:function(){
        var pk = this.pk
        pMenu = new dijit.Menu({
            targetNodeIds: [this.domNode]
        });
        pMenu.addChild(new dijit.MenuItem({
            label: "Показать накладные с этим кирпичем",
            iconClass: "dijitEditorIcon dijitEditorIconCut",
            onClick: function() {
                window.location='/bills/?brick='+pk;
            }
        }));
        pMenu.addChild(new dijit.MenuItem({
            label: "Создать продажу с этим кирпичем",
            iconClass: "dijitEditorIcon dijitEditorIconCut",
            onClick: function() {
                window.location='/form/sold/?brick='+pk;
            }
        }));
        pMenu.addChild(new dijit.MenuItem({
            label: "Создать перевод с этим кирпичем",
            iconClass: "dijitEditorIcon dijitEditorIconCut",
            onClick: function() {
                window.location='/form/transfer/?brick='+pk;
            }
        }));
    }
//    _setPkAttr : function(val){
//        console.log(val)
//        this.pk=val;
//    },
//    _getNameAttr : function(){
//        return this.Name;
//
//    }

        });



dojo.declare("whs.select.Brick", [dijit.form._FormValueWidget], {
            baseClass: 'selectBrick',
            className:'sb',
            templateString: dojo.cache("whs.select.Brick", "Brick.html"),
            store : new dojo.store.Memory({data:[]}),
            value:'',
            label:'Щелкните для выбора кирпича',
            name:'brick',
//            onChange: function(oldValue, newValue){
//
//            },

            _getValueAttr: function() {
                return this.value;
            },
            _setValueAttr: function(value) {
                this.onChange(this.value, parseInt(value));
                console.log('brick id',value);
                this.value = parseInt(value);
                dojo.attr(this.inputNode, 'value', this.value);
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

            reset : function() {
                this._setLabelAttr('Щелкните для выбора кирпича');
                this._setValueAttr('');
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
                console.log(this.containerNode);
                dojo.query('option', this.containerNode).forEach(function(node, i) {
                    var pk = parseInt(dojo.attr(node, 'value'));
                    var title = node.innerHTML;
                    store.put({id:pk,
                                title:title,
                                'brick_class':dojo.attr(node, 'cl'),
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

                var table = dojo.create('table', {id:'table',style:''}, content);
                dojo.attr(table, 'id', 'brickselect');

                var render = function () {
                    var query = {};
                    dojo.query('ul.filter').forEach(function(node, i) {
                        var key = dojo.attr(node, 'key');
                        var value = dojo.query('li.selected', node)[0]
                        if (value != undefined) {
                            console.log(key, dojo.attr(value, 'val'), value);
                            query[key] = dojo.attr(value, 'val');
                        }
                    });
                    console.log(query);
                    dojo.empty(table);
                    store.query(query).forEach(function(el) {
                        var tr = dojo.create('tr', {'class':el['css']}, table);//
                        dojo.attr(tr, 'pk', el['id']);
                        for (a in el) {
                            if (a == 'title' || a == 'total') {
                                var td = dojo.create('td', {innerHTML:el[a]}, tr);
                                if (a == 'title') {
                                    dojo.addClass(td, 'title');
                                }
                            }
                        }
                    });
                    dojo.query('tr', table).connect('onclick', function(e) {
                        console.log(e.target.parentElement);
                        var value = dojo.attr(e.target.parentElement, 'pk');
                        setValue(value);
                        dialog.hide();
                    });
                }
                render();

//
                var dialog = new dijit.Dialog({title:'Выбор кирпича',style:{weight:'600px'},'content':content,draggable:false});

                dojo.connect(this.containerNode, 'onclick', function(e) {
                    dialog.show();
                });

                dojo.query('ul.filter li').connect('onclick', function(e) {

                    dojo.query('li', e.target.parentNode).removeClass('selected');
                    if (!dojo.hasClass(e.target, 'None')) {
                        dojo.toggleClass(e.target, 'selected');
                    }

                    render();
                });

                console.log('ok')

            }
        });