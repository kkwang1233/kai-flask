from flask import Flask, render_template, request, redirect, session
# from pymongo import MongoClient


app = Flask(__name__)
# set secret key for managing user session
app.secret_key = "07aa0359eb93962d499c696cef90f6180670c2c8"

# campaigns list to store list of campaigns along with a sample
campaigns = [
    {'name': 'Campaign One', 'status': 'Active'}
]

# users list to store list of users with a sample user
users = [
    {'username': 'kai', 'password': 'strongpassword'}
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # checks if username and password combo matches each other
        user = next((user for user in users if user["username"] == username), None)
        if user and user["password"] == password:
            session["username"] = username
            return redirect("/campaigns")
        else:
            return render_template("login.html", error="Invalid username and password combo.")
    else:
        return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # checks if username is already registered
        if any(user["username"] == username for user in users):
            return render_template("register.html", error="Username already exists, please choose another.")

        # add a user
        users.append({"username": username, "password": password})
        return redirect("/login")
    else:
        return render_template("register.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect("/")

@app.route("/campaigns", methods=["GET", "POST"])
def campaign_list():
    # make sure user is logged in
    if "username" in session:
        if request.method == "POST":
            name = request.form.get("name")
            status = request.form.get("status")
            campaign = {"name": name, "status": status}
            campaigns.append(campaign)
            return redirect("/campaigns")
        else:
            return render_template("campaigns.html", campaigns=campaigns)
    else:
        return redirect("/login")

@app.route("/create", methods=["GET", "POST"])
def create_campaign():
    # make sure user is logged
    if "username" in session:
        if request.method == "POST":
            name = request.form.get("name")
            status = request.form.get("status")
            campaign = {"name": name, "status": status}
            campaigns.append(campaign)
            return redirect("/campaigns")
        else:
            return render_template("create.html")
    else:
        return redirect("/login")

@app.route("/edit/<int:campaign_id>", methods=["GET", "POST"])
def edit_campaign(campaign_id):
    # make sure user is logged
    if "username" in session:
        if request.method == "POST":
            name = request.form.get("name")
            status = request.form.get("status")
            campaigns[campaign_id]["name"] = name
            campaigns[campaign_id]["status"] = status
            return redirect("/campaigns")
        else:
            campaign = campaigns[campaign_id]
            return render_template("edit.html", campaign=campaign, campaign_id=campaign_id)
    else:
        return redirect("/login")

@app.route("/delete/<int:campaign_id>")
def delete_campaign(campaign_id):
    # make sure user is logged in
    if "username" in session:
        campaigns.pop(campaign_id)
    return redirect("/campaigns")

@app.route("/logout", endpoint="logout_route")
def logout():
    # clear session data for logged in user
    session.pop("username", None)
    return redirect("/")

# if __name__ == "__main__":
#     app.run()
