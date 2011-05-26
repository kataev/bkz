dojo.provide("whs.Form");

dojo.require("whs.OpersWidget");
dojo.require("dijit.form.NumberSpinner");
dojo.require("dijit.form.NumberTextBox");

dojo.declare('whs.Form', null, {
            submit:null,form:null,
            constructor:function(modelName, id) {
                this.url = (id == '' || 0) ? './form/' + modelName + '/' : './form/' + modelName + '/' + id + '/';
                var url = this.url;
                var submit;
                var form;
                var contentPane;
                var opers = {};
                dojo.xhrGet({url:url,handleAs:'json'})
                        .then(function(data) {
                    var div = dojo.create('div', {innerHTML:data.html});
                    dojo.query('.helptext', div).style({display:'none'});
                    dojo.query('*', div).removeAttr('id');
                    contentPane = new dijit.layout.ContentPane({title:data.title,style:'padding:0px;',closable:true}, div);
                    submit = dijit.getEnclosingWidget(dojo.query('.FormSubmit', div)[0]);
                    form = dijit.getEnclosingWidget(dojo.query('form', div)[0]);
                    dojo.query('[multiple]', div).forEach(function(item) {
                        var w = dijit.byNode(item)
                        opers[w.name] = [w.value];
                    });
//                    console.log(opers);
                    dojo.connect(submit, 'onClick', function(e) {
                        console.log('cliked');
                        if (form.validate()) {
                            dojo.xhrPost({
                                        form:form.containerNode,
                                        handleAs:'json'
                                    }, function(error) {
                                contentPane.containerNode.innerHTML = 'Что то пошло не так';
                            })
                                    .then(function(data) {
                                if (data.status != 'fail') {
                                    console.log('ok', data)
                                    submit.set('label', 'Сохранено');
                                    if (submit.mouseAnim) {
                                        submit.mouseAnim.stop();
                                    }

                                    // Set up the new animation
                                    submit.mouseAnim = dojo.animateProperty({
                                                node: submit.focusNode,
                                                properties: {
                                                    backgroundColor: 'green'
                                                },
                                                onEnd: dojo.hitch(this, function() {
                                                    // Clean up our mouseAnim property
                                                    submit.mouseAnim = null;
                                                })
                                            }).play();
//                                    dijit.byId('stackContainer').forward()
                                }
                                else {
                                    console.log('fail', data)
                                    for (var i in data.message) { // Цикл по словарю, берем dijit виджет
                                        var input = dijit.getEnclosingWidget(dojo.query('input[name="' + i + '"]', div))
                                        console.log(input);
                                        input.state = 'Error';
                                        input._setStateClass();// Код не мой, я просто разместил объяву
                                        dijit.setWaiState(input, 'invalid', 'true');
                                        input._maskValidSubsetError = true;
//                                        dijit.showTooltip(data.message[i], input.domNode, input.tooltipPosition); //Это уже мой код, тут показывается тултип
                                    }
                                }
                            });
                        }
                        else {
                            return false;
                        }

                    });


                    if (data.modelType == 'doc') {
                        var OpersTable = dojo.create('table', {style:'font-size:100%;'});
                        for (var a in opers) {
                            dojo.forEach(opers[a][0], function(item, i) {
//                                console.log('item',item);
                                if (item==''){return 0;}
                                dojo.xhrGet({url:'./form/'+a+'/'+item+'/',handleAs:'json'}).then(function(data) {
                                    var tr = dojo.create('tr', {innerHTML:data.html,opersId:item}, OpersTable);
                                    var s=[]
                                    dojo.query('*', tr).removeAttr('id');
                                    dojo.query('[name="amount"],[name="price"],[name="delivery"]', tr).attr('style','width:60px;')
//                                    dojo.query('[name="brick"]', tr).attr('dojoType','whs.BrickSelectWidget')
                                    var a = dojo.parser.parse(OpersTable);
//                                    console.log(a);
                                    for (var widget in a){
                                        if (a[widget].name=='transfers'){
                                            a[widget].values.forEach(function(it,i){
                                            s[it]=item;
                                            })

                                        }
                                    }

                                });
                            });
                        }
                        a = null
                        var border = dijit.byNode(dojo.query('.dijitContainer', contentPane.containerNode)[0]);
                        var contentPane1 = new dijit.layout.ContentPane({style:'padding:0px;height:300px;',content:OpersTable,region:'bottom'});
                        var toolbar = new dijit.Toolbar({region:'bottom',layoutPriority:2});
                        dojo.forEach(["Cut", "Copy", "Paste"], function(label) {
                            var button = new dijit.form.Button({
                                        // note: should always specify a label, for accessibility reasons.
                                        // Just set showLabel=false if you don't want it to be displayed normally
                                        label: label,
                                        showLabel: false,
                                        iconClass: "dijitEditorIcon dijitEditorIcon" + label
                                    });
                            toolbar.addChild(button);
                        });

                        border.addChild(toolbar)
                        border.addChild(contentPane1)

//                    console.log(border);
                    }


                    dijit.byId('TabContainer').addChild(contentPane);
                    dijit.byId('TabContainer').selectChild(contentPane);
                    dojo.connect(dijit.byId('TabContainer'), "removeChild", function(child) {
                        console.log("just removed: ", child);
                        child.destroyRecursive();
                        console.log("destroyed");
                    });
                },
                        function(error) {
                            var contentPane = new dijit.layout.ContentPane({title:'error'.title,style:'padding:0px;',closable:true});
                            dijit.byId('TabContainer').addChild(contentPane);
                            dijit.byId('TabContainer').selectChild(contentPane);
                            dojo.connect(dijit.byId('TabContainer'), "removeChild", function(child) {
                                console.log("just removed: ", child);
                                child.destroyRecursive();
                                console.log("destroyed");
                            });
                        }
                )
                        ;


//                var border = dijit.byNode(dojo.query('.dijitBorderContainer', contentPane.domNode)[0]);

            }
        })
        ;
