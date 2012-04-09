/*
 * User: bteam
 * Date: 05.03.12
 * Time: 19:53
 */
var m = [30, 20, 20, 19], // top right bottom left margin
    w = 180, // width
    h = 160, // height
    z = 18; // cell size


sizes = {100:0, 125:1, 150:2, 175:3, 200:4, 250:5, 300:6, 9000:7}
label = ['100', '125', '150', '175', '200', '250', '300', '>20']
months = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']

function draw(data,param,node) {
    var i = 0,j = 0;
    var svg = d3.select(node || "#transfer").append("svg")
        .attr("width",w)
        .attr("height",h)

    var mark = svg.append('svg')
        .attr("class", "YlGn")
        .attr("width",label.length*z+z)
        .attr("height",label.length*z+z)
        .attr("x", 20)
        .attr("y", 30)

    var hor = svg.append('svg')
        .attr('preserveAspectRatio',"xMaxYMax meet")

    var ver = svg.append('svg')
        .attr('preserveAspectRatio',"xMaxYMax meet")
        .attr("x", -10)
        .attr("y", 10)

    hor.selectAll("text")
        .data(label)
        .enter().append('text')
        .attr('width', z)
        .attr('height', 2 * z)
        .attr('y', function (d) { return z * ++j + 32 })
        .attr('x', 25)
        .attr("transform", "translate(-6," + z * 3.5 + ")rotate(-90)")
        .attr("text-anchor", "left")
        .text(String)

    hor.append('text')
        .attr('x',w/2)
        .attr('y',10)
        .attr("text-anchor", "middle")
        .text( (param.date__year || new Date().getFullYear()) +' ' + (param.date__month ? months[param.date__month-1]:'') )

    i = 0
    j=0
    ver.selectAll("text")
        .data(label.slice(0,-1))
        .enter().append('text')
        .attr('width', z)
        .attr('height', 2 * z)
        .attr('y', function (d) { return 6+z+(z)*++i })
        .attr('x', function (d) { return z * ++j})
        .attr("text-anchor", "right")
        .text(String)

    var row = _(data).pluck('v')
    var color = d3.scale.quantile()
        .domain(row.reverse())
        .range(d3.range(8));
    var rect = mark.selectAll("rect.mark")
        .data(data)
        .enter().append('rect')
        .attr("width", z)
        .attr("height", z)
        .attr("x", function (d) { return z * sizes[d.f]})
        .attr("y", function (d) { return z * sizes[d.t]})
        .attr("class", function (d) { return "mark q" + color(d.v).toFixed() + "-8"; })
        .attr("transform", "translate(10,10)")
        .append('title')
        .text(function (d) { return 'Марка:' + d.f + ' > ' + d.t + ' Кол-во:' + d.v })
        .datum(function (d) { return d.v })
}

$('#transfer_show').click(function(e){
    e.preventDefault()
    var year  = $('[name="date__year"]').val()
    var month  = $('[name="date__month"]').val()
    var param = {}
    if (year){
        param.date__year = year
        if (month) param.date__month = month
    }
    url = "Статистика/Переводы/"
    if (param) url += '?' + $.param(param);
    $.ajax({url:url, context:this }).success(function(data){
        $(this).button('Показать')
        draw(data,param)
    }).error(function(){$(this).button('Ошибка')})
    $(this).button('loading')
})


function totals(data){
    var svg = d3.select("totals").append("svg")
        .attr("width",w)
        .attr("height",h)

    var mark = svg.append('svg')
        .attr("class", "YlGn")
        .attr("width",label.length*z+z)
        .attr("height",label.length*z+z)
        .attr("x", 20)
        .attr("y", 30)

}