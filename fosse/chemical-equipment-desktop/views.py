from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, 
                             QPushButton, QLabel, QFrame, QFileDialog, QListWidget,
                             QListWidgetItem, QGraphicsDropShadowEffect)
from PyQt5.QtCore import Qt, pyqtSignal, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
import json
import os

class LoginView(QWidget):
    login_success = pyqtSignal(dict)
    
    def __init__(self, api):
        super().__init__()
        self.api = api
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        
        # Card-like container
        card = QFrame()
        card.setFixedSize(400, 500)
        card.setObjectName("loginCard")
        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(40, 40, 40, 40)
        card_layout.setSpacing(20)
        
        # Title
        title = QLabel("Command Center")
        title.setObjectName("loginTitle")
        title.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(title)
        
        subtitle = QLabel("Desktop Edition")
        subtitle.setObjectName("loginSubtitle")
        subtitle.setAlignment(Qt.AlignCenter)
        card_layout.addWidget(subtitle)
        
        # Inputs
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")
        self.username_input.setObjectName("loginInput")
        card_layout.addWidget(self.username_input)
        
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setObjectName("loginInput")
        card_layout.addWidget(self.password_input)
        
        # Buttons
        self.login_btn = QPushButton("Login")
        self.login_btn.setObjectName("primaryBtn")
        self.login_btn.clicked.connect(self.handle_login)
        card_layout.addWidget(self.login_btn)
        
        self.demo_btn = QPushButton("Quick Demo Login")
        self.demo_btn.setObjectName("secondaryBtn")
        self.demo_btn.clicked.connect(self.handle_demo_login)
        card_layout.addWidget(self.demo_btn)
        
        self.error_label = QLabel("")
        self.error_label.setObjectName("errorLabel")
        self.error_label.setWordWrap(True)
        card_layout.addWidget(self.error_label)
        
        layout.addWidget(card)
        
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if not username or not password:
            self.error_label.setText("Please enter credentials")
            return
            
        success, message = self.api.login(username, password)
        if success:
            self.login_success.emit(self.api.user_data)
        else:
            self.error_label.setText(message)

    def handle_demo_login(self):
        success, message = self.api.google_login("demo@fosse.com")
        if success:
            self.login_success.emit(self.api.user_data)
        else:
            self.error_label.setText(message)

class DashboardView(QWidget):
    def __init__(self, api):
        super().__init__()
        self.api = api
        self.init_ui()
        
    def init_ui(self):
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Sidebar (simplified for desktop)
        sidebar = QFrame()
        sidebar.setObjectName("appSidebar")
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout(sidebar)
        
        sidebar_title = QLabel("FOSSE Visualizer")
        sidebar_title.setObjectName("sidebarTitle")
        sidebar_layout.addWidget(sidebar_title)
        
        self.upload_btn = QPushButton("📤 Upload CSV")
        self.upload_btn.setObjectName("sidebarBtn")
        self.upload_btn.clicked.connect(self.handle_upload)
        sidebar_layout.addWidget(self.upload_btn)
        
        sidebar_layout.addStretch()
        
        self.logout_btn = QPushButton("Logout")
        self.logout_btn.setObjectName("sidebarBtn")
        sidebar_layout.addWidget(self.logout_btn)
        
        layout.addWidget(sidebar)
        
        # Main Content
        content = QWidget()
        self.content_layout = QVBoxLayout(content)
        
        header = QLabel("Dashboard")
        header.setObjectName("viewHeader")
        self.content_layout.addWidget(header)
        
        # Web Engine for Plotly
        self.web_view = QWebEngineView()
        self.web_view.setObjectName("plotlyContainer")
        self.content_layout.addWidget(self.web_view)
        
        layout.addWidget(content)
        
    def handle_upload(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select CSV", "", "CSV Files (*.csv)")
        if file_path:
            success, result = self.api.upload_csv(file_path)
            if success:
                self.load_visualizations(result['data'])
                
    def load_visualizations(self, data):
        # We'll generate a simple HTML string that uses the same Plotly logic as web
        html = f"""
        <html>
        <head>
            <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
            <style>
                body {{ background: #0a192f; margin: 0; padding: 0; overflow: hidden; }}
                #plot {{ width: 100vw; height: 100vh; }}
            </style>
        </head>
        <body>
            <div id="plot"></div>
            <script>
                const data = {json.dumps(data)};
                const trace = {{
                    x: data.map(d => d.flowrate),
                    y: data.map(d => d.pressure),
                    z: data.map(d => d.temperature),
                    mode: 'markers',
                    type: 'scatter3d',
                    marker: {{
                        size: 8,
                        color: data.map(d => d.temperature),
                        colorscale: 'Viridis',
                        opacity: 0.8
                    }}
                }};
                const layout = {{
                    paper_bgcolor: 'rgba(0,0,0,0)',
                    plot_bgcolor: 'rgba(0,0,0,0)',
                    font: {{ color: '#e6f1ff' }},
                    margin: {{ l: 0, r: 0, b: 0, t: 0 }},
                    scene: {{
                        xaxis: {{ title: 'Flowrate' }},
                        yaxis: {{ title: 'Pressure' }},
                        zaxis: {{ title: 'Temperature' }}
                    }}
                }};
                Plotly.newPlot('plot', [trace], layout);
            </script>
        </body>
        </html>
        """
        self.web_view.setHtml(html)
