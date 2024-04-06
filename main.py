from config import TOKEN, CLIENT_SECRET, REDIRECT_URI, OAUTH_URL, SERVICES, SECRET_KEY, PORT
from flask import Flask, render_template, request, redirect, url_for, session
from zenora import APIClient
import requests

app = Flask(__name__)
client = APIClient(TOKEN, client_secret = CLIENT_SECRET)

app.config["SECRET_KEY"] = SECRET_KEY

@app.route("/")
def home():
    access_token = session.get("access_token")
    if not access_token:
        return render_template("index.html")
    connections = get_current_user_connections(access_token, SERVICES)
    current_user = get_current_user(access_token)

    return render_template("index.html", user = current_user, connections = connections)

@app.route("/login")
def login():
    return redirect(OAUTH_URL)

@app.route("/logout")
def logout():
    session.pop("access_token")
    return redirect("/")

@app.route("/oauth/callback")
def callback():
    if "error" in request.args:
        errormsg = request.args["error"] + ":" + request.args["error_description"]
        return redirect("/")
    
    code = request.args["code"]
    oauth_response = client.oauth.get_access_token(code, REDIRECT_URI)
    access_token = oauth_response.access_token
    session["access_token"] = access_token
    return redirect("/")

#api function
def get_current_user(access_token):
    type = "/users/@me"
    user = discordapi(access_token, type)
    avatar_url = f"https://cdn.discordapp.com/avatars/{user["id"]}/{user["avatar"]}.webp?size=512"
    user["avatar_url"] = avatar_url
    return user

def get_current_user_connections(access_token, services):
    type = "/users/@me/connections"
    connections = discordapi(access_token, type)
    needed_connections = {}
    #選取對應到services的元素
    for element in connections:
        if element["type"] in services:
            needed_connections[element["type"]] = element
    #加入用戶沒有連接的帳戶並設定空字串
    for i in range(len(services)):
        if services[i] not in needed_connections.keys():
            needed_connections[services[i]] = ""
    return needed_connections
    
def discordapi(access_token, type):
    url = "https://discord.com/api/v10" + type

    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        return ("Failed, Status code:", response.status_code)


if __name__ == "__main__":
    app.run(port=PORT)