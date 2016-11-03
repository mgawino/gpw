var companyNames = null;
var selectedCompanyName = null;
var statNames = null;
var selectedStatName = null;
var SERVER_URL = 'http://localhost:8000';

function clearGraphs() {
    var elements = document.getElementsByTagName('svg');
    for(var i = 0; i < elements.length; i++) {
        element = elements[i];
        element.parentNode.removeChild(element);
    }
}

function createGraph(companyData) {
    clearGraphs();

    var parseDate = d3.time.format("%Y-%m-%d").parse;
    var margin = {top: 30, right: 20, bottom: 30, left: 50},
    width = 600 - margin.left - margin.right,
    height = 270 - margin.top - margin.bottom;
    var x = d3.time.scale().range([0, width]);
    var y = d3.scale.linear().range([height, 0]);
    var xAxis = d3.svg.axis().scale(x).orient("bottom").ticks(7);
    var yAxis = d3.svg.axis().scale(y).orient("left").ticks(7);

    var svg = d3.select("body")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
              "translate(" + margin.left + "," + margin.top + ")");

    companyData.forEach(function(d) {
      d.date = parseDate(d.date);
      d.value = +d.value;
    });
    // Scale the range of the data
    x.domain(d3.extent(companyData, function (d) {
        return d.date;
    }));
    y.domain([0, d3.max(companyData, function (d) {
        return d.value;
    })]);

    var valueline = d3.svg.line().x(function (d) {
            return x(d.date);
        }).y(function (d) {
            return y(d.value);
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
       if (selectedCompanyName !== null && selectedStatName !== null) {
           var url = SERVER_URL + '/data/' + selectedCompanyName + '/' + selectedStatName + '/';
           $.get(url, function(companyData){
               createGraph(companyData.results);
           });
       }
   };
   document.body.appendChild(select);
}

$.when(
    $.get(SERVER_URL + '/company_names', function(data){
        companyNames = data.company_names;
    }),
    $.get(SERVER_URL + '/stat_names', function(data){
        statNames = data.stat_names;
    })
).then(function() {
    addSelect(companyNames, function(companyName) { selectedCompanyName = companyName; });
    addSelect(statNames, function(statName) { selectedStatName = statName; });
});