from view import AppView
from model import AppModel


class AppController:
    def __init__(self, root):
        self.model = AppModel()
        self.view = AppView(root)
        # Setup event bindings or other initializations

    def run(self):
        # Here, you might start the main application loop or other necessary services
        pass