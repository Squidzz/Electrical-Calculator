from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    calculation_type = request.form.get('calculation')
    value1 = float(request.form.get('value1', 0))
    value2 = float(request.form.get('value2', 0))
    result = ""

    if calculation_type == 'resistance':
        result = f"Resistance: {round(value1 / value2, 2)} Ohms" if value2 != 0 else "Error: Division by zero"
    elif calculation_type == 'voltage':
        result = f"Voltage: {round(value1 * value2, 2)} Volts"
    elif calculation_type == 'current':
        result = f"Current: {round(value1 / value2, 2)} Amps" if value2 != 0 else "Error: Division by zero"
    elif calculation_type == 'power':
        result = f"Power: {round(value1 * value2, 2)} Watts"
    elif calculation_type == 'frequency':
        result = f"Frequency: {round(1 / value1, 2)} Hertz" if value1 != 0 else "Error: Division by zero"
    elif calculation_type == 'impedance':
        result = f"Impedance: {round((value1**2 + value2**2)**0.5, 2)} Ohms"
    else:
        result = "Invalid calculation"

    return render_template('result.html', result=result)

@app.route('/devices', methods=['POST'])
def devices():
    # Log all submitted form data for debugging
    print("Full form data:", request.form)

    # Retrieve device and circuit types
    device_type = request.form.get('device')
    circuit_type = request.form.get('circuit')

    # Safely retrieve and process 'values[]'
    try:
        values = [float(value) for value in request.form.getlist('values[]') if value.strip()]
    except ValueError:
        # Handle non-numeric values gracefully
        return render_template('result.html', result="Error: Invalid values submitted.")

    # Check if there are no values
    if not values:
        return render_template('result.html', result="Error: No values submitted for calculation.")

    # Calculate results based on the device type
    if device_type == 'resistor':
        result = calculate_resistor(circuit_type, values)
    elif device_type == 'capacitor':
        result = calculate_capacitor(circuit_type, values)
    elif device_type == 'inductor':
        result = calculate_inductor(circuit_type, values)
    else:
        result = "Invalid device"

    return render_template('result.html', result=result)



def calculate_resistor(circuit_type, values):
    if not values:
        return "Error: No values provided"
    if circuit_type == 'series':
        return f"Total Resistance: {sum(values)} Ohms"
    elif circuit_type == 'parallel':
        try:
            return f"Total Resistance: {round(1 / sum(1 / value for value in values), 3)} Ohms"
        except ZeroDivisionError:
            return "Error: Division by zero in parallel resistance calculation"
    return "Invalid circuit type"

def calculate_capacitor(circuit_type, values):
    if not values:
        return "Error: No values provided"
    if circuit_type == 'series':
        try:
            return f"Total Capacitance: {round(1 / sum(1 / value for value in values), 3)} Microfarads"
        except ZeroDivisionError:
            return "Error: Division by zero in series capacitance calculation"
    elif circuit_type == 'parallel':
        return f"Total Capacitance: {sum(values)} Microfarads"
    return "Invalid circuit type"

def calculate_inductor(circuit_type, values):
    if not values:
        return "Error: No values provided"
    if circuit_type == 'series':
        return f"Total Inductance: {sum(values)} Henrys"
    elif circuit_type == 'parallel':
        try:
            return f"Total Inductance: {round(1 / sum(1 / value for value in values), 3)} Henrys"
        except ZeroDivisionError:
            return "Error: Division by zero in parallel inductance calculation"
    return "Invalid circuit type"

if __name__ == '__main__':
    app.run(debug=True)
