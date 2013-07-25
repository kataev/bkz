/*
 * User: bteam
 * Date: 05.03.12
 * Time: 19:53
 */
marks = {100: 0, 125: 1, 150: 2, 175: 3, 200: 4, 250: 5, 300: 6, 9000: 7}
label = ['100', '125', '150', '175', '200', '250', '300', '>20']
months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

function transfer(data, param, node) {
    var m = [30, 20, 20, 19], // top right bottom left margin
        w = 180, // width
        h = 180, // height
        z = 18; // cell size
    var i = 0, j = 0;
    var svg = d3.select(node).append("svg")
        .attr("width", w)
        .attr("height", h)

    var mark = svg.append('svg')
        .attr("class", "YlGn")
        .attr("width", label.length * z + z)
        .attr("height", label.length * z + z)
        .attr("x", 20)
        .attr("y", 30)

    var hor = svg.append('svg')
        .attr('preserveAspectRatio', "xMaxYMax meet")

    var ver = svg.append('svg')
        .attr('preserveAspectRatio', "xMaxYMax meet")
        .attr("x", -10)
        .attr("y", 10)

    hor.selectAll("text")
        .data(label)
        .enter().append('text')
        .attr('width', z)
        .attr('height', 2 * z)
        .attr('y', function () {
            return z * ++j + 32
        })
        .attr('x', 25)
        .attr("transform", "translate(-6," + z * 3.5 + ")rotate(-90)")
        .attr("text-anchor", "left")
        .text(String)

    hor.append('text')
        .attr('x', w / 2)
        .attr('y', 10)
        .attr("text-anchor", "middle")
        .text((param.date__year || new Date().getFullYear()) + ' ' + (param.date__month ? months[param.date__month - 1] : ''))

    i = 0
    j = 0
    ver.selectAll("text")
        .data(label.slice(0, -1))
        .enter().append('text')
        .attr('width', z)
        .attr('height', 2 * z)
        .attr('y', function () {
            return 6 + z + (z) * ++i
        })
        .attr('x', function () {
            return z * ++j
        })
        .attr("text-anchor", "right")
        .text(String)

    var row = _(data).pluck('amount__sum')
    var color = d3.scale.quantile()
        .domain(row)
        .range(d3.range(9));

    var rect = mark.selectAll("rect.mark")
        .data(data)
        .enter().append('rect')
        .attr("width", z)
        .attr("height", z)
        .attr("x", function (d) {
            return z * marks[d.brick_from__mark]
        })
        .attr("y", function (d) {
            return z * marks[d.brick__mark]
        })
        .attr("class", function (d) {
            return "mark q" + color(d.amount__sum).toFixed() + "-9";
        })
        .attr("transform", "translate(10,10)")
        .append('title')
        .text(function (d) {
            return 'Марка:' + d.brick_from__mark + ' > ' + d.brick__mark + ' Кол-во:' + d.amount__sum
        })
        .datum(function (d) {
            return d.amount__sum
        })
}

views = {'Л': 1, 'Р': 0}
mass_c = {1.4: 2, 1.0: 1, 0.8: 0, 0.0: 3 }

view_c = ["\u0420\u044f\u0434\u043e\u0432\u043e\u0439", "\u041b\u0438\u0446\u0435\u0432\u043e\u0439"]
weight_c = ["\u0415\u0432\u0440\u043e",
    "\u041e\u0434\u0438\u043d\u0430\u0440\u043d\u044b\u0439",
    "\u0423\u0442\u043e\u043b\u0449\u0435\u043d\u043d\u044b\u0439",
    "\u0414\u0432\u043e\u0439\u043d\u043e\u0439"]
color_c = [ "\u041a\u0440\u0430\u0441\u043d\u044b\u0439",
    "\u0416\u0435\u043b\u0442\u044b\u0439",
    "\u041a\u043e\u0440\u0438\u0447\u043d\u0435\u0432\u044b\u0439",
    "\u0421\u0432\u0435\u0442\u043b\u044b\u0439",
    "\u0411\u0435\u043b\u044b\u0439"]

color_css = ['bc-red', 'bc-yellow', 'bc-brown', 'bc-light', 'bc-white']
function total(data, param, node) {
    var m = [30, 20, 20, 19], // top right bottom left margin
        w = 380, // width
        h = 340, // height
        z = 18; // cell size

    var svg = d3.select(node).append("svg")
        .attr("width", w)
        .attr("height", h)
    svg.append('text')
        .attr('x', w / 2)
        .attr('y', 10)
        .attr("text-anchor", "middle")
        .text((param.date__year || new Date().getFullYear()) + ' ' + (param.date__month ? months[param.date__month - 1] : ''))

    var weight_label = svg.selectAll("text")
        .data(_(mass_c).values())
        .enter().append('text')
        .attr('x', function (d) {
            return d * color_c.length * z + color_c.length * z / 2 + 10
        })
        .attr('y', 20)
        .text(function (d) {
            return weight_c[d]
        })
        .attr("text-anchor", "middle")

    var j = 0
    var view_label = svg.selectAll('text.view')
        .data(view_c)
        .enter().append('text')
        .attr('y', 10)
        .attr('x', function () {
            return -j++ * (label.length) * z - (label.length) * z / 2
        })
        .attr("transform", "translate(-6," + z * 3.5 + ")rotate(-90)")
        .attr('class', 'view')
        .text(String)

    var values = svg.append('svg')
        .attr("class", "BuGn")
        .attr("x", 0)
        .attr("y", 20)
    var q = 0
    for (var w in weight_c) {
        for (var v in view_c) {
            values.append('rect')
                .attr('x', w * z * color_c.length + 10)
                .attr('y', label.length * z * v + 10)
                .attr("width", color_c.length * z + q)
                .attr("height", label.length * z)
                .attr('class', 'rct')
        }
    }


    var row = _(data).pluck('amount__sum')
    var color = d3.scale.quantile()
        .domain(row)
        .range(d3.range(9));

    var rect = values.selectAll("rect.brick")
        .data(data)
        .enter().append('rect')
        .attr("width", z)
        .attr("height", z)
        .attr("x", function (d) {
            return color_c.length * z * mass_c[d.brick__weight] + d.brick__color * z
        })
        .attr("y", function (d) {
            return label.length * z * views[d.brick__view] + z * marks[d.brick__mark]
        })
        .attr("transform", "translate(10,10)")
        .attr("class", function (d) {
            return "brick q" + color(d.amount__sum).toFixed() + '-9';
        })
        .append('title')
        .text(function (d) {
            return weight_c[mass_c[d.brick__weight]] + ' ' + view_c[views[d.brick__view]] + ' ' + d.brick__mark + ' ' + color_c[d.brick__color] + ' Кол-во:' + d.amount__sum
        })
        .append('title')
}


$('div.thumbnail').on('click', 'form button', function (e) {
    e.preventDefault()
    var form = $('form', e.delegateTarget)
    var param = $(form).serializeArray()
    var url = $(e.delegateTarget).data('href')
    $.ajax({url: url, context: this, data: param}).success(function (data) {
        $(this).button('Показать')
        window[$(e.delegateTarget).attr('id')](data, param, $('div:first', e.delegateTarget)[0])
    }).error(function () {
            $(this).button('Ошибка')
        })
    $(this).button('loading')
})