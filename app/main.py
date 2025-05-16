from fasthtml.common import *


login_redirect = RedirectResponse("/login", status_code=303)

def user_auth(req, session):
    if not session.get("auth"):
        return login_redirect

b4ware = Beforeware(user_auth, skip=[
    r"^/login$",             # exact match
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


# for Docker
# app, rt = fast_app(static_path="static")

# for local
app, rt = fast_app(before=b4ware, static_path="app/static")

default_header = Head(
                    Title("Color Converter"),
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
def get(session):
    current_user = session.get("auth")
    return Html(
        default_header,
        Body(
            H1("Homepage", cls="pt-20 pb-2 text-xl text-center font-semibold"),
            Div(
                P(f"Hi! {current_user}"),
                cls="flex justify-center"
            ),
            # whole body CSS
            cls="body"
        ),
    lang="en",
    )


@rt("/login")
def get(session):
    session["auth"] = ""
    return Html(
        default_header,
        Body(
            H1("Login Page", cls="pt-20 pb-2 text-xl text-center font-semibold"),
            Div(
                Form(
                    Input(name="username", placeholder="  Username", cls="p-1 m-2"),
                    Input(name="password", placeholder="  Password", cls="p-1 m-2"),
                    Button("Login", type="submit", cls="btn"),
                    action="login", method="post",
                    cls="flex justify-center"
                ),
                cls="flex justify-center"
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


serve()

# if __name__ == '__main__':
#     # Important: Use host='0.0.0.0' to make the server accessible outside the container
#     serve(host='0.0.0.0', port=5001) # type: ignore