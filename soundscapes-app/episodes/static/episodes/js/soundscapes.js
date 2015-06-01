show_soundscapes = function(episodes) {
  var episodes = JSON.parse(episodes); // don't know why this isn't automatic
  d3.select("#vis")
    .selectAll("div")
      .data(episodes)
    .enter().append("div")
      .text(function(d) { console.log(d); return d.fields.title; });
}
