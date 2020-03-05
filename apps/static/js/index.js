let get_input_coefficients = function() {
    let term = $("textarea#term").val()
    return {"term": term} 
};

let send_coefficient_json = function(coefficients) {
    $.ajax({
        url: "/solve",
        contentType: "application/json; charset=utf-8",
        type: "POST",
        success: function (data) {
            display_graph(data);
        },
        data: JSON.stringify(coefficients)
    });
};

let display_graph = function(solutions) {
    window.chart.data.datasets[0].data = [];
    window.chart.data.datasets[0].pointBackgroundColor = [];

    for (item of solutions.results) {
        window.chart.data.datasets[0].data.push(item[0]);
        window.chart.data.datasets[0].pointBackgroundColor.push(item[1]);
    }
    window.chart.update();
};

$(document).ready(() => {
    $("button#solve").click(function(e) {
        // This prevents page full-refresh
        e.preventDefault();

        let coefficients = get_input_coefficients();
        send_coefficient_json(coefficients);
    });

    var ctx = $("canvas#result-chart");
    window.chart = new Chart(ctx, {
        type: "scatter",
        data: {
            datasets: [{
                label: "Scatter Dataset",
                data: [
                    {
                        x: 0,
                        y: 5
                    },
                    {
                        x: 1,
                        y: 5
                    },
                    {
                        x: 2,
                        y: 5
                    },
                    {
                        x: 3,
                        y: 5
                    },
                    {
                        x: 4,
                        y: 5
                    }
                ],
                showLines: false,
                pointBackgroundColor: ['#C7FEDD','#DFEEB9','#F2DE97','#FAA181','#F77B7E'],
                pointRadius: 10,
                borderSkipped: true
            }]
        },
        options: {
            backgroundColor:'rgb(40,10,20)',
            scales: {
                xAxes: [{
                    offset: true,
                    ticks: {
                        max: 5,
                        suggestedMin: -1,
                        suggestedMax: 5,
                    }
                }],
                yAxes: [{
                    offset: true,
                    ticks: {
                        suggestedMin: 1,
                        suggestedMax: 8
                    }
                }]
            }
        }
    });
});