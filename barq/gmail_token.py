from google_auth_oauthlib.flow import Flow

SCOPES = [
    "https://www.googleapis.com/auth/gmail.modify"
]

flow = Flow.from_client_secrets_file(
    "credentials.json",
    scopes=SCOPES
)

flow.redirect_uri = "https://didactic-space-tribble-pjr99pwv6gx4394q7.github.dev"

auth_url, state = flow.authorization_url(
    access_type="offline",
    prompt="consent",
    include_granted_scopes="true"
)

print("\nOpen this URL in your browser:\n")
print(auth_url)

redirected_url = input(
    "\nAfter login, paste the FULL URL you were redirected to:\n"
).strip()

# Extract ?code= from pasted URL
from urllib.parse import urlparse, parse_qs

parsed = urlparse(redirected_url)
code = parse_qs(parsed.query)["code"][0]

flow.fetch_token(code=code)

with open("token.json", "w") as f:
    f.write(flow.credentials.to_json())

print("\n✅ token.json created successfully")