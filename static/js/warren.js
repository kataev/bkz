$(function(){
$chart = $('#chart')
margin = {top: 20, right: 20, bottom: 30, left: 30},
width = $chart.width() - margin.left - margin.right,
height = 160 - margin.top - margin.bottom;

svg = d3.select("#chart").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")")


data = [{number:'1/2',tts:[11,28,32]},{number:'2',tts:[15,46,71,85]},{number:3,tts:[9,43],rows:9}]
data = json

yScale = d3.scale.linear().range([0,height]).domain([16,0])

svg.selectAll('g.tto')
	.data(data)
	.enter()
		.append('g')
		.attr('class','tto')
		.attr("transform", function(d,i){return "translate(" + (i*yScale(6)) + ","+ 0 +")"})
		.selectAll('rect')
		.data(function(d,i){
			var tts = this.parentNode.__data__.tts;
			var rows = this.parentNode.__data__.rows || 16;
			return tts.map(function(e){ return {number:e,size:rows/tts.length} }) })
		.enter()
			.append('rect')
			.attr('class','poddon')
			.attr('y',function(d,i){ return yScale((i+1)*d.size) })
			.attr('width',yScale(6))
			.attr('height',function(d,i){ return yScale(16-d.size) })

svg.selectAll('g.tto')
	.data(data)
		.selectAll('text')
		.data(function(d,i){
			var tts = this.parentNode.__data__.tts;
			var rows = this.parentNode.__data__.rows || 16;
			return tts.map(function(e){ return {number:e,size:(rows/tts.length) } }) })
		.enter()
			.append('text')
			.attr('y',function(d,i){ return yScale((i+0.45)*d.size) })
			.attr('x',function(d,i){ return yScale(11) })
			.text(function(d){ return d.number })


var yAxis = d3.svg.axis()
    .scale(yScale)
    .orient("left")

svg.append("g")
      .attr("class", "y axis")
      .call(yAxis)

})