
function updateProgress() {
  var audioElement = document.querySelector("audio");

  currentTime = audioElement.currentTime;
  console.log(timeScale(currentTime));

  d3.select("g")
    .append("line")
    .attr("x1", timeScale(currentTime))
    .attr("y1", 0)
    .attr("x2", timeScale(currentTime))
    .attr("y2", d3.max(valueScale.range()))
    .style("stroke", "black");
}

function toggleAudio() {
  var audioElement = document.querySelector("audio");

  if (audioElement.paused) {
    audioElement.play();
  } else {
    audioElement.pause();
  }

}
