dojo.provide('whs.core');

dojo.registerModulePath("whs", "/static/js");

dojo.require("dijit.layout.BorderContainer");
dojo.require("dijit.layout.TabContainer");
dojo.require("dijit.layout.ContentPane");

dojo.require("dijit.MenuBar");
dojo.require("dijit.MenuItem");
dojo.require("dijit.PopupMenuBarItem");


dojo.require("whs.main.MenuItem");
dojo.require("whs.main.Open");

var dojoConfig = {
            isDebug: true,
            locale: 'Ru-ru'
            ,'parseOnLoad':true
        };

//dojo.addOnLoad(function(){
//    dojo.query('.bills_table tr').connect('onclick',function(evt){
//        window.location = '/bill/' + dojo.attr(this,'pk') + '/';
//    });
//});

dojo.provide('whs.names');
whs.names = {bill:['sold','transfer']}
dojo.provide('whs.upper');
whs.upper = function(s){return s[0].toLocaleUpperCase().concat(s.slice(1))}


dojo.provide('whs.locale');
whs.locale = {bill:'накладная',sold:'продажа',transfer:'перевод'}


dojo.provide('whs.prefix');
whs.prefix = {'mark':'m','class':'cl_'}

dojo.provide('whs.css_order');

whs.css_order = ['weight','mark','brick_class','view'];


dojo.provide('whs.id_to_url');

whs.id_to_url = function(s) {
    s = ''+s;
    var name = s.split('.')[1].split('__')[0];
    var id = s.split('.')[1].split('__')[1];
    return '/'+name+'/'+id+'/';
};

dojo.provide('whs.id_to_dict');
whs.id_to_dict = function(s) {
    s = ''+s;
    var name = s.split('.')[1].split('__')[0];
    var id = s.split('.')[1].split('__')[1];
    return {name:name,id:id};
};

dojo.provide('whs.grid.date_formatter');
whs.date_formatter = function (date){
    return dojo.date.locale.format(new Date(date),{selector:'date',datePattern:'MMM d, yyyy'});
}