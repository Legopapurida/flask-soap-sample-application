from project import create_app
from project.config import DevelopmentConfig

if __name__ == '__main__':

    app = create_app(DevelopmentConfig)

    app.run(
        host=app.config['HOST'],
        port=app.config['PORT']
    )