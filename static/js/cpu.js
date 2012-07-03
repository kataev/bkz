var context = cubism.context()
    .step(3e4)
    .size(3e6)
//    .size(1440)
//    .clientDelay(60*1000*170)
//    .serverDelay(-60*1000*155)
var graphite = context.graphite('Датчики');

//context.scale = d3.time.scale
var foo = graphite.metric("cpu.22.34")


//var foo = graphite.metric(function(start, stop, step, callback){
//    console.log(graphite.toString())
//    $.ajax({dataType:'jsonp',jsonp:'jsonp',url:graphite.toString(),data:{format:'jsonp',target:'cpu.termodat22m.1',from:start,unlit:stop}}).success(callback)
//});


d3.select('#firing').call(function (div) {
    div.append('div')
        .attr('class', 'axis')
        .call(context.axis().orient('top'));

    div.selectAll('.horizon')
        .data([foo, ])
        .enter().append('div')
        .attr('class', 'horizon')
        .call(context.horizon().extent([0, 100]))

    div.append('div')
        .attr('class', 'rule')
        .call(context.rule())
})