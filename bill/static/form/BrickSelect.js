dojo.provide("whs.BrickSelect");

dojo.require('dijit._Widget');
dojo.require('whs.brick');
dojo.require('dijit._Templated');
dojo.require('dijit.Dialog');

dojo.provide('whs.Dialog');
dojo.declare('whs.Dialog',dijit.Dialog,{
    templateString: dojo.cache('whs', 'template/Dialog.html')
        });

dojo.declare("whs.BrickSelect", [dijit._Widget,dijit._Templated], {
            name:'',
            baseClass: 'BrickSelect',
            templateString: dojo.cache('whs', 'template/brickSelect.html'),
            widgetsInTemplate:true, label:'Щелкните для выбора кирпича',value:0,
            postCreate:function() {
                this.dialog = dijit.byId(this.id+'_dialog');
                var dialog = this.dialog;
                dojo.connect(this.labelNode, 'onclick', function(e) {
                    dialog.show()
                });
            },
            _setLabelAttr:function(val) {
                var c = this.containerNode;
                var labelNode = this.labelNode;
                var setValue = dojo.hitch(this, '_setValueAttr');
                dojo.query('[selected]',c).forEach(function(node) {
                var q = dojo.query('.nameNode', node);
                    if (q[0]) labelNode.innerHTML = q[0].innerHTML;
                    else labelNode.innerHTML = node.innerHTML;
                    setValue(dojo.attr(node, 'value'));
                    dojo.attr(labelNode,'class','dijitTextBox brick '+dojo.attr(node,'class'));
                });
            },
            _setValueAttr:function(val) {
                this.value = val;
                dojo.attr(this.inputNode,'value',val);
            },
            _getValueAttr:function() {
                var v = 0;
                dojo.query('[selected]', this.conteinerNode).forEach(function(node) {
                    v = dojo.attr(node, 'value');
                });
                return v;
            },
            startup:function() {
                var dialog = this.dialog;
                var setLabel = dojo.hitch(this, '_setLabelAttr');
                dojo.query('tr', this.containerNode).connect('onclick', function(e) {
                    setLabel();
                    dialog.hide();
                })
            }
        });