
dojo.require("whs.BrickWidget");
dojo.require("whs.OpersWidget");
dojo.require("whs.Form");


dojo.require("dijit.Toolbar");
dojo.require("dijit.layout.BorderContainer");
dojo.require("dijit.layout.TabContainer");
dojo.require("dijit.layout.ContentPane");
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



dojo.addOnLoad(function() {
   dojo.parser.parse();
memoryStore = new dojo.store.Memory({});
restStore = new dojo.store.JsonRest({target:"/json/bricks/"});
brick = new dojo.store.Cache(restStore, memoryStore);
});

dojo.addOnLoad(function() {
//    brick.query();
//    for (var a = 1;a<190;a++){
//        var br = new whs.BrickWidget({BrickId:a});dojo.place(br.domNode,'test');
//
//    }


    dojo.query('.menuCreate .dijitMenuItemLabel').connect('onclick', function(evt) {
        new whs.Form(dijit.getEnclosingWidget(evt.srcElement).modelName,0);
//        form.then(function(data) {
////                   console.log(data);
//            var div = dojo.create('div', {innerHTML:data.html})
//            dojo.query('.helptext', div).style({display:'none'})
//            dojo.query('*', div).removeAttr('id');
//            var contentPane = new dijit.layout.ContentPane({title:data.title,style:'padding:0px;',closable:true}, div);
////                   var contentPane = dijit.byNode(cont.children[0])
////                   dojo.parser.parse(contentPane.domNode);
//            var border = dijit.byNode(dojo.query('.dijitBorderContainer', contentPane.domNode)[0])
//            console.log('border', border, 'content', contentPane);
//            dijit.byId('TabContainer').addChild(contentPane);
//            dijit.byId('TabContainer').selectChild(contentPane);
//        });
//        dojo.connect(dijit.byId('TabContainer'), "removeChild", function(child) {
//            console.log("just removed: ", child);
//            child.destroyRecursive();
//            console.log("destroyed");
//        });


    });
});
