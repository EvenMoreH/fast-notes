from fasthtml.common import * # type: ignore

# for Docker
# app, rt = fast_app(static_path="static") # type: ignore

# for local
app, rt = fast_app(static_path="app/static") # type: ignore

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
def homepage():
    return Html(
        default_header,
        Body(
            # inline tailwind
            H1("Hello There", cls="pt-20 pb-1 text-xl text-center text-rose-400 hover:text-rose-700"),
            Div(
                # reusable .btn class set up in input.css
                Button("Click Me!", cls="btn"),
                cls="flex justify-center"
            ),
            # whole body CSS
            cls="body"
        ),
    lang="en",
    )


serve()

# if __name__ == '__main__':
#     # Important: Use host='0.0.0.0' to make the server accessible outside the container
#     serve(host='0.0.0.0', port=5001) # type: ignore