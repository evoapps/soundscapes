
function updateProgress() {
  var audioElement = document.querySelector("audio");

  currentTime = audioElement.currentTime;
  console.log(timeScale(currentTime));

  d3.select("g")
    .append("circle")
    .attr("cx", timeScale(currentTime))
    .attr("cy", 50)
    .attr("r", 10)
    .style("fill", "black");
}
