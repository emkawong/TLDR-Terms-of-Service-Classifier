let get_input_coefficients = function() {
    let term_gen = $("textarea#term_gen").val()
    return {"term_gen": term_gen} 
};

let send_coefficient_json = function(coefficients) {
    $.ajax({
        url: "/solve_gen",
        contentType: "application/json; charset=utf-8",
        type: "POST",
        success: function (data) {
            display_solutions(data);
        },
        data: JSON.stringify(coefficients)
    });
};

let display_solutions = function(solutions) {
    $("span#solution").html(solutions.generation)
};

$(document).ready(function() {

    $("button#solve_gen").click(function(e) {
        // This prevents page full-refresh
        e.preventDefault();

        let coefficients = get_input_coefficients();
        send_coefficient_json(coefficients);
    })

})