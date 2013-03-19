$(function(){
var $chart = $('#chart')
var margin = {top: 20, right: 20, bottom: 20, left: 20},
    width = $chart.width() - margin.left - margin.right,
    height = 260 - margin.top - margin.bottom;

var svg = d3.select("#chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")


tto_width = 82
tto_height = 6

svg.selectAll('.tto')
	.data([1])
	.enter().append('g')
		.attr('class','tto')
		.attr("transform", "translate(40,40)")
			.append('rect')
			.attr('width',tto_width)
			.attr('height',tto_height)

svg.select('.tto').selectAll('circle')
	.data([1,2])
	.enter().append('circle')
		.attr('r', 4)
		.attr('cx', function(d){ return d*52-37 })
		.attr('cy', 12)

svg.select('.tto').selectAll('.poddon')
	.data([1,2,3,3,4,5])
	.enter()
		.append('rect')
		.attr('width',20)
		.attr('height',20)
		.attr('x',function(d){ return d*7 })
		.attr('y',function(d){ return -d*2 })



})