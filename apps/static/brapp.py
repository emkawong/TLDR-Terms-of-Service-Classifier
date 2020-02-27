from browser import document, ajax
import json

def get_input_coefficients():
    a = document['a'].value
    b = document['b'].value
    c = document['c'].value

    return {'a': int(a),
            'b': int(b),
            'c': int(c)}

def display_solutions(req):
    result = json.loads(req.text)
    # note the syntax for setting the child text of an element
    document['solution'].html = f"{result['root_1']} and {result['root_2']}"

def send_coefficient_json(coefficients):
    req = ajax.Ajax()
    req.bind('complete', display_solutions)
    req.open('POST',
                '/solve',
                True)
    req.set_header('Content-Type', 'application/json')
    req.send(json.dumps(coefficients))

def click(event):
    coefficients = get_input_coefficients()
    send_coefficient_json(coefficients)

document['solve'].bind('click', click)
