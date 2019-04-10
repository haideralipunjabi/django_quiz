var bar, timer, remainingTime = timer_time, ticksound, timeEndSound;

function Interval(fn, time) {
    var t = false;
    var timer_;
    this.start = function () {
        if (!this.isRunning())
            {
              timer_ = setInterval(fn, time);
              ticksound.play();
              t = true;
    }
  };
    this.stop = function () {
      ticksound.stop();
      clearInterval(timer_);
        //remainingTime = timer_time;
        t = false;
    };
    this.isRunning = function () {
        return t !== false;
    };
}




$(window).on('load',function(){

  //Progress Bar
  bar = new ProgressBar.Circle('#timer', {
  color: '#000',
  strokeWidth: 6,
  trailWidth: 1,
  easing: 'easeInOut',
  duration: 1000,
  text: {
    autoStyleContainer: false
  },
  from: { color: '#f00', width: 1 },
  to: { color: '#0f0', width: 4 },
  // Set default step function for all animate calls
  step: function(state, circle) {
    circle.path.setAttribute('stroke', state.color);
    circle.path.setAttribute('stroke-width', state.width);

    var value = Math.round(circle.value() * 100);
    if (value === 0) {
      circle.setText('');
    } else {
      circle.setText(remainingTime);
    }

  }
});
  console.log(bar);
bar.text.style.fontFamily = '"Raleway", Helvetica, sans-serif';
bar.text.style.color = "#fff";
bar.text.style.fontSize = '8rem';

bar.animate(mapRange(timer_time, 0,timer_time,0,1));  // Number from 0.0 to 1.0

});
$("#timer").on('click', function(){
  startQuiz();
});
function startTimer(){
  timer = new Interval(function(){
    if(remainingTime > 0 && timer.isRunning)
    {
      console.log(remainingTime)
      remainingTime -= 1;
      bar.animate(mapRange(remainingTime, 0,timer_time,0,1));
    }
    else{
      stopTimer()
      timeEndSound.play()
    }
    
  }, 1000);
  timer.start();
}

function stopTimer(){
  $("#question").html(' ');
  timer.stop();

}

function startQuiz(){
  if(timer === undefined || !timer.isRunning()){
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
    startTimer();
    loadQuestion();
  }
}

function loadQuestion(){
  console.log(questions)
  if(timer.isRunning()){
    if(questions.length > 0){
      $("#question").html(questions.pop());
    }
    else{
      stopTimer();
    }  
  }
}

function correct(){
  if(timer.isRunning()){
    
  
  loadQuestion();
  $team = getUrlParameter('team');
  console.log($team);
  $increment = parseInt($("#increment_val")[0].textContent);
  $decrement = parseInt($("#decrement_val")[0].textContent);
  $quiz_name = $("#quiz_name")[0].textContent;  
  score("tick");
  updateScore($increment.toString(),$quiz_name, $team);
}
}
function wrong(){
  if(timer.isRunning()){
    
  
  loadQuestion();
  $team = getUrlParameter('team');
  $increment = parseInt($("#increment_val")[0].textContent);
  $decrement = parseInt($("#decrement_val")[0].textContent);
  $quiz_name = $("#quiz_name")[0].textContent;  
  score("cross");
  updateScore($decrement.toString(),$quiz_name, $team);
}
}
function score(item){
  $scorer = $("#scorer");
  $tick = $('<button><span class="fa fa-check"></span</button>');
  $cross = $('<button><span class="fa fa-times"></span</button>');
  if(item === "tick"){
    $scorer.append($tick);
  }
  if(item === "cross"){
    $scorer.append($cross);
  }
  return 0;
}
