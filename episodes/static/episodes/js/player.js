var audioContext = new (window.AudioContext || window.webkitAudioContext)();

function loadEpisodeAudioSource(episode) {
  episode.player = {}

  var request = new XMLHttpRequest();
  request.open('GET', episode.mp3, true);
  request.responseType = 'arraybuffer';

  // Decode asynchronously
  request.onload = function () {
    audioContext.decodeAudioData(request.response,
      function (buffer) {
        episode.player.buffer = buffer;
        var episodeGroup = document.getElementById("episode" + episode.id);
        episodeGroup.classList.add("loaded");
      },
      function (error) { console.log(error); });
  }
  request.send();

  episode.player.play = function (offset) {
    this.source = audioContext.createBufferSource();
    this.source.buffer = episode.player.buffer;
    this.source.connect(audioContext.destination);
    this.source.start(0, offset);

    this.startTime = audioContext.currentTime;
  }

  episode.player.stop = function () {
    this.source.stop();
  };

}
