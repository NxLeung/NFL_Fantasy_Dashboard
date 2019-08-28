// Define SVG area dimensions
let svgWidth = 960;
let svgHeight = 500;

// Define the chart's margins as an object
let margin = {
  top: 60,
  right: 60,
  bottom: 60,
  left: 60
};

// Define dimensions of the chart area
let chartWidth = svgWidth - margin.left - margin.right;
let chartHeight = svgHeight - margin.top - margin.bottom;

// Select body, append SVG area to it, and set its dimensions
let svg = d3
  .select("body")
  .append("svg")
  .attr("width", svgWidth)
  .attr("height", svgHeight);

// Append a group area, then set its margins
let chartGroup = svg.append("g")
  .attr("transform", `translate(${margin.left}, ${margin.top})`);

// Load data from playertable.csv
d3.json('http://127.0.0.1:5000/player_data?player_name=I.Smith', function(error,playerData) {

  // Throw an error if one occurs
  if (error) throw error;

  // Print the playerData
  console.log(playerData);

  // Configure a parseTime function which will return a new game_year object from a string
  let parseTime = d3.timeParse("%Y");
  
  // Format the game_year and cast the  value to a number
  playerData.forEach(function(d) {
    d.game_year = parseTime(d.game_year);
    d.passing_yards_gained= +d.passing_yards_gained;
    d.receiving_yards_gained= +d.receiving_yards_gained;
    d.rushing_yards_gained= +d.rushing_yards_gained;
  });

  // Configure a time scale with a range between 0 and the chartWidth
  // Set the domain for the xTimeScale function
  // d3.extent returns the an array containing the min and max values for the property specified
  let xTimeScale = d3.scaleTime()
    .range([0, chartWidth])
    .domain(d3.extent(playerData, data => data.game_year));

  // Configure a linear scale with a range between the chartHeight and 0
  // Set the domain for the xLinearScale function
  let yLinearScale1 = d3.scaleLinear()
    .range([chartHeight, 0])
    .domain([d3.min(playerData, data => data.passing_yards_gained), d3.max(playerData, data => data.passing_yards_gained)]);

  let yLinearScale2 = d3.scaleLinear()
    .range([chartHeight, 0])
    .domain([d3.min(playerData, data => data.receiving_yards_gained), d3.max(playerData, data => data.rushing_yards_gained)]);

  
  // Create two new functions passing the scales in as arguments
  // These will be used to create the chart's axes
  let bottomAxis = d3.axisBottom(xTimeScale)
      .tickFormat(d3.timeFormat("%Y"));
  let leftAxis = d3.axisLeft(yLinearScale1);
  let rightAxis = d3.axisRight(yLinearScale2);

  // Add x-axis
  chartGroup.append("g")
    .classed("axis", true)
    .attr("transform", `translate(0, ${chartHeight})`)
    .call(bottomAxis);

  // Add y1-axis to the left side of the display
  chartGroup.append("g")
  // Define the color of the axis text
  .classed("black", true)
  .call(leftAxis);

  // Add y2-axis to the right side of the display
  chartGroup.append("g")
  // Define the color of the axis text
  .classed("black", true)
  .attr("transform", `translate(${chartWidth}, 0)`)
  .call(rightAxis);


  // Configure a drawLine function which will use our scales to plot the line's points
  let drawLine1 = d3
    .line()
    .x(d => xTimeScale(d.game_year))
    .y(d => yLinearScale1(d.passing_yards_gained));

  let drawLine2 = d3
    .line()
    .x(d => xTimeScale(d.game_year))
    .y(d => yLinearScale2(d.receiving_yards_gained));

  let drawLine3 = d3
    .line()
    .x(d => xTimeScale(d.game_year))
    .y(d => yLinearScale2(d.rushing_yards_gained));

  // Append an SVG path and plot its points using the line function
  chartGroup.append("path")
    // The drawLine function returns the instructions for creating the line for playerData
    .attr("d", drawLine1(playerData))
    .classed("line green", true);

  chartGroup.append("path")
    // The drawLine function returns the instructions for creating the line for playerData
    .attr("d", drawLine2(playerData))
    .classed("line blue", true);

  chartGroup.append("path")
    // The drawLine function returns the instructions for creating the line for playerData
    .attr("d", drawLine3(playerData))
    .classed("line orange", true);

 // Append axes titles
 chartGroup.append("text")
 .attr("transform", `translate(${chartWidth / 2}, ${chartHeight})`)
   .classed("yards text", true)
   .text("Number of Yards");

// append circles (passing)
var circlesGroup = chartGroup.selectAll("circle")
.data(playerData)
.enter()
.append("circle")
.attr("cx", d => xTimeScale(d.game_year))
.attr("cy", d => yLinearScale1(d.passing_yards_gained))
.attr("r", "5")
.attr("fill", "green")
.attr("stroke-width", "1")
.attr("stroke", "black");

//   // Step 1: Append tooltip div
//   var toolTip = d3.select("body")
//   .append("div")
//   .classed("tooltip", true);

// // Step 2: Create "mouseover" event listener to display tooltip
// circlesGroup.on("mouseover", function(d) {
//   toolTip.style("display", "block")
//       .html(
//         `<strong>${dateFormatter(d.game_year)}<strong><hr>${d.passing_yards_gained}
//     yards`)
//       .style("left", d3.event.pageX + "px")
//       .style("top", d3.event.pageY + "px");
// })
//   // Step 3: Create "mouseout" event listener to hide tooltip
//   .on("mouseout", function() {
//     toolTip.style("display", "none");
//   });

// append circle (receiving)
var circlesGroup2 = chartGroup.selectAll("circle")
.data(playerData)
.enter()
.append("circle")
.attr("width", d => xTimeScale(d.game_year))
.attr("height", d => yLinearScale2(d.receiving_yards_gained))
.attr("r", "5")
.attr("fill", "orange")
.attr("stroke-width", "1")
.attr("stroke", "black");

//   // Step 1: Append tooltip div
//   var toolTip = d3.select("body")
//   .append("div")
//   .classed("tooltip", true);

// // Step 2: Create "mouseover" event listener to display tooltip
// circlesGroup2.on("mouseover", function(d) {
//   toolTip.style("display", "block")
//       .html(
//         `<strong>${dateFormatter(d.game_year)}<strong><hr>${d.receiving_yards_gained}
//     yards`)
//       .style("left", d3.event.pageX + "px")
//       .style("top", d3.event.pageY + "px");
// })
//   // Step 3: Create "mouseout" event listener to hide tooltip
//   .on("mouseout", function() {
//     toolTip.style("display", "none");
//   });

// // append circles (rushing)
// var circlesGroup3 = chartGroup.selectAll("circle")
// .data(playerData)
// .enter()
// .append("circle")
// .attr("cx", d => xTimeScale(d.game_year))
// .attr("cy", d => yLinearScale2(d.rushing_yards_gained))
// .attr("r", "5")
// .attr("fill", "orange")
// .attr("stroke-width", "1")
// .attr("stroke", "black");

//   // Step 1: Append tooltip div
//   var toolTip = d3.select("body")
//   .append("div")
//   .classed("tooltip", true);

// // Step 2: Create "mouseover" event listener to display tooltip
// circlesGroup3.on("mouseover", function(d) {
//   toolTip.style("display", "block")
//       .html(
//         `<strong>${dateFormatter(d.game_year)}<strong><hr>${d.rushing_yards_gained}
//     yards`)
//       .style("left", d3.event.pageX + "px")
//       .style("top", d3.event.pageY + "px");
// })
//   // Step 3: Create "mouseout" event listener to hide tooltip
//   .on("mouseout", function() {
//     toolTip.style("display", "none");
//   });

});
