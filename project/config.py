
class BaseConfig:

    # Environment config
    DEBUG: bool = ...

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
