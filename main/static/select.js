dojo.provide("whs.select");


//dojo.require('dijit.form._FormWidget');
dojo.require('dijit._Widget');
dojo.require('whs.brick');
dojo.require('dijit._Templated');
//dojo.require("dojo.store.Memory");
dojo.require("dijit.Dialog");

dojo.declare("whs.select", [dijit._Widget,dijit._Templated], {
            name:'',
            baseClass: 'selectBrick',
            templateString: dojo.cache('whs', 'select.html'),
            widgetsInTemplate:true,
            label:'Щелкните для выбора кирпича',
            value:0,
            postCreate:function() {
                this.dialog = dijit.byId(this.id+'_dialog');
                var dialog = this.dialog;

                dojo.connect(this.labelNode, 'onclick', function(e) {
                    dialog.show() //TODO: get relative widget insance
                });
//        dojo.query('option',this.containerNode).connect('onclick',function(e){console.log(e)})
//        console.log(dojo.query('*',this.containerNode));
            },
            _setLabelAttr:function(val) {
                labelNode = this.labelNode;
                setValue = dojo.hitch(this, '_setValueAttr');
                dojo.query('[selected]', this.conteinerNode).forEach(function(node) {
                var q = dojo.query('.nameNode', node);
//                    console.log(node,q);
                            if (q[0]) {
                                    labelNode.innerHTML = q[0].innerHTML;
                            } else {
                                    labelNode.innerHTML = node.innerHTML;
                            }//TODO: передалть, чтобы отображался виджет whs.brick
                    setValue(dojo.attr(node, 'value'));
                });
            },
            _setValueAttr:function(val) {
                this.value = val;
//                this._setLabelAttr('');
            },
            _getValueAttr:function() {
                var v = 0;
                dojo.query('[selected]', this.conteinerNode).forEach(function(node) {
//                    console.log(node);
                    v = dojo.attr(node, 'value');
                });
//                console.log('get val',v);
                return v;
            },
            startup:function() {
                var dialog = this.dialog;
                var setLabel = dojo.hitch(this, '_setLabelAttr')
                dojo.query('tr', this.containerNode).connect('onclick', function(e) {
//                    dojo.query('td:first',e.target).forEach(function(node){
//                        node.innerHTML
//                    });
                    setLabel();
                    dialog.hide();

                })
            }
        });