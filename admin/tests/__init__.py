from src.web import create_app

app = create_app(env="test")

client = app.test_client()