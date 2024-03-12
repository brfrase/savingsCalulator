from flask import Flask, render_template, request
from scipy.optimize import fsolve
import numpy as np

app = Flask(__name__)

def calculate_months(startBal, goalBal, monthInv, annual_rate):
    monthInt = 1 + (annual_rate / 12)
    r = monthInt - 1

    def future_value(n, P, PMC, r):
        return P * ((1 + r)**n) + PMC * (((1 + r)**n - 1) / r)

    equation = lambda n: future_value(n, startBal, monthInv, r) - goalBal

    initial_guess = 100
    months = fsolve(equation, initial_guess)[0]
    return np.ceil(months)

@app.route('/', methods=['GET', 'POST'])
def index():
    months = None
    if request.method == 'POST':
        try:
            startBal = float(request.form.get('startBal'))
            goalBal = float(request.form.get('goalBal'))
            monthInv = float(request.form.get('monthInv'))
            annual_rate = float(request.form.get('annual_rate')) / 100
            unit = request.form.get('unit', 'months')

            if unit == 'years':
                months = calculate_months(startBal, goalBal, monthInv, annual_rate) / 12
            else:
                months = calculate_months(startBal, goalBal, monthInv, annual_rate)

            months = int(np.ceil(months))
        except ValueError:
            months = "Invalid input. Please ensure all fields are filled correctly."

    return render_template('index.html', months=months)

if __name__ == '__main__':
    app.run(debug=True)
