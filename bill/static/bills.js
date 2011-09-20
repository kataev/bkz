dojo.require('dijit.form.Form');
dojo.require("dojox.grid.TreeGrid");
dojo.require("dojox.grid.DataGrid");
dojo.require("dojo.data.ItemFileReadStore");
dojo.require("dijit.tree.ForestStoreModel");
dojo.require("dijit.Tree");

dojo.addOnLoad(function() {
    dijit.byId('BillTree').onStyleRow = function(row) {
        var item = this.getItem(row.index);
        if (item) {
            row.customClasses += BillStore.getValue(item, 'css', null);
        }
    }
    dijit.byId('BillTree').onCellContextMenu = function(e){
        console.log('ololo')
    };
});
//
//dojo.addOnLoad(function(){
//        if (BillModel) {
//        BillModel.mayHaveChildren = function(item) {
//            if (item.children) return item.children.length;
//        };
//    }
//});

function Formatter(value, rowIdx, cell, sing, plur) {
    if (value) return value;
    else return '';
}