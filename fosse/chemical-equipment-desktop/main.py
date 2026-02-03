import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt5.QtCore import Qt
from api_client import APIClient
from views import LoginView, DashboardView
from styles import get_stylesheet

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment visualizer - Command Center")
        self.setMinimumSize(1200, 800)
        
        self.api = APIClient()
        
        # Central widget and layout
        self.central_widget = QStackedWidget()
        self.setCentralWidget(self.central_widget)
        
        self.init_ui()
        
    def init_ui(self):
        # Apply global styling
        self.setStyleSheet(get_stylesheet())
        
        # Login View
        self.login_view = LoginView(self.api)
        self.login_view.login_success.connect(self.show_dashboard)
        self.central_widget.addWidget(self.login_view)
        
        # Dashboard View
        self.dashboard_view = DashboardView(self.api)
        self.dashboard_view.logout_btn.clicked.connect(self.show_login)
        self.central_widget.addWidget(self.dashboard_view)
        
        # Start at login
        self.show_login()

    def show_dashboard(self, user_data):
        self.central_widget.setCurrentWidget(self.dashboard_view)
        
    def show_login(self):
        self.central_widget.setCurrentWidget(self.login_view)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
