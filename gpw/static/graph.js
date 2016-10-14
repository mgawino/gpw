var parseDate = d3.time.format("%Y-%m-%d").parse;

var initGraph = function() {
    margin = {top: 30, right: 20, bottom: 30, left: 50},
        width = 600 - margin.left - margin.right,
        height = 270 - margin.top - margin.bottom;

// Set the ranges
    x = d3.time.scale().range([0, width]);
    y = d3.scale.linear().range([height, 0]);

// Define the axes
    xAxis = d3.svg.axis().scale(x)
        .orient("bottom").ticks(5);

    yAxis = d3.svg.axis().scale(y)
        .orient("left").ticks(5);

// Define the line
    valueline = d3.svg.line()
        .x(function (d) {
            return x(d.date);
        })
        .y(function (d) {
            return y(d.close_price);
        });

// Adds the svg canvas
    svg = d3.select("body")
        .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
        .append("g")
        .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");
};

var clearGraphs = function() {
    var elements = document.getElementsByTagName('svg');
    for(var i = 0; i < elements.length; i++) {
        element = elements[i];
        element.parentNode.removeChild(element);
    }
};

var createGraph = function(companyName) {
    clearGraphs();
    initGraph();
    $.get('http://localhost:8000/data', function(data){
        data = data[companyName];
        data.forEach(function (d) {
            d.date = parseDate(d.date);
            d.close_price = +d.close_price;
        });

        // Scale the range of the data
        x.domain(d3.extent(data, function (d) {
            return d.date;
        }));
        y.domain([0, d3.max(data, function (d) {
            return d.close_price;
        })]);

        // Add the valueline path.
        svg.append("path")
            .attr("class", "line")
            .attr("d", valueline(data));

        // Add the X Axis
        svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0," + height + ")")
            .call(xAxis);

        // Add the Y Axis
        svg.append("g")
            .attr("class", "y axis")
            .call(yAxis);
    });

};

function addSelect() {
   var select = document.createElement('select');
   $.get('http://localhost:8000/companies', function(data) {
       companies = data.companies;
       html = '';
       for (var i = 0; i < companies.length; i++) {
           html += "<option value='" + companies[i] + "'>" + companies[i] + "</option>";
       }
       select.innerHTML = html;
       select.onclick = function() {
           var companyName = select.options[select.selectedIndex].value;
           createGraph(companyName);
       };
       document.body.appendChild(select);
   });
};
addSelect();