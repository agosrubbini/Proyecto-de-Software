from src.web import create_app
from authlib.integrations.flask_client import OAuth

app = create_app()
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='',
    client_secret='',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1',
    client_kwargs={'scope': 'openid profile email'}
)

if __name__ == "__main__":
    app.run()