dojo.require('dijit.form.Form');
dojo.require("dojox.grid.TreeGrid");
dojo.require("dojo.data.ItemFileReadStore");
dojo.require("dijit.tree.ForestStoreModel");
dojo.require("dijit.Tree");

dojo.addOnLoad(function() {
    BillModel.mayHaveChildren = function(item) {
        if (item.children) return item.children.length;
    };
    dijit.byId('BillTree').onStyleRow = function(row) {
        var item = dijit.byId('BillTree').getItem(row.index);
        if (item) {
            row.customClasses += BillStore.getValue(item, 'css', null);
        }
    }
});
function Formatter(value, rowIdx, cell, sing, plur) {
    if (value) return value;
    else return '';
}