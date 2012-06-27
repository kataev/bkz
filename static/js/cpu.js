

var context = cubism.context(),
    graphite = context.graphite('http://3авод/graphite');

var foo = graphite.metric(function(start, stop, step, callback){
    console.log(graphite.toString())
//    $.ajax({dataType:'jsonp',jsonp:'jsonp',url:graphite.toString(),data:{format:'jsonp',target:'cpu.termodat22m.1',from:start,unlit:stop}}).success(callback)
});


d3.select('#firing').call(function(div){
    div.append('div')
        .attr('class','axis')
        .call(context.axis().orient('top'));

    div.selectAll('.horizon')
        .data([foo,])
        .enter().append('div')
        .attr('class','horizon')
        .call(context.horizon().extent([-20,20]))

    div.append('div')
        .attr('class','rule')
        .call(context.rule())
})