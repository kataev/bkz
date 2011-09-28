dojo.require('dijit.form.Form');
dojo.require("dojox.grid.DataGrid");
dojo.require("dojo.data.ItemFileReadStore");
dojo.require("dijit.Menu");
dojo.require("dijit.MenuItem");
dojo.require("dojo.date.locale");

function date_formatter(date){
    return dojo.date.locale.format(new Date(date),{selector:'date',datePattern:'MMM d, yyyy'});
}

dojo.addOnLoad(function() {
    dijit.byId('BillsTable').onStyleRow = function(row) {
        var item = this.getItem(row.index);
        if (item) row.customClasses += BillStore.getValue(item, 'css', null);
    }
});
dojo.addOnLoad(function(){
    dijit.byId('BillsTable').onCellContextMenu = function(e){
        var item = e.grid.getItem(e.rowIndex);
        if (item){
            var menu = new dijit.Menu({targetNodeIds: [e.cellNode]});
            menu.addChild(new dijit.MenuItem({
                label:'Открыть накладную',
                onClick: function(event){window.location = '/bill/'+whs.id_to_dict(item.id[0]).id+'/'}
            }));
            menu.addChild(new dijit.MenuItem({
                label:'Открыть контрагента',
                onClick: function(event){window.location = '/agent/'+item.agent_id[0]+'/'}
            }));
            menu.startup();
            menu._openMyself(e);
            dojo.connect(menu,'onClose',function(){menu.uninitialize()})
        }
    };
});

function Formatter(value, rowIdx, cell, sing, plur) {
    if (value) return value;
    else return '';
}