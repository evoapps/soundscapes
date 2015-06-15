
function drawEpisodeList(episodes) {
  globalVars.episodes = episodes;

  // Convert release string to javascript Date
  episodes.forEach(function (ep) {
    ep.released = Date.parse(ep.released);
  });

  d3.select("#episodeList")
    .selectAll("div.episode")
    .data(episodes)
    .enter()
    .append("div")
    .attr("class", "episode");

  var episodeDivs = d3.selectAll("div.episode");

  episodeDivs.append("h2")
    .append("a")
    .attr("href", function (ep) { return ep.url; })
    .text(function (ep) { return ep.title; });
}

function drawSegments(episode) {
  // don't know if this is going to be a single object or an array
  globalVars.episode = episode;
}
