dojo.provide('whs.Form');

dojo.require('dijit.form.Form');
dojo.require('dijit.Tooltip');

dojo.declare('whs.Form', dijit.form.Form, {
    onSuccess:function(id) {

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
                        onSuccess(data.id);
                    }
                    else { // Если сервер ответсит об неудаче ( серверая валидация неудалась )
                        console.log(data, 'server validation fail');
                        dojo.forEach(getChildren(), function(widget) { // перебираем виджеты формы
//                            console.log(widget);
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
                        });
                    }
                }, function(error) { // Deferred error, onError callback
                    console.log('Server or connect error', error);
                });
        } else {
            console.log(this, event, this.get('state'), 'not valid widgets')
        }
        return this.isValid();
//                console.log(event, 'submit', form.get('value'));
    }

});


dojo.provide('whs.Form.Bill');

dojo.declare('whs.Form.Bill', whs.Form, {
    onSuccess:function(id) {
        if (document.location.href.split('bill')[1] == '/') {
            document.location = '/bill/' + id + '/';
        }
    }
});

dojo.provide('whs.Form.Oper');

dojo.declare('whs.Form.Oper', whs.Form, {
    onSuccess:function(id) {
        document.location = '/bill/' + dojo.queryToObject(document.location.href.split('?')[1]).bill + '/';
    }
});