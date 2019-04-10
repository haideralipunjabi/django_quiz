var WORD_TYPE      = 'word_type',
    WORD_ORIGIN    = 'word_origin',
    WORD_MEANING   = 'word_meaning',
    WORD_USAGE     = 'word_usage';
var $word_type, $word_origin, $word_meaning, $word_usage, $correct_word;
var clock, ticksound, correctSound, wrongSound, timeEndSound;

function nextQuestion(){
  
  $qid = parseInt(getUrlParameter('qid'));
  openurl('?qid=' + ($qid + 1).toString());
  
}
function previousQuestion(){
  
  $qid = parseInt(getUrlParameter('qid'));
  openurl('?qid=' + ($qid + -1).toString());
  
}

$(document).bind('keypress', 'ctrl+shift+n', function(){
  nextQuestion();
});

$(document).bind('keypress', 'ctrl+shift+b', function(){
  show("content");
});


function loadHints(){
  $word_type = $("#type")[0].innerText;
  $word_origin = $("#origin")[0].innerText;
  $word_meaning = $("#meaning")[0].innerText;
  $word_usage = $("#usage")[0].innerText;
  $correct_word = $("#word")[0].innerText;
  
  $hints = $("#hints_container");
  if($word_type !== ""){
    $hints.append('<div id="word_type" class=" hint_container col-md-3" onclick="showModal(\'word_type\')"><div class="box"><a class="fa fa-list-alt"></a></div></div>');
  }
  if($word_origin !== ""){
    $hints.append('<div id="word_origin" class="hint_container col-md-3" onclick="showModal(\'word_origin\')"><div class="box"><a class="fa fa-chain"></a></div></div>');
  }
  if($word_usage !== ""){
    $hints.append('<div id="word_usage" class="hint_container col-md-3" onclick="showModal(\'word_usage\')"><div class="box"><a class="fa fa-comments-o "></a></div></div>');
  }
  if($word_meaning !== ""){
    $hints.append('<div id="word_meaning" class="hint_container col-md-3" onclick="showModal(\'word_meaning\')"><div class="box"><a class="fa fa-file-text-o"></a></div></div>');
  }
  
  $(".box").click(function(){
    console.log(this);
     if(this.parentElement.id !== "word_meaning" && this.parentElement.id !== "word_usage"){
       $(this).addClass('magictime tinUpOut');
     }
  }
  );
  
}
function loadPronouncitation(){
  $url = $("#audio")[0].innerText;
  console.log($url);
    if($url !== "" && $url !== undefined && $url !== "None"){
      $("#pronunciation").html('<div id="word_pronounciation" class="hint_container col-md-3" onclick="playPronounciation();"><div class="box"><a class="fa fa-volume-up"></a></div></div>');
    }
}

function playPronounciation(){
  $url = $("#audio")[0].innerText;
  sound = new Howl({
    src: [$url],
    autoplay: false,
    loop: false,
    volume: 1
  });  
  sound.play();
}
function showModal(element){
  $(".remodal").css('background', palette.random('500'));
  $title = $("#modal_title");
  $desc = $("#modal_description");
  switch(element){
    case WORD_TYPE:
      $title.html('Type of Word');
      $desc.html($word_type);
      $("#word_type").html('<h2 class="hint_desc">'+$word_type+'</h2>');
      break;
    case WORD_ORIGIN:
      $title.html('Origin of Word');
      $desc.html($word_origin);
      $("#word_origin").html('<h2 class="hint_desc">'+$word_origin+'</h2>');
      
      break;
    case WORD_MEANING:
      $title.html('Meaning of Word');
      $desc.html($word_meaning);
      break;
    case WORD_USAGE:
      $title.html('Usage');
      $desc.html($word_usage.replace($correct_word, "___"));
      break;
  }
  $('#modal_description').attr('hidden','true');
  $('#hints_container').attr('hidden', 'true');

  openurl('#modal');
  
}
$(document).on('opened', '.remodal', function () {
  resize_to_fit();
  $('#modal_description').removeAttr('hidden');
  console.log('Modal is opened');
});
$(document).on('closed', '.remodal', function () {
    $('#hints_container').removeAttr('hidden');
});
function resize_to_fit(){
    var fontsize = $('#modal_description').css('font-size');
    console.log(fontsize);
    $("#modal_description").css('font-size', parseFloat(fontsize) - 1);
    console.log($('#modal_description').height());
    if($('#modal_description').height() >= 500){
        resize_to_fit();
    }
}
$("#word_input").on('input',function() {
  console.log(mapRange(this.value.length, 9,20,80,120));
  if(this.value.length > 9)
  {
    $(this).css('font-size', mapRange(this.value.length, 9,20,90,70) +'px');
    $(this).css('letter-spacing', mapRange(this.value.length, 9,20,30,10) +'px');
  
  }
  console.log('cahnged');
});
function checkWord(){
  $team = $("#current_team")[0].textContent;
  $increment = parseInt($("#increment_val")[0].textContent);
  $decrement = parseInt($("#decrement_val")[0].textContent);
  $quiz_name = $("#quiz_name")[0].textContent;
  console.log($team, $increment, $decrement, $quiz_name);
  $input = $("#word_input")[0].value;
  if($correct_word.toLowerCase() === $input.toLowerCase()){
    switchColor('#64dd17');
    correctSound.play();
    updateScore($increment.toString(), $quiz_name, $team);

  }
  else{
    switchColor('#d50000');
    wrongSound.play();
    updateScore($decrement.toString(), $quiz_name, $team);
  }

}

function switchColor(color){
  $input = $("#word_input");
  $button = $("#check");
  $input.css('color', color);
  $input.css('border', '2px solid ' + color);
  $button.css('background-color', color);
}
function mapRange(n, start1, stop1, start2, stop2) {
  return ((n-start1)/(stop1-start1))*(stop2-start2)+start2;
}

jQuery(document).ready(function($) {
  console.log("Ready");
  time = $("#time").html();
  ticksound = new Howl({
    src: ['/static/media/tick.mp3'],
    autoplay: false,
    loop: true,
    volume: 1
  });
  timeEndSound = new Howl({
    src: ['/static/media/timeEndSound.mp3'],
    autoplay: false,
    loop: false,
    volume: 1
  });
  wrongSound = new Howl({
    src: ['/static/media/wrongSound.mp3'],
    autoplay: false,
    loop: false,
    volume: 1
  });
  correctSound = new Howl({
    src: ['/static/media/correctSound.mp3'],
    autoplay: false,
    loop: false,
    volume: 1
  });
  clock = new FlipClock($('#flipclock'), {
    countdown: true,
    autoStart: false,
    clockFace: 'MinuteCounter',
    callbacks: {
      start: function() {
        console.log('start');
        ticksound.play();
      },
      stop: function() {
        console.log('stop');
        (this.factory.time.time===0) && timeEndSound.play();

        ticksound.stop();
      }
    }

  });
  clock.time.time = time;
});


var toggleClock = function(){
  console.log(clock)
  if(clock.running){
    clock.stop();
  } 
  else
  {
    clock.start();
  } 
};

var teamChange = function(){
  $("#current_team")[0].textContent = $("#teamchange")[0].value;
};
