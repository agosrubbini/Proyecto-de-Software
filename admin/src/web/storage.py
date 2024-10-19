from minio import Minio 

class Storage:

    def __init__(self, app=None):

        self._client = None
        if app is not None:
            self.init_app(app)

    
    def init_app(self, app):

        """
            Inicializa el cliente de MiniO y lo adjunta al contexto 
        """

        minio_server = app.config.get("MINIO_SERVER")
        access_key = app.config.get("MINIO_ACCESS_KEY")
        secret_key = app.config.get("MINIO_SECRET_KEY")
        secure = app.config.get("MINIO_SECURE", False)

        # Inicializa el cliente de Minio

        self._client = Minio(
            minio_server, access_key = access_key, secret_key = secret_key, secure = secure
        )

        # Adjunta el cliente al contexto de la app

        app.storage = self

        return app


    @property
    def client(self):

        """
            Propiedad para obtener el cliente de MiniO
        """

        return self._client

    @client.setter
    def client(self, value):

        """
            Propiedad setter para permitir reasignar el cliente de MiniO
        """

        self._client = value


storage = Storage()
