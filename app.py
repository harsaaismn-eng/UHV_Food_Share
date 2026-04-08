from flask import Flask, render_template, request, redirect

app = Flask(__name__)

donations = []
requests_data = []
volunteers = []
notifications = []

@app.route('/')
def home():
    return render_template(
        'index.html',
        donations=donations,
        requests=requests_data,
        volunteers=volunteers,
        notifications=notifications
    )

# -------- DONATION --------
@app.route('/add_donation', methods=['POST'])
def add_donation():
    donor = request.form['donor']
    food = request.form['food']
    qty = request.form['quantity']
    loc = request.form['location']

    donations.append({
        "donor": donor,
        "food": food,
        "quantity": qty,
        "location": loc
    })

    return redirect('/')

# -------- REQUEST --------
@app.route('/add_request', methods=['POST'])
def add_request():
    name = request.form['name']
    food = request.form['food']
    qty = request.form['quantity']
    loc = request.form['location']
    contact = request.form['contact']

    req = {
        "name": name,
        "food": food,
        "quantity": qty,
        "location": loc,
        "contact": contact,
        "fulfilled": False
    }

    requests_data.append(req)
    return redirect('/')

# -------- VOLUNTEER --------
@app.route('/add_volunteer', methods=['POST'])
def add_volunteer():
    name = request.form['name']
    city = request.form['city']
    phone = request.form['phone']

    volunteers.append({
        "name": name,
        "city": city,
        "phone": phone
    })

    return redirect('/')

# -------- FULFILL --------
@app.route('/fulfill/<int:i>')
def fulfill(i):
    req = requests_data[i]

    for d in donations:
        if d['food'].lower() == req['food'].lower() and d['location'].lower() == req['location'].lower():
            for v in volunteers:
                if v['city'].lower() == req['location'].lower():
                    notifications.append(
                        f"🚚 {v['name']} delivering {req['food']} to {req['name']}"
                    )
                    req['fulfilled'] = True
                    return redirect('/')

    notifications.append("❌ No match found")
    return redirect('/')

# -------- DELETE --------
@app.route('/delete_donation/<int:i>')
def delete_donation(i):
    donations.pop(i)
    return redirect('/')

@app.route('/delete_request/<int:i>')
def delete_request(i):
    requests_data.pop(i)
    return redirect('/')

@app.route('/delete_volunteer/<int:i>')
def delete_volunteer(i):
    volunteers.pop(i)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
