IMAGE_EXTENSIONS = ['jpg', 'png', 'jpeg'];
VIDEO_EXTENSIONS = ['mp4', 'mkv'];
AUDIO_EXTENSIONS = ['mp3'];

var usedColors = [];
var clock, ticksound, correctSound, wrongSound, timeEndSound;

function getRandomColor() {
  $color = palette.random();
  if (usedColors.includes($color)) {
    $color = getRandomColor();
  }
  usedColors.push($color);
  return $color;
}

function nextQuestion() {

  $qid = parseInt(getUrlParameter('qid'));
  openurl('?qid=' + ($qid + 1).toString());

}

function previousQuestion() {

  $qid = parseInt(getUrlParameter('qid'));
  openurl('?qid=' + ($qid + -1).toString());

}

function loadfromOutbox() {
  usedColors = [];
  $("#content").removeClass("magictime perspectiveDownReturn");
  $("#content").addClass("magictime perspectiveDown");

  $.ajax({
    url: 'http://localhost:8000/api/outbox?quiz_name=' + $("#quiz_name")[0].textContent,
    type: 'GET',
    crossDomain: true,
    dataType: 'json',
    success: function(json) {
      console.log(json);

      //Object {  correct: "Santa Clara", explanation: null }
      $("#media_asset").html(json.media_asset);
      $("#question").html(json.content);
      $($(".options")[0]).html(' ');
      $($(".options")[1]).html(' ');
      $(json.options).each(function(index) {
        list_index = parseInt(index) % 2;

        toAppend = "";
        if (json.options[index] === json.correct) {
          toAppend = '<li><a class="option nohighlight button-icon" style="display:none;" onclick="show(\'correct\')"><span class="option-icon"></span>' + json.options[index] + '</a></li>';
        } else {
          toAppend = '<li><a class="option nohighlight button-icon" style="display:none;" onclick="show(\'wrong\')"><span class="option-icon"></span>' + json.options[index] + '</a></li>';
        }
        console.log(toAppend);
        console.log($(toAppend));
        $($(".options")[list_index]).prepend($(toAppend));
        $option_letter = "";
        $(".option-icon").each(function(index) {
          switch (index) {
            case 0:
              $option_letter = "A";
              break;
            case 1:
              $option_letter = "C";
              break;
            case 2:
              $option_letter = "B";
              break;
            case 3:
              $option_letter = "D";
              break;
          }
          $(this).html($option_letter);
        });
        $("#question").css('display', 'block');
        $("#question").addClass('magictime tinUpIn');
        $(".option").each(function() {
          $(this).css('background-color', getRandomColor());
          $(this).css('display', 'inline-block');
          $(this).addClass('magictime boingInUp');
          $(this).mousedown(function(e) {
            if (e.button == 2) {
              if($(this).hasClass('nohighlight') === true)
              {
              $(this).addClass('highlight');
              $(this).removeClass('nohighlight');  
              }
              else{
                $(this).addClass('nohighlight');
                $(this).removeClass('highlight')
              }
              return false;
            }
            return true;
          });
        });
      });

      setTimeout(function() {
        //$("#content").removeClass("magictime perspectiveDown");
        $("#content").addClass("magictime perspectiveDownReturn");

      }, 2000);

    }
  });
}

$(document).bind('keypress', 'ctrl+shift+n', function() {
  nextQuestion();
});

$(document).bind('keypress', 'ctrl+shift+b', function() {
  show("content");
});


function checkMedia() {
  $media = $("#media_asset");
  if ($media.length === 1) {
    $path = $($media).html();
    $extension = $path.substring($path.lastIndexOf('.') + 1, $path.length);
    if (IMAGE_EXTENSIONS.indexOf($extension) >= 0) {
      $("#media_container").append("<img src='" + $path + "' />");
      $("#question").removeClass('col-md-12');
      $("#question").addClass('col-md-10');
      $(".option_list").each(function() {
        $(this).removeClass('col-md-6');
        $(this).addClass('col-md-5');
      });
    }
    if (VIDEO_EXTENSIONS.indexOf($extension) >= 0) {
      $("#media_container").append("<video width='320' height='240' controls> <source src='" + $path + "' ></video>");
    }
    if (AUDIO_EXTENSIONS.indexOf($extension) >= 0) {
      $("#media_container").append("<audio controls> <source src='" + $path + "' ></audio>");
    }

  }
}
var show = function show(element) {
  clock.stop();
  var CORRECT = "correct",
    WRONG = "wrong",
    CONTENT = "content",
    EXPLANATION = "explanation";

  $correct = $("#correct");
  $wrong = $("#wrong");
  $content = $("#content");
  $teams = $("#teams")[0].textContent.split(',');
  $team = $("#current_team")[0].textContent;
  $increment = parseInt($("#increment_val")[0].textContent);
  $decrement = parseInt($("#decrement_val")[0].textContent);
  $quiz_name = $("#quiz_name")[0].textContent;
  $explanation = $("#explanation")[0].textContent;
  $title = $("#modal_title");
  $desc = $("#modal_description");
  $correct_answer = $('a[onclick^="show(\'correct\')"]').html();
  switch (element) {
    case CORRECT:
      $title.html('');
      $desc.html('CORRECT');
      $(".remodal").css('background', palette.get('Green', '500'));
      updateScore($increment.toString(), $quiz_name, $team);
      correctSound.play();
      break;
    case WRONG:
      $title.html('');
      $desc.html('WRONG');
      $(".remodal").css('background', palette.get('Red', '500'));
      updateScore($decrement.toString(), $quiz_name, $team);
      wrongSound.play();
      break;
    case EXPLANATION:
      $title.html($correct_answer);
      $desc.html($explanation);
      $(".remodal").css('background', palette.random('500'));
      break;
    default:
      break;
  }
  openurl('#modal');
  $('#modal_description').attr('hidden', 'true');


  /*
   switch(element){
   case CORRECT:
   if($correct.css("display") === "none"){
   $content.css("display", "none");
   $wrong.css("display", "none");
   $explanation.css("display", "none");
   $correct.css("display", "block");
   updateScore($increment.toString(), $quiz_name, $team);
   }
   else{
   $correct.css("display", "none");
   $wrong.css("display", "none");
   $explanation.css("display", "none");
   $content.css("display", "block");
   }
   break;
   case WRONG:
   if($wrong.css("display") === "none"){
   $content.css("display", "none");
   $correct.css("display", "none");
   $explanation.css("display", "none");
   $wrong.css("display", "block");
   updateScore($decrement.toString(), $quiz_name, $team);
   }
   else{
   $wrong.css("display", "none");
   $correct.css("display", "none");
   $explanation.css("display", "none");
   $content.css("display", "block");
   }
   break;
   case EXPLANATION:
   if($explanation.css("display") === "none"){
   $content.css("display", "none");
   $correct.css("display", "none");
   $wrong.css("display", "none");
   $explanation.css("display", "block");
   }
   else{
   $wrong.css("display", "none");
   $correct.css("display", "none");
   $explanation.css("display", "none");
   $content.css("display", "block");
   }
   break;
   case CONTENT:
   if($content.css("display") === "none"){
   $correct.css("display", "none");
   $wrong.css("display", "none");
   $explanation.css("display", "none");
   $content.css("display", "block");
   }
   break;
   default:
   break;
   }

   */
};
$(document).on('opened', '.remodal', function() {
  $("#flipclock").css('display', 'none');
  resize_to_fit();
  $('#modal_description').removeAttr('hidden');
  console.log('Modal is opened');
});
$(document).on('closed', '.remodal', function() {
  $("#flipclock").css('display', 'block');
  $("#modal_description").css('font-size', '100px');
});

function resize_to_fit() {
  var fontsize = $('#modal_description').css('font-size');
  console.log(fontsize);
  $("#modal_description").css('font-size', parseFloat(fontsize) - 1);
  console.log($('#modal_description').height());
  if ($('#modal_description').height() >= 500) {
    resize_to_fit();
  }
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
        console.log(this);
        ticksound.stop();
        (this.factory.time.time===0) && timeEndSound.play();
      }
    }

  });
  clock.time.time = time;


  //icons
  $option_letter = "";
  $(".option-icon").each(function(index) {
    // switch ($quiz_name.toLowerCase()) {
    //   case "chemistry":
    //     $icon_class = "fa-flask";
    //     break;
    //   case "physics":
    //     $icon_class = "fa-lightbulb-o";
    //     break;
    //   case "computers":
    //     $icon_class = "fa-code";
    //     break;
    //   case "inventions":
    //     $icon_class = "fa-book";
    //     break;
    //   case "biology":
    //     $icon_class = "fa-heartbeat";
    //     break;
    //   case "logical reasoning":
    //     $icon_class = "fa-cubes";
    //     break;
    //   case "current affairs":
    //     $icon_class = "fa-globe";
    //     break;
    //   default:
    // }
    // $(this).addClass("fa " + $icon_class);
    switch (index) {
      case 0:
        $option_letter = "A";
        break;
      case 1:
        $option_letter = "C";
        break;
      case 2:
        $option_letter = "B";
        break;
      case 3:
        $option_letter = "D";
        break;
    }
    $(this).html($option_letter);
  });
  document.oncontextmenu = function() {
    return false;
  };
  $("#question").css('display', 'block');
  $("#question").addClass('magictime tinUpIn');
  $(".option").each(function() {
    $(this).css('background-color', getRandomColor());
    $(this).css('display', 'inline-block');
    $(this).addClass('magictime boingInUp');
        $(this).mousedown(function(e) {
          if (e.button == 2) {
            if($(this).hasClass('nohighlight') === true)
            {
            $(this).addClass('highlight');
            $(this).removeClass('nohighlight');  
            }
            else{
              $(this).addClass('nohighlight');
              $(this).removeClass('highlight')
            }
            return false;
          }
          return true;
        });
      
    
  });


});


var toggleClock = function() {
  console.log('called');
  if (clock.running) {
    clock.stop();
  } else {
    clock.start();
  }
};

var teamChange = function() {
  $("#current_team")[0].textContent = $("#teamchange")[0].value;
};
Array.prototype.getRandom = function(num, cut) {
  var A = cut ? this : this.slice(0);
  A.sort(function() {
    return .5 - Math.random();
  });
  return A.splice(0, num);
}

var highlightCorrect = function(){
  $team = $("#current_team")[0].textContent;
  $increment = parseInt($("#increment_val")[0].textContent);
  $decrement = parseInt($("#decrement_val")[0].textContent);
  $quiz_name = $("#quiz_name")[0].textContent;
  $correct_answer = $('a[onclick^="show(\'correct\')"]');
  if($correct_answer.hasClass('highlight')){
    updateScore($increment.toString(), $quiz_name, $team);
  }
  else{
      $(".highlight").addClass("wrong");
      $(".highlight").removeClass("highlight");
    
    updateScore($decrement.toString(), $quiz_name, $team);
    
  }
  $correct_answer.addClass('correct');
  $correct_answer.removeClass('highlight');
  $correct_answer.removeClass('nohighlight');

  
}
var fifty_fifty = function() {
  $correct_answer = $('a[onclick^="show(\'correct\')"]').html();

  array = [0, 1, 2, 3];
  $(".option").each(function(index) {
    if (this.innerHTML === $correct_answer) {
      array.splice(array.indexOf(index), 1);
    }
  });
  toRemove = array.getRandom(2, false);
  $(toRemove).each(function() {
    console.log(this)
    $($(".option")[this]).addClass('magictime boingOutDown');
  });


};
