var b = 10,
    m = 25,
    color = d3.interpolateRgb('#aad','#556');


data = _(positions).map(function(v,k){return {x:v,y:parseInt(k)}})
//data = _(_.range(25)).map(function(d){ return {x:d,y:d} })

var margin = 20,
    padding = 10,
    width = 960,
    height = 500 - .5 - margin,
    x = function(d) {return d.x * width / mx;},
    y0 = function(d) {return height - d.y * height / my};

var vis = d3.select('#firing')
    .append('svg')
    .attr('width',width)
    .attr('height',height + margin);

var layers = vis.selectAll('rect.bar')
    .data(data)
    .enter().append('rect')
    .style('fill','#0f4')
    .attr('class','bar')
    .attr('x',function(d){return ( b + padding ) * d.x})
    .attr('y',function(d){return height - margin - d.y })
    .attr('height',function(d){return d.y })
    .attr('width',b)

