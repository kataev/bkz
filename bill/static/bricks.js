dojo.require("dojox.grid.DataGrid");
dojo.require("dojo.data.ItemFileReadStore");
dojo.require("whs.CheckBox");
dojo.require("dijit.form.Form");

var BrickTotalLayout = [
    { field:'label', width:'280px',name:'Кирпич'},
    { field:'begin', width:'60px', name:'Начало'},
    { field:'t_to', width:'60px',name:'Акт в'},
    { field:'t_from', width:'60px',name:'Акт из'},
    { field:'sold', width:'60px',name:'Расход'},
    { field:'total', width:'auto',name:'Остаток'}
]

var testdata = {items: [
    {
        label: 'Итого:',
        begin: 0,
        t_to: 0,
        t_from: 0,
        sold:0,
        total: 0
    }
]};

dojo.addOnLoad(function() {
    var table = dijit.byId('Brick');
    dojo.connect(table, "_onFetchComplete", function(e) {
        dojo.forEach(['begin','t_to','t_from','sold','total'], function(i) {
            testdata.items[0][i][0] = 0;
        });
        BrickStore.fetch({query:dijit.byId('Brick').query,onItem:function(item) {
            dojo.forEach(['begin','t_to','t_from','sold','total'], function(i) {
                testdata.items[0][i][0] += parseInt(item[i]);
            });
        }});
        dijit.byId('BricksTotal').render();
//        console.log(testdata.items[0])
    });
    dijit.byId('Brick_info').onStyleRow = function(row) {
        var item = dijit.byId('Brick_info').getItem(row.index);
        if (item) {
            row.customClasses += ' ' + whs.id_to_dict(brick_info.getValue(item, 'id', null)).name;
        }
    };

    dijit.byId('Brick').onStyleRow = function(row) {
        var item = table.getItem(row.index);
        if (item) {
            row.customClasses += BrickStore.getValue(item, 'css', null);
        }
//            console.log(row.customClasses)
    }
    dijit.byId('Brick').onRowClick = function(e) {
        var item = table.getItem(e.rowIndex);
        brick_name.innerHTML = item.label;
        dojo.attr(brick_name, 'class', 'dijitContentPane dijitBorderContainer-child dijitBorderContainer-dijitContentPane dijitBorderContainerPane dijitAlignTop ' + item.css);
        brick_info.url = whs.id_to_url(item.id) + 'store/';
        brick_info.close();
        dijit.byId('Brick_info').render();
    }
});

