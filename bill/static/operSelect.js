dojo.provide('whs.operSelect');

//dojo.require('dojox.data.QueryReadStore');
//dojo.require('dojox.grid.DataGrid');
dojo.require('whs.oper');

dojo.declare('whs.operSelect', [dijit._Widget,dijit._Templated], {
    name:'',
    store:0,
    baseClass: 'operSelect',
    templateString: dojo.cache('whs', 'template/operSelect.html'),
    widgetsInTemplate:true,
    postCreate:function() {
        var tableNode = this.containerNode;
        var inputNode = this.inputNode;
        var name = this.name;

        var amount = this.amountNode;
        var tara = this.taraNode;

        dojo.query('option', this.containerNode).forEach(function(node, i) {
            var attr = dojo.attr
            var tr = new whs.oper_tr({
                value:attr(node,'value'),
                brick:attr(node,'brick'),
                brick_value:attr(node,'brick_value'),
                brick_css:attr(node,'brick_css'),
                amount:attr(node,'amount'),
                tara:attr(node,'tara'),
                i:attr(node,'info'),
                url:attr(node,'url')
            });
            tara.innerHTML = parseInt(tara.innerHTML) + parseInt(attr(node,'tara'));
            amount.innerHTML = parseInt(amount.innerHTML) + parseInt(attr(node,'amount'));


            dojo.place(tr.domNode,tableNode)
            dojo.place(tr.inputNode,inputNode)
            dojo.destroy(node);
        });
        url = '/'+name.slice(0,-1)+'/?bill='+document.location.href.split('bill')[1].split('/')[1];
        dojo.create('a',{href:url,innerHTML:'Добавить'},this.menuNode) ;

    },
    _setUrlAttr:function(name){
        console.log(name,'url');
        return '/'+name.slice(0,-1)+'/';
    },
    _getValueAttr:function(){
        var val = []
        dojo.query('option',this.inputNode).forEach(function(node,i){
            val.push(dojo.attr(node,'value'));
        });
        return val;
    }
});