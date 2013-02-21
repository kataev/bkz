$(function(){
  json_parse = function(json){
    data = {}
    json.forEach(function(e, index, array){
      var value = e.datapoints[0][0]
      this[parseInt(e.target.split('.')[2])] = value 
      },data)
    firing.filter(function(e,i,a){return e.position && data[e.field]})
    
    
    var tr3 = $('<tr><th>Значение</th></tr>').appendTo('table#help'),
        tr4 = $('<tr><th>Рассогласование</th></tr>').appendTo('table#help'),
        tr1 = $('<tr><th>Точка</th></tr>').appendTo('table#help'),
        tr2 = $('<tr><th>Канал</th></tr>').appendTo('table#help')
        
    firing.forEach(function(e,index,array){
      console.log(e.field,e.point,this[e.field],e.position)
      $('<th>').text(e.point).appendTo(tr1)
      $('<td>').text(e.field).appendTo(tr2)
      $('<td>').text(this[e.field]).appendTo(tr3)
      $('<td>').text((e.target[2]-this[e.field]).toFixed(1)).appendTo(tr4)
    },data)

var $chart = $('#firing')
var margin = {top: 20, right: 10, bottom: 70, left: 50},
    width = $chart.width() - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

var y = d3.scale.linear()
    .range([height, 0])
    .domain(d3.extent(_.union(_.flatten(_.map(firing,function(e){return e.target})),
                              firing.filter(function(e,i,a){return e.position && data[e.field]}).map(function(e,i){ return data[e.field]}))))

var color = d3.scale.category10();

var positions = d3.scale.linear()
    .range([0, width])
    .domain([4,15])
    .clamp(false)

var xAxis = d3.svg.axis()
    .scale(positions)
    .orient("bottom")

var points = d3.svg.axis()
    .scale(positions)
    .orient("bottom")
    .ticks(2)
    .tickValues(firing.map(function(e,i){return e.position}))

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")

var line = d3.svg.line()
    // .interpolate("basis")
    .x(function(d) {return positions(d.position || null) })
    .y(function(d) { return y(data[d.field]) })
    .defined(function(d) { return (data[d.field]) })

var target = d3.svg.line()
    // .interpolate("basis")
    .x(function(d) {return positions(d.position || null); })
    .y(function(d) { return y(d.target[2]); })
    // .defined(function(d) { return (data[d.field]) })

var svg = d3.select("#firing").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + (height+35) + ")")
      .call(xAxis);

svg.append("g")
      .attr("class", "x axis points")
      .attr("transform", "translate(0," + (height+10) + ")")
      .call(points);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)

  svg.select('.points').selectAll('text')
      .data(firing)
      .text(function(e){return e.point})

  svg.append('g')
      .attr('class','target')
      .selectAll('circle.target')
      .data(firing)
      .enter()
      .append('circle')
      .attr('cx',function(d) {return positions(d.position || null); })
      .attr('cy',function(d) { return y(d.target[2]); })
      .attr('r',3)
      .attr('title',function(e){return e.target[2]})

  svg.append('g')
      .attr('class','firing')
      .selectAll('circle')
      .data(firing)
      .enter()
      .append('circle')
      .attr('cx',function(d) {return positions(d.position || null); })
      .attr('cy',function(d) { return y(data[d.field]) })
      .attr('title',function(e) {return data[e.field]})
      .attr('r',3)

  svg.select('g.firing')
      .append("path")
      .datum(firing)
      .attr("class", "line")
      .attr("d", line)

  svg.select('g.target')
      .append("path")
      .datum(firing)
      .attr("class", "line")
      .attr("d", target)
}
  // json_parse([{"target": "cpu.1.0", "datapoints": [[null, 1361418750], [null, 1361418760], [null, 1361418770]]}, {"target": "cpu.1.1", "datapoints": [[49.6, 1361418750], [49.6, 1361418760], [null, 1361418770]]}, {"target": "cpu.1.10", "datapoints": [[609.0, 1361418750], [608.9, 1361418760], [null, 1361418770]]}, {"target": "cpu.1.11", "datapoints": [[717.2, 1361418750], [717.2, 1361418760], [null, 1361418770]]}, {"target": "cpu.1.12", "datapoints": [[825.0, 1361418750], [825.0, 1361418760], [null, 1361418770]]}, {"target": "cpu.1.13", "datapoints": [[873.0, 1361418750], [872.9, 1361418760], [null, 1361418770]]}, {"target": "cpu.1.14", "datapoints": [[945.9, 1361418750], [945.8, 1361418760], [null, 1361418770]]}, {"target": "cpu.1.15", "datapoints": [[978.5, 1361418750], [978.6, 1361418760], [null, 1361418770]]}, {"target": "cpu.1.16", "datapoints": [[978.7, 1361418750], [978.6, 1361418760], [null, 1361418770]]}, {"target": "cpu.1.17", "datapoints": [[947.1, 1361418750], [947.3, 1361418760], [null, 1361418770]]}, {"target": "cpu.1.18", "datapoints": [[47.5, 1361418750], [47.5, 1361418760], [null, 1361418770]]}, {"target": "cpu.1.19", "datapoints": [[470.5, 1361418750], [470.5, 1361418760], [null, 1361418770]]}, {"target": "cpu.1.2", "datapoints": [[54.2, 1361418750], [54.2, 1361418760], [null, 1361418770]]}, {"target": "cpu.1.20", "datapoints": [[530.2, 1361418750], [530.2, 1361418760], [null, 1361418770]]}, {"target": "cpu.1.21", "datapoints": [[553.7, 1361418750], [553.7, 1361418760], [null, 1361418770]]}, {"target": "cpu.1.22", "datapoints": [[801.1, 1361418750], [801.1, 1361418760], [null, 1361418770]]}, {"target": "cpu.1.23", "datapoints": [[693.8, 1361418750], [693.7, 1361418760], [null, 1361418770]]}, {"target": "cpu.1.24", "datapoints": [[552.2, 1361418750], [552.1, 1361418760], [null, 1361418770]]}, {"target": "cpu.1.3", "datapoints": [[49.1, 1361418750], [49.1, 1361418760], [null, 1361418770]]}, {"target": "cpu.1.4", "datapoints": [[59.9, 1361418750], [60.0, 1361418760], [null, 1361418770]]}, {"target": "cpu.1.5", "datapoints": [[44.2, 1361418750], [44.3, 1361418760], [null, 1361418770]]}, {"target": "cpu.1.6", "datapoints": [[50.1, 1361418750], [50.3, 1361418760], [null, 1361418770]]}, {"target": "cpu.1.7", "datapoints": [[0.0, 1361418750], [0.0, 1361418760], [null, 1361418770]]}, {"target": "cpu.1.8", "datapoints": [[0.2, 1361418750], [0.2, 1361418760], [null, 1361418770]]}, {"target": "cpu.1.9", "datapoints": [[2.6, 1361418750], [2.5, 1361418760], [null, 1361418770]]}])
   d3.json('/carbon/render/?target=cpu.1.*&format=json&from=-30s',json_parse)
})
