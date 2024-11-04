from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        # Retrieve form data
        age = int(request.form.get('age', 0))
        sex = int(request.form.get('sex', 0))
        pivka = int(request.form.get('pivka', 0))
        afp = int(request.form.get('afp', 0))
        etiology = int(request.form.get('etiology', 0))

        # Logistic regression equation to calculate logit(p)
        logit_p = -4.394 + (1.553 * age) + (1.311 * sex) + (1.720 * pivka) + (2.690 * afp) + (1.515 * etiology)

        # Format logit_p to two decimal places
        logit_p = round(logit_p, 2)

        # Convert logit(p) to probability
        probability = 1 / (1 + (2.71828 ** -logit_p))  # Convert logit to probability
        probability_percentage = probability * 100

        # Determine the probability category
        if probability_percentage >= 75:
            risk_category = "The patient has a very high (>75%) probability of having HCC"
        elif 50 <= probability_percentage < 75:
            risk_category = "The patient has a high (50-75%) probability of having HCC"
        elif 25 <= probability_percentage < 50:
            risk_category = "The patient has a moderate (25-50%) probability of having HCC"
        else:
            risk_category = "The patient has a low (<25%) probability of having HCC"

        # Render result with formatted logit and category
        return render_template('result.html', logit_p=logit_p, risk_category=risk_category)
    except Exception as e:
        return f"An error occurred: {e}"

if __name__ == '__main__':
    app.run(debug=True)
