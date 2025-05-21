from fasthtml.common import *
from sqlite3 import *
from ksuid import ksuid


login_redirect = RedirectResponse("/login", status_code=303)

def user_auth(req, session):
    if not session.get("auth"):
        return login_redirect

b4ware = Beforeware(user_auth, skip=[
    r"^/login$",             # exact match
    r"^/register$",          # exact match
    r"^/static/.*",          # any file under /static/
    r"^/css/.*",             # # any file under /css/
    r"^/favicon\.ico$",      # literal favicon.ico
])

@dataclass
class LoginForm:
    username: str
    password: str

ADMIN_USER = "admin"
ADMIN_PASS = "admin1"
# ADMIN_USER = "James"
# ADMIN_PASS = "james1"

db = database("data/app.db")

users = db.t.users
if users not in db.t:
    users.create(
        dict(
            id=str,
            username=str,
            password=str
        ),
        pk="username"
    )

if not any(user["username"] == "admin" for user in users()):
    users.insert(id=str(ksuid()), username="admin", password="admin1")

notes = db.t.notes
if notes not in db.t:
    notes.create(
        {
            "id": str,
            "user_id": str,
            "date": str,
            "content": str,
        },
        pk="id"
    )


# for Docker
# app, rt = fast_app(static_path="static")

# for local
app, rt = fast_app(before=b4ware, static_path="app/static")

default_header = Head(
                    Title("Notes App"),
                    Meta(charset="UTF-8"),
                    Meta(name="viewport", content="width=device-width, initial-scale=1"),
                    Meta(name="description", content="insert page description for Search Engines"),
                    Meta(name="author", content="EvenMoreH"),
                    Script(src="https://unpkg.com/htmx.org"),
                    Link(rel="stylesheet", href="css/tailwind.css"),
                    Link(rel="icon", href="images/favicon.ico", type="image/x-icon"),
                    Link(rel="icon", href="images/favicon.png", type="image/png"),
                )


@rt("/")
def get(session, req):
    current_user = session.get("auth")
    return Html(
        default_header,
        Body(
            H1("Homepage", cls="pt-20 pb-2 text-xl text-center font-semibold"),
            Div(
                P(f"Hi! {current_user}", cls="font-bold"),
                cls="flex justify-center"
            ),
            # whole body CSS
            cls="body"
        ),
    lang="en",
    )


@rt("/login")
def get(session, req):
    session["auth"] = ""

# print who is in database already for testing
    for user in db.t.users():
        print(user["id"])
        print(user["username"])

    return Html(
        default_header,
        Body(
            H1("Login Page", cls="pt-20 pb-2 text-xl text-center font-semibold"),
            Div(
                Form(
                    Input(name="username", placeholder="  Username", cls="input1"),
                    # obfuscate password field using type="password"
                    Input(name="password", placeholder="  Password", type="password", cls="input1"),
                    Button("Login", type="submit", cls="btn"),
                    action="login", method="post",
                    cls="flex justify-center"
                ),
                cls="flex justify-center"
            ),
            Div(
                P("No account? Sign up below."),
                # Button("Register account", type="submit", action="register", method="post", cls="btn")
                A("Register account", href="/register", cls="btn")
            ),
            # whole body CSS
            cls="body"
        ),
    lang="en",
    )

@rt("/login")
def post(data: LoginForm, session):
    if data.username == ADMIN_USER and data.password == ADMIN_PASS:
        session["auth"] = data.username

        return RedirectResponse("/", status_code=303)
    else:
        return login_redirect


# TODO:
# - below code (commented function) that checks if user with provided username is in DB already,
#   if yes, it needs to prompt that such username exists and should not add user to DB
#   if no user in DB and username is valid it should add user to DB

# def add_user(data: LoginForm, session):
#     if not any(user["username"] == f"{data.username}" for user in users()):
#         users.insert(username=f"{data.username}", password=f"{data.password}")
#     else:
#         print(f"user with username {data.username} already exists!")

@rt("/register")
def get(session, req):
    return Html(
        default_header,
        Body(
            H1("Register Account", cls="pt-20 pb-2 text-xl text-center font-semibold"),
            Form(
                Input(name="username", placeholder="  Username", cls="input1"),
                Input(name="password", placeholder="  Password", type="password", cls="input1"),
                Input(name="rpassword", placeholder="  Repeat Password", type="password", cls="input1"),
                Button("Register", hx_post="register", hx_target="#message1", hx_push_url="true", cls="btn"),
                cls="flex justify-center",
                id="signup",
            ),
            Div(id="message1"),
            cls="body",
        )
    )

@rt("/register")
async def post(data: LoginForm, session, req):
    form = await req.form()
    password  = form["password"]
    rpassword = form["rpassword"]

    if password != rpassword:
        return Div("Passwords do not match!", id="message1", hx_swap_oob=True)

    if any(user["username"] == f"{data.username}" for user in users()):
        return Div("Username taken!", id="message1", hx_swap_oob=True)
    else:
        users.insert(id=str(ksuid()), username=f"{data.username}", password=f"{data.password}")
        return Div(
            "Sign up successful!",
            A("Login", href="login", cls="btn"),
            id="message1", hx_swap_oob=True)

serve()

# if __name__ == '__main__':
#     # Important: Use host='0.0.0.0' to make the server accessible outside the container
#     serve(host='0.0.0.0', port=5001) # type: ignore