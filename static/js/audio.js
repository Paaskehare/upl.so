var audio = $('.player audio:first');
var loadingIndicator = $('.player #loading');
var positionIndicator = $('.player #handle');
var timeleft = $('.player #timeleft');

console.log($(audio));

if ((audio.buffered != undefined) && audio.buffered.length != 0) {
  $(audio).bind('progress', function() {
    var loaded = parseInt(((audio.buffered.end(0) / audio.duration) * 100), 10);
    loadingIndicator.css({width: loaded + '%'});
  });
} else {
  loadingIndicator.remove();
}

$(audio).bind('timeupdate', function() {
  var rem = parseInt(audio.duration - audio.currentTime, 10)
    , pos = (audio.currentTime / audio.duration) * 100
    , mins = Math.floor(rem/60,10)
    , secs = rem - mins * 60;

  timeleft.text('-' + mins + ':' + (secs > 9 ? secs : '0' + secs));
  if (!manualSeek) { positionIndicator.css({left: pos + '%'}); }
  if (!loaded) {
    loaded = true;

    $('.player #gutter').slider({
      value: 0,
      step: 0.01,
      orientation: 'horizontal',
      range: 'min',
      max: audio.duration,
      slide: function() {
        manualSeek = true;
      },
      stop: function(e,ui) {
        manualSeek = false;
        audio.currentTime = ui.value;
      }
    });
  }
  
});

$(audio).bind('play', function() {
  $('#playtoggle').addClass('playing');
}).bind('pause ended', function() {
  $('#playtoggle').removeClass('playing');
});

$('#playtoggle').click(function() {
  console.log('what');
  if (audio.paused) { audio.play(); }
  else { audio.pause(); }
});
