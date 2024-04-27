from flask import Blueprint, render_template, redirect, url_for, request, flash, jsonify, session
from app import oauth, db,models, login_manager,books,movie,artworks
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from config import Config

main = Blueprint("main", __name__)

google = oauth.remote_app(
    "google",
    consumer_key=Config.GOOGLE_OAUTH_CLIENT_ID,
    consumer_secret=Config.GOOGLE_OAUTH_CLIENT_SECRET,
    request_token_params={"scope": "email profile"},
    base_url="https://www.googleapis.com/oauth2/v1/",
    request_token_url=None,
    access_token_method="POST",
    access_token_url="https://accounts.google.com/o/oauth2/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
)

login_manager = LoginManager()
login_manager.login_view = 'main.login'


def load_user(user_id):
    return models.User.query.get(str(user_id))

@main.route("/")
def index():
    
    if current_user.is_authenticated:
        return render_template("index.html", user=current_user)
    else:
        return render_template("index.html")



@main.route("/login")
def login():
    callback = url_for("main.authorized", _external=True, _scheme="http")
    return google.authorize(callback=callback)


@main.route("/logout")
@login_required
def logout():
    logout_user()  
    session.pop("google_token", None)
    session.pop("user", None)
    return redirect(url_for(".index"))


@main.route("/authorized")
def authorized():
    resp = google.authorized_response()
    if resp is None or resp.get('access_token') is None:
        flash("Authorization failed.")
        return redirect(url_for(".index"))

    access_token = resp["access_token"]
    session['google_token'] = (access_token, '')

    # Get user information
    user_data = google.get("https://www.googleapis.com/oauth2/v1/userinfo")
    if not user_data.status == 200:
        flash("Failed to fetch user data.")
        return redirect(url_for(".index"))

    
    user_id = user_data.data["id"]
    user_email = user_data.data["email"]
    user_name = user_data.data["name"]

# Check if the user already exists in the database
    user = models.User.query.get(user_id)

# If the user does not exist, create a new User object and add it to the database
    if user is None:
        user = models.User(id=user_id, email=user_email, name=user_name)
        db.session.add(user)
        db.session.commit()

# Log in the user
    login_user(user, remember=True)


    flash(f"You were successfully logged in as {user_data.data['name']}.")
    return redirect(url_for(".index"))

@main.route("/book_to_movie", methods=["GET", "POST"])
def book_to_movie():
    if current_user.is_authenticated:
        if request.method == "POST":
            book = request.form.get("book")
            if book:
                book_data = books.get_book(book,Config.GOOGLE_BOOK_API_KEY)
                movie_data = movie.get_movie(book,Config.TMDB_API_KEY)
                artwork_data = artworks.artwork()
                return render_template("book_to_movie.html", book_data=book_data, movie_data=movie_data,artwork_data = artwork_data)
            else:
                flash("Book name is required.")
                return render_template("book_to_movie.html")
    else:
        flash("Please log in to access the book_to_movie recommendation system.")
        return redirect(url_for('main.index'))
            



@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')
