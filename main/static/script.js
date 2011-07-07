
dojo.require("whs.BrickWidget");
dojo.require("whs.BrickSelectWidget");
//dojo.require("whs.OpersWidget");
dojo.require("whs.Form");
dojo.require("dojo.data.ItemFileReadStore");
dojo.require("dijit.Tree");
 dojo.require("dojo.date.locale");
dojo.require("dijit.Toolbar");
dojo.require("dijit.layout.BorderContainer");
dojo.require("dijit.layout.TabContainer");
dojo.require("dijit.layout.TabContainer");
dojo.require("dijit.layout.AccordionContainer");
//        dojo.require("dijit.Dialog");
dojo.require("dojo.data.ItemFileReadStore");
dojo.require("dijit.MenuBar");
dojo.require("dijit.PopupMenuBarItem");
dojo.require("dijit.Menu");
dojo.require("dijit.Toolbar");
dojo.require("dijit.MenuItem");
dojo.require("dijit.PopupMenuItem");
dojo.require('dijit.form.ValidationTextBox');
dojo.require('dijit.form.DateTextBox');
dojo.require('dijit.form.NumberTextBox');
dojo.require('dijit.form.Form');
dojo.require('dijit.form.Button');
dojo.require('dijit.form.Select');
dojo.require('dijit.form.MultiSelect');
//        dojo.require("dijit.layout.StackContainer");
dojo.require("dijit.form.Button");
dojo.require("dojo.parser");
dojo.require("dojo.store.JsonRest");
dojo.require("dojo.store.Memory");
dojo.require("dojo.store.Cache");

dojo.require("dojo.data.ItemFileWriteStore");
dojo.require("dojox.grid.DataGrid");


BrickClass = ['class_red','class_yellow','class_brown','class_light','class_white','class_euro','class_other']
//BrickColor = ['brick_red','brick_yellow','brick_brown','brick_light','brick_white']
BrickColor={'Кр':'color_red','Же':'color_yellow','Ко':'color_brown','Св':'color_light','Бе':'color_white'}

dojo.addOnLoad(function() {
//dojo.parser.parse();

var schema = {"type": "object", "description": "\u041a\u0438\u0440\u043f\u0438\u0447", "properties": {"refuse": {"type": "string", "maxLength": 10}, "features": {"type": "string", "maxLength": 60}, "weight": {"type": "string", "maxLength": 60}, "color": {"type": "string", "maxLength": 60}, "name": {"type": "string", "maxLength": 160}, "color_type": {"type": "string", "maxLength": 6}, "defect": {"type": "string", "maxLength": 60}, "mark": {}, "brick_class": {"type": "integer"}, "total": {}, "id": {"type": "integer"}, "view": {"type": "string", "maxLength": 60}}}

memoryStore = new dojo.store.Memory({});
restStore = new dojo.store.JsonRest({target:"/json/bricks/"});
brick = new dojo.store.Cache(restStore, memoryStore);

pMenu = new dijit.Menu({
//            targetNodeIds: ["prog_menu"]
        });
        pMenu.addChild(new dijit.MenuItem({
            label: "Menu Item With an icon",
            iconClass: "dijitEditorIcon dijitEditorIconCut",
            onClick: function() {
                whs.Form('bricks',0)
            }
        }));
        pMenu.startup();


store = new dojo.data.ItemFileWriteStore({url:"brick/"});
gridLayout = [
//    { name: 'Id', field: 'id'},
    { name: 'Label', field: 'label',width:'190px',noscroll:true}
//    { name: 'total', field: 'total'}
];

var grid = new dojox.grid.DataGrid({
    region:'center',
    headerMenu:pMenu,
//    editable:true,
    query:{mark:'*'},
    store: store,
    structure: gridLayout
}, dojo.byId("br"));
    
    grid.startup()
dojo.connect(grid,'onRowContextMenu',function(e){

    console.log(e)
})




//dojo.place(new whs.BrickSelectWidget().domNode,'test')
//dojo.date.locale.addCustomFormats('d.M.y m.h','m.h')
//new whs.Form('bills',2);

});

dojo.addOnLoad(function() {
//    brick.query();
//    for (var a = 1;a<10;++a){
//        var br = new whs.BrickSelectWidget({BrickId:a});dojo.place(br.domNode,'test');
//
//    }
//
//
    dojo.query('.menuCreate .dijitMenuItemLabel').connect('onclick', function(evt) {
        new whs.Form(dijit.getEnclosingWidget(evt.srcElement).modelName,0);

//        form.then(function(data) {
//////                   console.log(data);
////            var div = dojo.create('div', {innerHTML:data.html})
////            dojo.query('.helptext', div).style({display:'none'})
////            dojo.query('*', div).removeAttr('id');
////            var contentPane = new dijit.layout.ContentPane({title:data.title,style:'padding:0px;',closable:true}, div);
//////                   var contentPane = dijit.byNode(cont.children[0])
//////                   dojo.parser.parse(contentPane.domNode);
////            var border = dijit.byNode(dojo.query('.dijitBorderContainer', contentPane.domNode)[0])
////            console.log('border', border, 'content', contentPane);
////            dijit.byId('TabContainer').addChild(contentPane);
////            dijit.byId('TabContainer').selectChild(contentPane);
////        });
////        dojo.connect(dijit.byId('TabContainer'), "removeChild", function(child) {
////            console.log("just removed: ", child);
////            child.destroyRecursive();
////            console.log("destroyed");
////        });
//
//
    });
});
