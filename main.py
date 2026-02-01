"""
Real Estate MIS Application
Main entry point for the desktop application.
"""
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from core.database import db_manager
from ui.main_window import MainWindow
import config
from PySide6.QtCore import QtMsgType, qInstallMessageHandler


def suppress_qt_warnings(mode, context, message):
    if "QFont::setPointSize" in message:
        return  # Ignore this specific spam warning
    print(message)

def main():
    """
    Main application entry point.
    """
    # Create application instance
    app = QApplication(sys.argv)

    # Set application metadata
    app.setApplicationName(config.APP_NAME)
    app.setApplicationVersion(config.APP_VERSION)
    app.setOrganizationName(config.APP_AUTHOR)
    
    # Note: High DPI scaling is automatic in Qt6/PySide6
    # No need to manually enable AA_EnableHighDpiScaling or AA_UseHighDpiPixmaps
    
    # Initialize database
    print("Initializing database...")
    db_manager.initialize()
    
    # Create and show main window
    print("Launching application...")
    qInstallMessageHandler(suppress_qt_warnings)
    window = MainWindow()
    window.show()
    
    # Start event loop
    exit_code = app.exec()
    
    # Cleanup
    print("Shutting down...")
    db_manager.close()
    
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
