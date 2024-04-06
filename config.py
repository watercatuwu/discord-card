from urllib import parse

# configure area
PORT = 8080
TOKEN = "" #bot token
CLIENT_ID = "" #oauth2 client id
CLIENT_SECRET = "" #oauth2 client secret
REDIRECT_URI = f"http://localhost:{PORT}/oauth/callback" #set a redirct uri in oauth2 page(ex: http://localhost:8080/oauth/callback)
SECRET_KEY = "uwuwuwuwuub" # a random ganarate string

scope = ["identify","connections"]
SERVICES = ["youtube", "github", "twitch"]

scopestr = ""
for i in scope:
   scopestr += i + "+"

OAUTH_URL = f"https://discord.com/oauth2/authorize?client_id={CLIENT_ID}&response_type=code&redirect_uri={parse.quote(REDIRECT_URI)}&scope={scopestr}"