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
    SECRET_KEY: str = '99da28d8-fc31-451e-85c1-728bd8562787'
    DBHOST: str = '127.0.0.1'
    DBNAME: str = 'mydatabase'
    DBPASS: str = "Ali1362137"
    DBUSER: str = 'root'
    DBPORT: int = 3306