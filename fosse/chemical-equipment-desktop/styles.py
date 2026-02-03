def get_stylesheet():
    return """
    QMainWindow {
        background-color: #0a192f;
    }
    
    #loginCard {
        background-color: rgba(16, 33, 58, 0.7);
        border: 1px solid rgba(0, 212, 255, 0.2);
        border-radius: 20px;
    }
    
    #loginTitle {
        font-size: 28px;
        font-weight: bold;
        color: #00d4ff;
    }
    
    #loginSubtitle {
        font-size: 16px;
        color: #b794f6;
    }
    
    #loginInput {
        background-color: rgba(10, 25, 47, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 8px;
        padding: 12px;
        color: white;
        font-size: 14px;
    }
    
    #loginInput:focus {
        border: 1px solid #00d4ff;
    }
    
    #primaryBtn {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #00d4ff, stop:1 #b794f6);
        border: none;
        border-radius: 8px;
        padding: 12px;
        color: #0a192f;
        font-weight: bold;
        font-size: 14px;
    }
    
    #primaryBtn:hover {
        background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #33e0ff, stop:1 #c9aff8);
    }
    
    #secondaryBtn {
        background: transparent;
        border: 1px solid rgba(183, 148, 246, 0.5);
        border-radius: 8px;
        padding: 12px;
        color: #b794f6;
    }
    
    #secondaryBtn:hover {
        background: rgba(183, 148, 246, 0.1);
    }
    
    #appSidebar {
        background-color: #0b1e35;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    #sidebarTitle {
        font-size: 18px;
        font-weight: bold;
        color: #00d4ff;
        padding: 20px;
    }
    
    #sidebarBtn {
        background: transparent;
        border: none;
        padding: 15px 20px;
        text-align: left;
        color: #a0aec0;
        font-size: 14px;
    }
    
    #sidebarBtn:hover {
        background: rgba(0, 212, 255, 0.1);
        color: #00d4ff;
    }
    
    #viewHeader {
        font-size: 24px;
        font-weight: bold;
        color: white;
        padding: 20px;
    }
    
    #errorLabel {
        color: #ff4d4d;
        font-size: 12px;
    }
    
    #plotlyContainer {
        border-radius: 15px;
        background: #0a192f;
    }
    """
