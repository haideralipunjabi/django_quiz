var int_team_score_changes = {};
var graph_dataset = [];
var chart_data= {};
var animate_index = 0;
var usedColors = [];
var animate = true;
function animScore() {
    $(".score").each(function (index) {
        var numAnim = new CountUp(this, 0, parseInt(this.textContent));
        setInterval(function () {
            numAnim.start();
        }, 1000);

    });
}
function getRandomColor() {
    $color = palette.random();
    if(usedColors.length === 17){
      usedColors = [];
    }
    if (usedColors.includes($color)) {
        $color = getRandomColor();
    }
    usedColors.push($color);
    return $color;
}

scores = {
  "Albert Einstein" : {
    "Spelling Bee": "4",
    "Computers": "4"
  },
  "Nikola Tesla" : {
    "Spelling Bee": "4",
    "Computers": "4"
  },
  
}

function loadData() {
    $.ajax({
        url: 'http://localhost:8000/api/score/?format=json',
        type: 'GET',
        crossDomain: true,
        dataType: 'json',
        success: function (json) {
            $(json.scores).each(function (index) {
              chart_data.labels = [];
              chart_data.datasets =[];
                for (var team in this) {
                    
                    $team = this[team];
                    team_dataset = {
                      borderWidth: 3
                    };
                    team_dataset.label = team;
                    color = getRandomColor();
                    team_dataset.backgroundColor = hexToRgb(color, 0.5);
                    team_dataset.borderColor = hexToRgb(color);
                    team_dataset.data = [];
                    for (var quiz in $team) {
                      if(!chart_data.labels.includes(quiz)){
                        chart_data.labels.push(quiz);
                        
                      }
                        team_dataset.data.push($team[quiz]);
                    }
                    chart_data.datasets.push(team_dataset);
                    //chart_dataset.push(quiz_data);
                }
            });

            $(json.team_score_change).each(function (index) {
                for (var key in this) {
                    data = [];
                    strarray = this[key].split(',');
                    var sum = 0;
                    for (var score in strarray) {
                        sum += parseInt(strarray[score])
                      console.log('In data', data.sum(), strarray[score]);
                        data.push(sum);
                    }
                    graph_data = {
                        borderWidth: '10',
                        lineTension: 0,
                        borderColor: hexToRgb(getRandomColor()),
                        fill: false,
                        pointColor: "rgba(220,220,220,1)",
                        pointStrokeColor: "#fff",
                        pointHighlightFill: "#fff",
                        pointHighlightStroke: "rgba(220,220,220,1)"
                    };
                    graph_data.label = key;
                    graph_data.data = data;
                    graph_dataset.push(graph_data);
                    int_team_score_changes[key] = data;
                }
                // if(getUrlParameter('type') === 'bar'){
                //   createBarGraphs();
                // }
                // else{
                //   createGraph();
                //
                // }
                $one = $("#drawing_area");
                $two = $("#drawing_area_2");
                $two.addClass('hidden');

                createRadarGraph();
                createGraph();
                setInterval(function () {
                  if(animate){
                    if(animate_index === 0){
                      $one.removeClass('bounceInDown');
                      $two.removeClass('bounceOutUp hidden');
                      $two.addClass('bounceInDown');
                      $one.addClass('bounceOutUp hidden');
                      animate_index=1;
                    }
                    else{
                      $two.removeClass('bounceInDown');
                       $one.removeClass('bounceOutUp hidden');
                        $one.addClass('bounceInDown');
                        $two.addClass('bounceOutUp hidden');
                        animate_index=0;
                      }
                  }
                
                
                }, 5000);
            });
        }
    });
}
function toggleAnimation() {
    $toggle = $("#toggleAnim");
    if (animate) {
        animate = false;
        //show play
        $toggle.removeClass('fa-pause');
        $toggle.addClass('fa-play');
    }
    else {
        animate = true;
        $toggle.removeClass('fa-play');
        $toggle.addClass('fa-pause');
    }
}
function createGraph() {
    $("#drawing_area").append('<canvas id="myChart" width="400px" height="400px"></canvas>');
    $canvas = $("#myChart");
    console.log("GRaph Dataset", graph_dataset);
    labels = [];
    max_label = 0;
    gridLineData=[]
    $(graph_dataset).each(function () {
        if (this.data.length > max_label) max_label = this.data.length;
    });
    for (i = 0; i < max_label; i++) {
        labels.push(i);
        gridLineData[i]="rgba(0,0,0,0.1)"

    }
    $(graph_dataset).each(function () {
        if(this.data.length>2) gridLineData[this.data.length-2] = "rgba(0,0,0,1)"
    });
    var data = {
        labels: labels,
        datasets: graph_dataset
    };
    var options = {
        maintainAspectRatio: false,
         scales: {
             xAxes: [{
                 gridLines: {
                    color: gridLineData
                 }
             }]
         }
    };
    var lineChart = new Chart($canvas, {
        type: 'line',
        data: data,
        options: options
    });

}

function createRadarGraph(){
  $("#drawing_area_2").append('<div class="col-md-6"><canvas id="radarChart" width="400px" height="400px"></canvas></div>');
  $canvas = $("#radarChart");
  var myRadarChart = new Chart($canvas, {
    type: 'radar',
    data: chart_data,
    options: {
      legend:{
        labels: {
          fontSize: 20
        }
      },
      scale: {
        gridLines: {
            lineWidth: 5
         },
          ticks: {
            beginAtZero: true
          },
          pointLabels: {
            fontSize: 20
          },
        }
    }
});
}
function createBarGraphs() {
        $("#drawing_area_2").append('<div class="col-md-6"><canvas id="radarChart" width="400px" height="400px"></canvas></div>');
        $canvas = $("#radarChart");

        var myBarChart = new Chart($canvas, {
            type: 'bar',
            data: bar_rounds[data],
            options: {
                maintainAspectRatio: false
            }
        });
}
Array.prototype.sum = function(){
  if (this.length > 0){
  sum = 0;
  arr = this;
  $(this).each(function(index,value){
    console.log(value);
    sum += parseInt(value);
  });
  
  return sum;
}
return 0;
};
