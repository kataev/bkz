$(function(){
  json_parse = function(json){
    data = {}
    json.forEach(function(e, index, array){
      var value = e.datapoints[0][0]
      this[parseInt(e.target.split('.')[2])+1] = value 
      },data)
    firing.filter(function(e,i,a){return e.position && data[e.field]})
    

    firing.forEach(function(e,index,array){
      console.log(e.field,e.point,this[e.field],e.position)
    },data)

var $chart = $('#firing')
var margin = {top: 20, right: 80, bottom: 60, left: 50},
    width = $chart.width() - margin.left - margin.right,
    height = 200 - margin.top - margin.bottom;

var y = d3.scale.linear()
    .range([height, 0])
    .domain(d3.extent(firing.filter(function(e,i,a){return e.position && data[e.field]}).map(function(e,i){ return data[e.field]})))


var positions = d3.scale.linear()
    .range([0, width])
    .domain([4,16])

var points = d3.scale.ordinal()
    .range([0, width])
    .domain(d3.extent(_(data).pluck('position')))
    .rangePoints([0, width])


var xAxis = d3.svg.axis()
    .scale(positions)
    .orient("bottom")

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")

var pointAxis = d3.svg.axis()
    .scale(points)
    .orient("bottom")

var line = d3.svg.line()
    // .interpolate("basis")
    .x(function(d) {return positions(d.position || null); })
    .y(function(d) { return y(data[d.field]); })
    .defined(function(d) { return (data[d.field]) })

var svg = d3.select("#firing").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + (height+25) + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "x axis points")
      .attr("transform", "translate(0," + height + ")")
      .call(pointAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)

  svg.append("path")
      .datum(firing)
      .attr("class", "line")
      .attr("d", line)
}
  json_parse([{"target": "cpu.1.0", "datapoints": [[52.9, 1361266540], [52.8, 1361266550], [52.9, 1361266560]]}, {"target": "cpu.1.1", "datapoints": [[57.7, 1361266540], [57.8, 1361266550], [57.8, 1361266560]]}, {"target": "cpu.1.10", "datapoints": [[727.7, 1361266540], [727.3, 1361266550], [727.5, 1361266560]]}, {"target": "cpu.1.11", "datapoints": [[805.4, 1361266540], [805.4, 1361266550], [805.6, 1361266560]]}, {"target": "cpu.1.12", "datapoints": [[871.9, 1361266540], [871.8, 1361266550], [871.8, 1361266560]]}, {"target": "cpu.1.13", "datapoints": [[945.4, 1361266540], [945.7, 1361266550], [945.3, 1361266560]]}, {"target": "cpu.1.14", "datapoints": [[977.8, 1361266540], [977.3, 1361266550], [977.9, 1361266560]]}, {"target": "cpu.1.15", "datapoints": [[978.6, 1361266540], [978.6, 1361266550], [978.9, 1361266560]]}, {"target": "cpu.1.16", "datapoints": [[946.8, 1361266540], [947.1, 1361266550], [947.1, 1361266560]]}, {"target": "cpu.1.17", "datapoints": [[51.5, 1361266540], [51.5, 1361266550], [51.5, 1361266560]]}, {"target": "cpu.1.18", "datapoints": [[456.0, 1361266540], [456.0, 1361266550], [456.1, 1361266560]]}, {"target": "cpu.1.19", "datapoints": [[506.5, 1361266540], [506.5, 1361266550], [506.5, 1361266560]]}, {"target": "cpu.1.2", "datapoints": [[66.6, 1361266540], [66.7, 1361266550], [66.7, 1361266560]]}, {"target": "cpu.1.20", "datapoints": [[0.0, 1361266540], [0.0, 1361266550], [0.0, 1361266560]]}, {"target": "cpu.1.21", "datapoints": [[792.4, 1361266540], [792.3, 1361266550], [792.3, 1361266560]]}, {"target": "cpu.1.22", "datapoints": [[672.0, 1361266540], [672.0, 1361266550], [672.1, 1361266560]]}, {"target": "cpu.1.23", "datapoints": [[537.8, 1361266540], [537.7, 1361266550], [537.8, 1361266560]]}, {"target": "cpu.1.3", "datapoints": [[65.9, 1361266540], [65.8, 1361266550], [65.9, 1361266560]]}, {"target": "cpu.1.4", "datapoints": [[45.0, 1361266540], [45.2, 1361266550], [45.0, 1361266560]]}, {"target": "cpu.1.5", "datapoints": [[46.4, 1361266540], [46.4, 1361266550], [46.4, 1361266560]]}, {"target": "cpu.1.6", "datapoints": [[0.2, 1361266540], [0.1, 1361266550], [0.1, 1361266560]]}, {"target": "cpu.1.7", "datapoints": [[0.0, 1361266540], [0.0, 1361266550], [0.0, 1361266560]]}, {"target": "cpu.1.8", "datapoints": [[3.0, 1361266540], [2.9, 1361266550], [3.0, 1361266560]]}, {"target": "cpu.1.9", "datapoints": [[644.9, 1361266540], [644.4, 1361266550], [644.6, 1361266560]]}])
  // d3.json('/carbon/render/?target=cpu.1.*&format=json&from=-30s',json_parse)

})