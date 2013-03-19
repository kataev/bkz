$(function(){
var $chart = $('#chart')
var margin = {top: 20, right: 80, bottom: 30, left: 50},
    width = $chart.width() - margin.left - margin.right,
    height = 250 - margin.top - margin.bottom;
var vacuum = 0
data = $('tbody tr').not('.fake').map(function(){ 
        var tts = $(this).find('input[name*="tts"]').val()
        var density = $(this).find('input[name*="density"]').val()
        vacuum = $(this).find('input[name*="vacuum"]').val() || vacuum
        if (density) {
        return {tts:+tts,"Плотность":parseFloat(density),"Вакуум":parseFloat(vacuum)}
        }
     })
if (!data.length) return;


var x = d3.scale.ordinal()
    .range([0, width])
    .domain(data.map(function(i,d){return d.tts}))
    .rangePoints([0, width])

var y = d3.scale.linear()
    .range([height, 0]);

var color = d3.scale.category10();

var xAxis = d3.svg.axis()
    .scale(x)
    .orient("bottom")

var yAxis = d3.svg.axis()
    .scale(y)
    .orient("left")

var line = d3.svg.line()
    // .interpolate("basis")
    .x(function(d,i) { return x(d.tts); })
    .y(function(d) { return y(d.temperature); });

var svg = d3.select("#chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");


  color.domain(d3.keys(data[0]).filter(function(key) { return key !== "tts"; }));


  cities = color.domain().map(function(name) {
    return {
      name: name,
      values: data.map(function(i,d) {
        return {tts: d.tts, temperature: d[name]};
      })
    };
  });

  y.domain([
    d3.min(cities, function(c) { return d3.min(c.values, function(v) { return v.temperature; }); }),
    d3.max(cities, function(c) { return d3.max(c.values, function(v) { return v.temperature; }); })
  ]);

  svg.append("g")
      .attr("class", "x axis")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis);

  svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)

  var city = svg.selectAll(".city")
      .data(cities)
    .enter().append("g")
      .attr("class", "city");

  city.append("path")
      .attr("class", "line")
      .attr("d", function(d) { return line(d.values); })
      .style("stroke", function(d) { return color(d.name); });

  city.append("text")
      .datum(function(d) { return {name: d.name, value: d.values[d.values.length - 1]}; })
      .attr("transform", function(d) { return "translate(" + x(d.value.tts) + "," + y(d.value.temperature) + ")"; })
      .attr("x", 3)
      .attr("dy", ".35em")
      .text(function(d) { return d.name; });
});