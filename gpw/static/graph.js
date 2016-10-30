// data
var companyName = null;
var statsName = null;
var data = null;
var companies = null;
var statistics = null;


function clearGraphs() {
    var elements = document.getElementsByTagName('svg');
    for(var i = 0; i < elements.length; i++) {
        element = elements[i];
        element.parentNode.removeChild(element);
    }
}

function createGraph() {
    clearGraphs();

    var parseDate = d3.time.format("%Y-%m-%d").parse;
    var margin = {top: 30, right: 20, bottom: 30, left: 50},
    width = 600 - margin.left - margin.right,
    height = 270 - margin.top - margin.bottom;
    var x = d3.time.scale().range([0, width]);
    var y = d3.scale.linear().range([height, 0]);
    var xAxis = d3.svg.axis().scale(x).orient("bottom").ticks(5);
    var yAxis = d3.svg.axis().scale(y).orient("left").ticks(5);

    var svg = d3.select("body")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");
    var companyData = data[companyName];

    // Scale the range of the data
    x.domain(d3.extent(companyData, function (d) {
        return parseDate(d.date);
    }));
    y.domain([0, d3.max(companyData, function (d) {
        return +d[statsName];
    })]);

    var valueline = d3.svg.line().x(function (d) {
            return x(parseDate(d.date));
        }).y(function (d) {
            return y(+d[statsName]);
        });

    // Add the valueline path.
    svg.append("path")
        .attr("class", "line")
        .attr("d", valueline(companyData));

    // Add the X Axis
    svg.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    // Add the Y Axis
    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis);
}

function addSelect(collection, clickCallback) {
   var select = document.createElement('select');
   html = '';
   for (var i = 0; i < collection.length; i++) {
       html += "<option value='" + collection[i] + "'>" + collection[i] + "</option>";
   }
   select.innerHTML = html;
   select.onchange = function() {
       clickCallback(select.options[select.selectedIndex].value);
       if (companyName !== null && statsName !== null) {
           createGraph();
       }
   };
   document.body.appendChild(select);
}

$.when(
    $.get('http://localhost:8000/data', function(d){
        data = d;
    }),
    $.get('http://localhost:8000/companies', function(d){
        companies = d.companies;
    }),
    $.get('http://localhost:8000/statistics', function(d){
        statistics = d.statistics;
    })
).then(function() {
    addSelect(companies, function(selectedCompanyName) {
        companyName = selectedCompanyName;
    });
    addSelect(statistics, function(selectedStatsName) {
        statsName = selectedStatsName;
    });
});