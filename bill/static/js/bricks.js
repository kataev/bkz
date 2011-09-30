dojo.require("dojox.grid.DataGrid");
dojo.require("dojo.data.ItemFileReadStore");
dojo.require("whs.form.Form");
dojo.require("dojo.date.locale");

dojo.require("whs.form.CheckBox");

dojo.provide('whs.grid.date_formatter');
whs.date_formatter = function (date){
    return dojo.date.locale.format(new Date(date),{selector:'date',datePattern:'MMM d, yyyy'});
}

var BrickLayout = [
    { field:'label', width:'270px',name:'Кирпич',cellClasses:'label'},
    { field:'begin', width:'60px', name:'Начало',cellClasses:'begin'},
    { field:'plus', width:'60px', name:'Приход',cellClasses:'plus'},
    { field:'t_to', width:'60px',name:'Акт в',cellClasses:'t_to'},
    { field:'t_from', width:'60px',name:'Акт из',cellClasses:'t_from'},
    { field:'sold', width:'60px',name:'Расход',cellClasses:'sold'},
    { field:'total', width:'auto',name:'Остаток',cellClasses:'total'}
]

var BrickInfoLayout = BrickLayout.slice(1,-1);
BrickInfoLayout[0]={ field:'date',
    width:'auto',name:'Дата',
    cellClasses:'date',formatter:whs.date_formatter}

var testdata = {items: [
    {
        label: 'Итого:',
        begin: 0,
        plus: 0,
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
        var count=0
        BrickStore.fetch({query:dijit.byId('Brick').query,onItem:function(item) {
            count++;
            dojo.forEach(['begin','t_to','t_from','sold','total','plus'], function(i) {
                var ye = 1;
                if (dijit.byId('id_ye_total').get('value') && item.weight == 'Утолщенный') ye = 1.4;
                if (dijit.byId('id_ye_total').get('value') && item.weight == 'Двойной') ye = 2;
                testdata.items[0][i][0] += parseInt(item[i]*ye)
            });
            testdata.items[0]['label'][0] = count + ' наименований Итого:';
        }});
        dijit.byId('BricksTotal').render();
//        console.log(testdata.items[0])
    });

    dijit.byId('id_ye_total').onChange=function(e) {
        dojo.forEach(['begin','t_to','t_from','sold','total'], function(i) {
            testdata.items[0][i][0] = 0;
        });
        var count=0
        BrickStore.fetch({query:dijit.byId('Brick').query,onItem:function(item) {
            count++;
            dojo.forEach(['begin','t_to','t_from','sold','total','plus'], function(i) {
                var ye = 1;
                if (dijit.byId('id_ye_total').get('value') && item.weight == 'Утолщенный') ye = 1.4;
                if (dijit.byId('id_ye_total').get('value') && item.weight == 'Двойной') ye = 2; //TODO: Переделать
                testdata.items[0][i][0] += parseInt(item[i]*ye);
            });
            testdata.items[0]['label'][0] = count + ' кирпичей Итого:';
        }});
        dijit.byId('BricksTotal').render();

    }

    dijit.byId('Brick_info').onStyleRow = function(row) {
//        console.log(row)
        var item = dijit.byId('Brick_info').getItem(row.index);
        if (item) {
            var node = dojo.query('.date',row.node)[0];
            var name = whs.id_to_dict(brick_info.getValue(item, 'id', null)).name;
            if (name == 'sold')
            dojo.addClass(node,'sold');
            if (name =='transfer' && brick_info.getValue(item, 't_to', null))
            dojo.addClass(node,'t_to');
            if (name =='transfer' && brick_info.getValue(item, 't_from', null))
            dojo.addClass(node,'t_from');
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

dojo.addOnLoad(function(){
    dijit.byId('Brick').onCellContextMenu = function(e){
        var item = e.grid.getItem(e.rowIndex);
        var id = whs.id_to_dict(item.id[0]).id
        if (item){
            var menu = new dijit.Menu({targetNodeIds: [e.cellNode]});
            menu.addChild(new dijit.MenuItem({
                label:'Продать этот кирпич',
                onClick: function(event){window.location = '/bill/?sold='+id}
            }));
            menu.addChild(new dijit.MenuItem({
                label:'Показать накладные с этим кирпичем',
                onClick: function(event){window.location = '/bills/?brick='+id}
            }));
            menu.startup();
            menu._openMyself(e);
            dojo.connect(menu,'onClose',function(){menu.uninitialize()})
        }
    };
});
