from uuid import uuid4

class BaseConfig:

    # Environment config
    DEBUG: bool = ...
    SECRET_KET: str = ...

    # Database Config
    DBHOST: str = ...
    DBNAME: str = ...
    DBPASS: str = ...
    DBUSER: str = ...
    DBPORT: int = ...

    # Host config
    HOST: str = ...
    PORT: int = ...
    

class DevelopmentConfig(BaseConfig):

    DEBUG: bool = True
    HOST: str = 'localhost'
    PORT: int = 8080
    SECRET_KEY: str = str(uuid4())
    DBHOST: str = 'localhost'
    DBNAME: str = 'database'
    DBPASS: str = ''
    DBUSER: str = 'user'
    DBPORT: int = 3392