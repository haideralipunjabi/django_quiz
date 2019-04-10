function openurl(url) {
  window.open(url, "_self");
}

function nextTeam() {
  $last_team = $("#last_team").html();
  if ($last_team != 'True') {
    url = "/team/?team=next&current=" + $(".team_name").html();
    window.open(url, "_self");
  } else {

    url = "/quiz";
    window.open(url, "_self");
  }
}

var getUrlParameter = function getUrlParameter(sParam) {
  var sPageURL = decodeURIComponent(window.location.search.substring(1)),
    sURLVariables = sPageURL.split('&'),
    sParameterName,
    i;

  for (i = 0; i < sURLVariables.length; i++) {
    sParameterName = sURLVariables[i].split('=');

    if (sParameterName[0] === sParam) {
      return sParameterName[1] === undefined ? true : sParameterName[1];
    }
  }
};

function storeScore(score, quiz, team) {
  score = parseInt(getScore(quiz, team)) + parseInt(score);
  $.cookie(quiz + "_" + team, score.toString());
}

function getScore(quiz, team) {
  return $.cookie(quiz + "_" + team);
}

function clearScore(quiz, team) {
  $.cookie(quiz + "_" + team, '0');
}
function getCookie(c_name)
{
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
 }
function updateScore(score, quiz, team) {
  var $csrf_token = $('[name="csrfmiddlewaretoken"]').attr('value');
  console.log('update_Started');
  scoreData = {
    'team': team,
    'quiz': quiz,
    'score': score
  };
  // scoreData.team = team;
  // scoreData.quiz = quiz;
  // scoreData.score = score;  
  // scoreData = JSON.stringify(scoreData);
  console.log("TESTING", JSON.stringify(scoreData));
  $.ajax({
    url: '/api/score/',
    headers : { "X-CSRFToken" : getCookie("csrftoken" ) },
    type: 'POST',
    data: scoreData,
    success: function(json) {
      console.log("Update success");
    },
    error: function(json) {
      console.log("Update Failed");
    }
  });
}

var randomSelection = function randomSelection() {
  $array = $(".quiz_list li");
  $length = $array.length;
  $index = $length;
  $animation = setInterval(function() {
    $($($array[Math.floor(($index - 1) % $length)]).children()[0]).removeClass("selected");
    $($($array[Math.floor($index % $length)]).children()[0]).addClass("selected");
    $index = $index + 1;
    if ($index > 50) {

      clearInterval($animation);
      $number = Math.floor((Math.random() * $length));
      $($array).each(function(index) {
        $($(this).children()[0]).removeClass("selected");
      });
      $($($array[$number]).children()[0]).addClass("selected");

    }
  }, 200);
};
$(document).bind('keypress', 'ctrl+shift+v', function() {
  openurl('/quiz');
  console.log('home');
});

function hexToRgb(hex, alpha) {
  var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  var obj =  result ? {
    r: parseInt(result[1], 16),
    g: parseInt(result[2], 16),
    b: parseInt(result[3], 16)
  } : null;
  if(alpha === undefined){
    return "rgba(" + obj.r +',' + obj.g + ',' + obj.b + ',1)';
  }
  else{
    return "rgba(" + obj.r +',' + obj.g + ',' + obj.b + ','+alpha.toString()+')';
  }
}


// Navigation Bar
function loadNavBar(callback){
  $("#navbar").load('/navigation',function(){
    callback();
  });
  $top = $(window).height() - 10;
  console.log($top);
  $("#navbar").css('top', $top.toString() );
  $("#navbar").css('opacity', '0');
  $("#navbar").hover(
    function(){
      //Mouse IN
      $(this).animate({
        opacity: 100
      }, 200);
    },
    function(){
      //Mouse Out
      $(this).animate({
        opacity: 0
      }, 200);
    
    });
  }
  function mapRange(n, start1, stop1, start2, stop2) {
    return ((n-start1)/(stop1-start1))*(stop2-start2)+start2;
  }
