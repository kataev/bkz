dojo.provide('whs.form.Form');

dojo.require('dijit.form.Form');
dojo.require('dijit.Tooltip');

dojo.require('dojo.hash');


dojo.declare('whs.form.Form', dijit.form.Form, {
    onSuccess:function(data) {

    },
    onSubmit : function(event) { //Переопределяем метод болванку для сабмита
        var onSuccess = dojo.hitch(this, 'onSuccess');
        dojo.stopEvent(event); // Тормoзим сабмит для ajax отправки данных
        if (this.get('state') == '') {
            var getChildren = dojo.hitch(this, 'getChildren');
            dojo.xhrPost({ // Отправляем ajax пост запросом
                form:this.domNode, // данные берем из input нод ноды формы
                'handleAs':'json' // ответ разпарсить в виже json
            }).then(function(data) { // Deferred success OnSucces callback
                    if (data.success) { // Если сервер ответил об удаче, то показать юзеру положительный ответ
                        console.log(data, 'all good');
                        onSuccess(data);
                    }
                    else { // Если сервер ответсит об неудаче ( серверая валидация неудалась )
                        console.log(data, 'server validation fail');
                        dojo.forEach(getChildren(), function(widget) { // перебираем виджеты формы
                            if (data.errors[widget.name]) { // Если имя виджета в сообщениях об ошибке
                                if (widget._refreshState) { // Если виджет сам обновляет сообщение об ошибке
                                    widget.state = 'Error';     // Вывести сообщение об ошибке
                                    widget._setStateClass();    // А если не обновляет(CheckBox) то пропустить
//                                    widget.set('WaiState  ', 'invalid', 'true');
                                    widget._maskValidSubsetError = true;
                                }
                                var tip = new dijit.Tooltip({ // Текст ошибки
                                    label:data.errors[widget.name],
                                    connectId:[widget.domNode],
                                    position:widget.tooltipPosition});
                            }
                            delete data.errors[widget.name];
                        });
                        dojo.forEach(data.errors, function(name) {
                            dojo.create('div',{innerHTML:data.errors[name]},'error_msg');
                        });
                    }
                }, function(error) { // Deferred error, onError callback
                    console.log('Server or connect error', error);
                    dojo.create('div',{innerHTML:'Что то пошло не так.'},'error_msg')
                });
        } else {
            console.log(this, event, this.get('state'), 'not valid widgets')
        }
        return this.isValid();
//                console.log(event, 'submit', form.get('value'));
    }

});


dojo.provide('whs.form.Form.Bill');

dojo.declare('whs.form.Form.Bill', whs.form.Form, {
    onSuccess:function(data) {
        dojo.hash(data.id);
//        var brick = document.location.href.split('sold=')[1];
//        if (brick) document.location = '/sold/?doc=' + id + '&brick='+brick;
//        else {
//            if (!window.location.pathname.split('/')[2])
//            document.location = '/bill/' + id + '/';}
    }
});

dojo.provide('whs.form.Form.Oper');

dojo.declare('whs.form.Form.Oper', whs.form.Form, {
    onSuccess:function(data) {
//        var name = window.location.pathname.split('/')[1]
        if (window.opener){
            window.opener.dojo.publish('whs/FKSelect',[{value:this.get('value'),id:data.id}]);
            window.close()

        }else{
            document.location = '/bill/'+this.get('value')['doc']+'/';
        }

    }
});