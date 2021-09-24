var module = angular.module('myApp',[]);

function Main($scope,$http, $compile){

  $http.get("/idchart/").then( function(response) {
       $scope.data = response.data;

Chart.defaults.global.defaultFontFamily = 'Nunito', '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#858796';

function number_format(number, decimals, dec_point, thousands_sep) {
  // *     example: number_format(1234.56, 2, ',', ' ');
  // *     return: '1 234,56'
  number = (number + '').replace(',', '').replace(' ', '');
  var n = !isFinite(+number) ? 0 : +number,
    prec = !isFinite(+decimals) ? 0 : Math.abs(decimals),
    sep = (typeof thousands_sep === 'undefined') ? ',' : thousands_sep,
    dec = (typeof dec_point === 'undefined') ? '.' : dec_point,
    s = '',
    toFixedFix = function(n, prec) {
      var k = Math.pow(10, prec);
      return '' + Math.round(n * k) / k;
    };
  // Fix for IE parseFloat(0.55).toFixed(0) = 0;
  s = (prec ? toFixedFix(n, prec) : '' + Math.round(n)).split('.');
  if (s[0].length > 3) {
    s[0] = s[0].replace(/\B(?=(?:\d{3})+(?!\d))/g, sep);
  }
  if ((s[1] || '').length < prec) {
    s[1] = s[1] || '';
    s[1] += new Array(prec - s[1].length + 1).join('0');
  }
  return s.join(dec);
}

// Bar Chart Example
var xaxis1_data = $scope.data.x1;
var yaxis1_data = $scope.data.y1;
var ctx2 = document.getElementById("myBarChart2");
var myBarChart2 = {
  type: 'line',
  data: {
    labels: $scope.data.x1,
    datasets: [{
      label: "Water Output: ",
      backgroundColor: "#4e73df",
      hoverBackgroundColor: "blue",
      borderColor: "#4e73df",
      // barPercentage: 0.25,
      // barThickness: 5,
      // axBarThickness: 3,
      data: $scope.data.y2,
    }],
  },

  options: {
    maintainAspectRatio: false,
    // cornerRadius: 50,
    layout: {
      padding: {
        left: 10,
        right: 25,
        top: 25,
        bottom: 0
      }
    },

    scales: {
      xAxes: [{
   
        scaleLabel: {
            display: true,
            labelString: 'Time',
            fontColor: "#4e73df",
            fontStyle: "bold",
            // barPercentage: 0.2
          },

        gridLines: {
          display: false,
          drawBorder: false
        },
        ticks: {
          maxTicksLimit: 14

        },
        maxBarThickness: 25,
      }],
      yAxes: [{
        ticks: {
          beginAtZero:true,
          maxTicksLimit: 10,
          padding: 1,
          // Include a dollar sign in the ticks
          callback: function(value, index, values) {
            return  number_format(value);
          }
        },

        scaleLabel: {
            display: true,
            labelString: 'Liters Per Hour',
            fontColor: "#4e73df",
            fontStyle: "bold"
          },

        gridLines: {
          color: "rgb(234, 236, 244)",
          zeroLineColor: "rgb(234, 236, 244)",
          drawBorder: false,
          borderDash: [2],
          zeroLineBorderDash: [2]
        }
      }],
    },
    legend: {
      display: false,
    },
    tooltips: {
      titleMarginBottom: 10,
      titleFontColor: '#6e707e',
      titleFontSize: 14,
      backgroundColor: "rgb(255,255,255)",
      bodyFontColor: "#858796",
      borderColor: '#dddfeb',
      borderWidth: 1,
      xPadding: 15,
      yPadding: 15,
      displayColors: false,
      caretPadding: 10,
      callbacks: {
        label: function(tooltipItem, chart) {
          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
          return datasetLabel + number_format(tooltipItem.yLabel) + ' LPH' ;
        }
      }
    },
  }
};

 var myChartData2 = new Chart(ctx2, myBarChart2);
    $("#ab").click(function() {
      var data = myChartData2.config.data;
      var options = myChartData2.config.options;
      data.datasets[0].label = "Power: ";
      data.datasets[0].data = yaxis1_data;
      data.datasets[0].backgroundColor =  "#5cb85c";  
      data.datasets[0].hoverBackgroundColor =  "green";
      options.tooltips.callbacks = {
        label: function(tooltipItem, chart) {
          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
          return datasetLabel + Number(tooltipItem.yLabel).toFixed(2) + ' Watts' ;
        }
      };
      options.scales.yAxes[0].scaleLabel = {
            display: true,
            labelString: 'Power in Watts',
            fontColor: "#5cb85c",
            fontStyle: "bold"
          };
      options.scales.xAxes[0].scaleLabel = {
            display: true,
            labelString: 'Time',
            fontColor: "#5cb85c",
            fontStyle: "bold"
          };
      data.labels = $scope.data.x1;
      myChartData2.update();
    });

    $("#cd").click(function() {
      var yaxis1_data = $scope.data.y2;
      var data = myChartData2.config.data;
      var options = myChartData2.config.options;
      data.datasets[0].label = "Water Output: ";
      data.datasets[0].data = yaxis1_data;
      data.datasets[0].backgroundColor =  "#4e73df";
      data.datasets[0].hoverBackgroundColor =  "blue";
      options.tooltips.callbacks = {
        label: function(tooltipItem, chart) {
          var datasetLabel = chart.datasets[tooltipItem.datasetIndex].label || '';
          return datasetLabel + number_format(tooltipItem.yLabel) + ' LPH' ;
        }
      };
      options.scales.yAxes[0].scaleLabel = {
            display: true,
            labelString: 'Liters Per Hour',
            fontColor: "#4e73df",
            fontStyle: "bold"
          };

        options.scales.xAxes[0].scaleLabel = {
            display: true,
            labelString: 'Time',
            fontColor: "#4e73df",
            fontStyle: "bold"
          };
      data.labels = $scope.data.x1;
      myChartData2.update();
    });

  })
}

module.controller("MainCtrl",Main); 
