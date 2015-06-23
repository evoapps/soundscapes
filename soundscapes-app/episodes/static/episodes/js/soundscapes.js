var svgWidth = 500,
    svgHeight = 200;

var colorRampScale = d3.scale.ordinal()
  .domain(["StartUp", "Reply All", "Mystery Show"])
  .range(["Blues", "Greens", "Purples"]);

function drawEpisodeList(episodes) {
  globalVars.episodes = episodes;


  // Convert release string to javascript Date
  episodes.forEach(parseEpisode);

  d3.select("#episodeList")
    .selectAll("li.episode")
    .data(episodes)
    .enter()
    .append("li")
    .attr("class", "episode");

  var episodeItems = d3.selectAll("li.episode");

  episodeItems
    .append("svg")
    .attr("width", svgWidth)
    .attr("height", svgHeight)
    .append("g")
    .attr("class", "episode")
    .attr("id", function (episode) { return "episode" + episode.id; })
    .each(drawSegments);

  episodeItems
    .append("h2")
    .append("a")
    .attr("href", function (episode) { return episode.url; })
    .text(function (episode) { return episode.title; })
}

function drawSegments(episode) {

  var line = d3.svg.line(),
      timeScale = d3.scale.linear(),
      valueScale = d3.scale.linear(),
      colorScale = d3.scale.ordinal();

  line
    .x(function (moment) { return timeScale(moment.time); })
    .y(function (moment) { return valueScale(moment.value); })
    .interpolate("basis");

  timeScale
    .domain(d3.extent(episode.moments, function (moment) { return parseFloat(moment.time); }))
    .range([0, svgWidth]);

  valueScale
    .domain(d3.extent(episode.moments, function (moment) { return moment.value; }))
    .range([svgHeight, 0]);

  episode.segments.forEach(addEndMoments);

  d3.select("#episode" + episode.id)
    .selectAll("path.segment")
    .data(episode.segments)
    .enter()
    .append("path")
    .attr("class", "segment")
    .attr("id", function (segment) { return "segment" + segment.id; })
    .attr("d", function (segment) { return line(segment.moments) + "Z"; })
    .on("click", selectSegment)
    .style("fill", function (segment) {
      var ramp = colorRampScale(episode.show.name),
          size = 5;
          hue = 3;  // arbitrarily select the center hue
      return colorbrewer[ramp][size][hue];
    });

  function selectSegment(segment) {
    var episodeGroup = d3.select(this.parentNode);

    if (!episodeGroup.classed("loaded")) {
      loadEpisodeAudioSource(episode);
      return;
    }

    var segmentPath = d3.select(this);

    segmentPath.classed("playing", !segmentPath.classed("playing"));
    if (segmentPath.classed("playing")) {
      episode.playEpisode(segment.start_time);
    } else {
      episode.stopEpisode();
    }
  }

}

function parseEpisode(episode) {
  episode.released = Date.parse(episode.released);
}

function addEndMoments(segment) {
  var firstMoment = {time: segment.start_time, value: 0.0},
      lastMoment = {time: segment.end_time, value: 0.0};
  segment.moments.splice(0, 0, firstMoment);
  segment.moments.push(lastMoment);
}
