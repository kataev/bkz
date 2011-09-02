dojo.provide('whs.operSelect');

dojo.require('dojox.data.QueryReadStore');
dojo.require('dojox.grid.DataGrid');
dojo.require('whs.oper');

dojo.declare('whs.operSelect', [dijit._Widget,dijit._Templated], {
    name:'',
    baseClass: 'operSelect',
    templateString: dojo.cache('whs', 'template/operSelect.html'),
    widgetsInTemplate:true,
    store:0,
    postCreate:function() {
        var tableNode = this.containerNode;
        var inputNode = this.inputNode;
        dojo.query('option', this.containerNode).forEach(function(node, i) {
            console.log(node);
            var attr = dojo.attr
            var tr = new whs.oper_tr({
                value:attr(node,'value'),
                brick:attr(node,'brick'),
                brick_css:attr(node,'brick_css'),
                amount:attr(node,'amount')
            })

            dojo.place(tr.domNode,tableNode)
            dojo.place(tr.inputNode,inputNode)

            dojo.destroy(node);
        });
    },
    _getValueAttr:function(){
        var val = []
        dojo.query('option',this.inputNode).forEach(function(node,i){
            val.push(dojo.attr(node,'value'));
        });
        return val;
    }

});