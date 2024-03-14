from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route("/list_prof/<param>")
def list_prof(param):
    prof = ["инженер-исселователь", "пилот", "строитель", "экзобиолог",
            "врач", "инженер по-терраформированию", "климатолог",
            "специалист по радиоционной защите", "астрогеолог", "инженер жизнеобеспечения",
            "метеоролог", "оператор марсохода", "киберинженер", "штурман", "пилот дронов"]
    return render_template("index.html", param=param,
                           members=prof)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
