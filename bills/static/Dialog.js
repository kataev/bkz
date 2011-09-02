dojo.provide('whs.Dialog');

dojo.require('dijit.Dialog');

dojo.declare('whs.Dialog',dijit.Dialog,{
    templateString: dojo.cache('whs', 'template/Dialog.html')
        });