from pathlib import Path

from app import create_app
from flask_frozen import Freezer

app = create_app()
app.config["FREEZER_DESTINATION"] = str(Path(__file__).resolve().parent / "build")
app.config["FREEZER_RELATIVE_URLS"] = True
freezer = Freezer(app)


@freezer.register_generator
def blog_post_slugs():
    # yield each slug so Frozen-Flask knows every /blog/<slug> URL to build
    from app.blog.routes import all_post_slugs

    for slug in all_post_slugs():
        yield "blog.post", {"slug": slug}


@freezer.register_generator
def game_slugs():
    from app.games.routes import all_game_slugs

    for slug in all_game_slugs():
        yield "games.play", {"slug": slug}


if __name__ == "__main__":
    freezer.freeze()
