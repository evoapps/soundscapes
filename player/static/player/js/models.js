// TODO Episodes need a method that will load the episode as
// a sound manager sound that can be played at specific times
// by the EpisodeView
var Episode = Backbone.Model.extend({
  initialize: function () {
    this.on("episode:play", this.playEpisode);
  },
  loadEpisode: function () {
    // Create soundManager object
    this.episodeSound = soundManager.createSound({
      id: "episode" + this.get("id"),
      url: this.get("url"),
      autoLoad: true,
      onload: function () {
        // e.g., this.trigger('episode:loaded')
        console.log("episode " + this.get("id") + " loaded");
      }
    });
  },
  playEpisode: function (start) {
    console.log("playing episode at " + start);
    this.episodeSound.play(start);
  }
});


var EpisodeCollection = Backbone.Collection.extend({
  model: Episode,
  url: '/api/episodes',
  initialize: function () {
    this.on("soundmanager:ready", function () {
      console.log("soundmanager:ready, so loading first episode")
      var firstEpisodeId = this.models[0].id;
      this.trigger("collection:load", firstEpisodeId)
    });

    this.on("collection:load", this.loadEpisode)
  },
  loadEpisode: function (id) {
    console.log("triggering episode:load on the first episode")
    this.get(id).loadEpisode();
  },
});
