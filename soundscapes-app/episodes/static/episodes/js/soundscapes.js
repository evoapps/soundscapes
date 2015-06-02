

show_soundscapes = function(episodes) {
  var episodes = JSON.parse(episodes); // don't know why this isn't automatic

  var numEpisodes = episodes.length,
      perEpisodeHeight = 30;

  var svgWidth = 700,
      svgHeight = perEpisodeHeight * (numEpisodes + 1);

  d3.select("#vis")
    .append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight)

  d3.select("svg")
    .selectAll("g")
    .data(episodes)
    .enter()
    .append("g")
    .attr("class", "episode")

  d3.selectAll("g.episode")
    .append("text")
    .attr("y", function(ep, i) { return perEpisodeHeight * (i + 1); })
    .text(function(ep) { console.log(ep); return ep.fields.title; });
}
