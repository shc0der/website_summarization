from injector import Injector

from app.di.app_module import AppModule
from app.presentation.application import Application


def main():
    injector = Injector([AppModule()])
    application = injector.get(Application)
    application.launch()


if __name__ == "__main__":
    main()
