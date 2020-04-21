let get_input_coefficients = function() {
    let term = $("textarea#term").val()
    return {"term": term} 
};

/* 
    Takes a string phrase and breaks it into separate phrases 
    no bigger than 'maxwidth', breaks are made at complete words.
    NOTE: Found from internet
*/
function formatLabel(str, maxwidth){
    var sections = [];
    var words = str.split(" ");
    var temp = "";

    words.forEach(function(item, index){
        if(temp.length > 0)
        {
            var concat = temp + ' ' + item;

            if(concat.length > maxwidth){
                sections.push(temp);
                temp = "";
            }
            else{
                if(index == (words.length-1))
                {
                    sections.push(concat);
                    return;
                }
                else{
                    temp = concat;
                    return;
                }
            }
        }

        if(index == (words.length-1))
        {
            sections.push(item);
            return;
        }

        if(item.length < maxwidth) {
            temp = item;
        }
        else {
            sections.push(item);
        }

    });

    return sections;
}

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
    window.chart.data.labels = []
    window.chart.data.datasets[0].pointBackgroundColor = [];

    for (item of solutions.results) {
        var super_long_string = `You irrevocably grant us perpetual and unlimited permission to reproduce, distribute, create derivative works of, modify, publicly perform (including on a through-to-the-audience basis), communicate to the public, make available, publicly display, and otherwise use and exploit the Feedback and derivatives thereof for any purpose and without restriction, free of charge and without attribution of any kind, including by making, using, selling, offering for sale, importing, and promoting commercial products and services that incorporate or embody Feedback, whether in whole or in part, and whether as provided or as modified.`;
        // Replace this with data from the server
        window.chart.data.labels.push(super_long_string);
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
            labels: [],
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
            }],
        },
        options: {
            tooltips: {
                callbacks: {
                    label: function(tooltipItem, data) {
                        var label = data.labels[tooltipItem.datasetIndex];

                        if (!label) return 'TLDR';

                        var chartWidth = $('#result-chart').width();
                        // Divide by 6 seems to map the ratio of the width
                        // of the pixels to the number of letters that fit on the screen.
                        var maxNumLetters = Math.round(chartWidth / 6) - 1;

                        // letters split into an array of letters based on what is
                        // likely to fit on a screen.
                        // Can be broken by overridden font size, etc.
                        label = formatLabel(label, maxNumLetters);

                        return label;
                    }
                }
            },
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