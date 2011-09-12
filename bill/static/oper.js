dojo.provide('whs.oper');

//dojo.require('dijit.form.MultiSelect')
dojo.require('whs.brick')

dojo.require('dijit._Widget');
dojo.require('dijit._Templated');
//dojo.require('dijit.Dialog')

dojo.declare('whs.oper', [dijit._Widget, dijit._Templated], {
    name:'',selected:false,value:0,
    title:'',amount:0,tara:0,i:'',
    brick_css:'',brick:'',brick_value:0,
    baseClass: 'oper',
    templateString: dojo.cache('whs', 'template/oper.html'),
    widgetsInTemplate:true,
    _setInfoAttr: function(val) {
        this.info = this.srcNodeRef.innerHTML;
    },
    postCreate:function() {
        var url = '/' + this.name + '/' + this.value + '/' + 'delete/';
        widget = this;
        dojo.connect(this.deleteNode, 'onclick', function(evt) {
            if (confirm('Удалить операцию?')) {
                dojo.xhrPost({url:url,content:{confirm:true},handleAs:'json'}).then(function(data) {
                    if (data.success) {
                        widget.destroy()
                    }
                });
            }
        });
    }
});


dojo.provide('whs.oper.tr');

dojo.declare('whs.oper.tr', whs.oper, {
    templateString: dojo.cache('whs', 'template/oper_tr.html')
});