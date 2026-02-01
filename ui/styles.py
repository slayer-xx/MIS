"""
Global Styles
Centralized stylesheet for the entire application.
Modify colors, fonts, and spacing here to change the entire UI theme.
"""

# Color Palette (Professional & Calm)
PRIMARY_COLOR = "#2c3e50"          # Dark blue-gray
SECONDARY_COLOR = "#34495e"        # Lighter blue-gray
ACCENT_COLOR = "#3498db"           # Blue
SUCCESS_COLOR = "#27ae60"          # Green
WARNING_COLOR = "#f39c12"          # Orange
DANGER_COLOR = "#e74c3c"           # Red
BACKGROUND_COLOR = "#ecf0f1"       # Light gray
CARD_BACKGROUND = "#ffffff"        # White
TEXT_PRIMARY = "#2c3e50"           # Dark text
TEXT_SECONDARY = "#7f8c8d"         # Gray text
BORDER_COLOR = "#bdc3c7"           # Light border

# Typography
FONT_FAMILY = "Segoe UI, Arial, sans-serif"
FONT_SIZE_SMALL = "11px"
FONT_SIZE_NORMAL = "13px"
FONT_SIZE_LARGE = "15px"
FONT_SIZE_HEADING = "18px"
FONT_SIZE_TITLE = "24px"

# Spacing
SPACING_SMALL = "8px"
SPACING_MEDIUM = "16px"
SPACING_LARGE = "24px"

# Border Radius
BORDER_RADIUS_SMALL = "4px"
BORDER_RADIUS_MEDIUM = "6px"
BORDER_RADIUS_LARGE = "8px"


def get_stylesheet():
    """
    Returns the complete application stylesheet.
    """
    return f"""
    /* Global Application Styles */
    QWidget {{
        font-family: {FONT_FAMILY};
        font-size: {FONT_SIZE_NORMAL};
        color: {TEXT_PRIMARY};
    }}

    /* Main Window */
    QMainWindow {{
        background-color: {BACKGROUND_COLOR};
    }}

    /* Central Widget */
    QWidget#centralWidget {{
        background-color: {BACKGROUND_COLOR};
    }}

    /* Sidebar */
    #sidebar {{
        background-color: {PRIMARY_COLOR};
        border-right: 2px solid {SECONDARY_COLOR};
    }}
    
    #appTitle {{
        color: white;
        padding: 10px;
    }}
    
    #versionLabel {{
        color: #95a5a6;
        font-size: 11px;
        padding: 5px;
    }}
    
    /* Navigation buttons */
    QPushButton#navButton {{
        background-color: transparent;
        color: white;
        border: none;
        border-radius: {BORDER_RADIUS_SMALL};
        padding: 12px 15px;
        text-align: left;
        font-size: 14px;
        margin: 2px 0;
    }}
    
    QPushButton#navButton:hover {{
        background-color: {SECONDARY_COLOR};
    }}
    
    QPushButton#navButton:checked {{
        background-color: {ACCENT_COLOR};
        color: white;
        font-weight: bold;
    }}

    /* Page Containers */
    QWidget[cssClass="page"] {{
        background-color: {CARD_BACKGROUND};
        border-radius: {BORDER_RADIUS_MEDIUM};
    }}
    
    /* Page Title */
    QLabel#pageTitle {{
        font-size: {FONT_SIZE_TITLE};
        font-weight: bold;
        color: {PRIMARY_COLOR};
        padding: 5px 0;
    }}

    /* Headers and Titles */
    QLabel[cssClass="page-title"] {{
        font-size: {FONT_SIZE_TITLE};
        font-weight: bold;
        color: {PRIMARY_COLOR};
        padding: {SPACING_MEDIUM};
    }}

    QLabel[cssClass="section-title"] {{
        font-size: {FONT_SIZE_HEADING};
        font-weight: bold;
        color: {PRIMARY_COLOR};
        padding: {SPACING_SMALL} 0px;
    }}
    
    QLabel#sectionTitle {{
        font-size: 14px;
        font-weight: bold;
        color: {PRIMARY_COLOR};
    }}
    
    QLabel#warningTitle {{
        color: {WARNING_COLOR};
        font-size: 14px;
        font-weight: bold;
    }}
    
    /* Cards and Frames */
    QFrame#cardFrame {{
        background-color: {CARD_BACKGROUND};
        border: 1px solid {BORDER_COLOR};
        border-radius: {BORDER_RADIUS_LARGE};
        padding: 5px;
    }}
    
    QFrame#summaryCard {{
        background-color: {CARD_BACKGROUND};
        border: 1px solid {BORDER_COLOR};
        border-radius: {BORDER_RADIUS_LARGE};
        padding: 5px;
    }}
    
    QLabel#cardTitle {{
        color: {TEXT_SECONDARY};
        font-size: 12px;
    }}
    
    QLabel#cardValue {{
        color: {PRIMARY_COLOR};
        font-size: 20px;
        font-weight: bold;
    }}
    
    /* Metric widgets */
    QLabel#metricLabel {{
        color: {TEXT_SECONDARY};
        font-size: 12px;
    }}
    
    QLabel#metricValue {{
        color: {PRIMARY_COLOR};
        font-size: 18px;
        font-weight: bold;
    }}
    
    /* Action items */
    QWidget#actionItem {{
        background-color: {CARD_BACKGROUND};
        border: 1px solid {BORDER_COLOR};
        border-radius: {BORDER_RADIUS_SMALL};
        padding: 5px;
    }}
    
    /* Labels */
    QLabel#emptyStateLabel {{
        color: {TEXT_SECONDARY};
        font-style: italic;
        padding: 20px;
    }}
    
    QLabel#successLabel {{
        color: {SUCCESS_COLOR};
        font-weight: bold;
        padding: 20px;
    }}
    
    QLabel#subtleText {{
        color: {TEXT_SECONDARY};
        font-size: 11px;
    }}

    /* Buttons */
    QPushButton {{
        background-color: {ACCENT_COLOR};
        color: white;
        border: none;
        border-radius: {BORDER_RADIUS_SMALL};
        padding: {SPACING_SMALL} {SPACING_LARGE};
        font-weight: bold;
        min-height: 32px;
    }}

    QPushButton:hover {{
        background-color: #2980b9;
    }}

    QPushButton:pressed {{
        background-color: #21618c;
    }}

    QPushButton:disabled {{
        background-color: {BORDER_COLOR};
        color: {TEXT_SECONDARY};
    }}
    
    /* Primary Button */
    QPushButton#primaryButton {{
        background-color: {ACCENT_COLOR};
        color: white;
        border: none;
        border-radius: {BORDER_RADIUS_SMALL};
        padding: 10px 20px;
        font-weight: bold;
        font-size: 14px;
    }}
    
    QPushButton#primaryButton:hover {{
        background-color: #2980b9;
    }}
    
    QPushButton#primaryButton:pressed {{
        background-color: #21618c;
    }}
    
    /* Secondary Button */
    QPushButton#secondaryButton {{
        background-color: {SECONDARY_COLOR};
        color: white;
        border: none;
        border-radius: {BORDER_RADIUS_SMALL};
        padding: 10px 20px;
        font-weight: bold;
        font-size: 14px;
    }}
    
    QPushButton#secondaryButton:hover {{
        background-color: {PRIMARY_COLOR};
    }}
    
    /* Link Button */
    QPushButton#linkButton {{
        background-color: transparent;
        color: {ACCENT_COLOR};
        border: none;
        text-decoration: underline;
        padding: 5px;
    }}
    
    QPushButton#linkButton:hover {{
        color: #2980b9;
    }}

    QPushButton[cssClass="secondary"] {{
        background-color: {SECONDARY_COLOR};
    }}

    QPushButton[cssClass="secondary"]:hover {{
        background-color: #2c3e50;
    }}

    QPushButton[cssClass="success"] {{
        background-color: {SUCCESS_COLOR};
    }}

    QPushButton[cssClass="danger"] {{
        background-color: {DANGER_COLOR};
    }}

    /* Input Fields */
    QLineEdit, QTextEdit, QPlainTextEdit {{
        background-color: white;
        border: 1px solid {BORDER_COLOR};
        border-radius: {BORDER_RADIUS_SMALL};
        padding: {SPACING_SMALL};
        selection-background-color: {ACCENT_COLOR};
    }}

    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
        border: 2px solid {ACCENT_COLOR};
    }}
    
    QDateEdit, QTimeEdit, QSpinBox, QDoubleSpinBox {{
        background-color: white;
        border: 1px solid {BORDER_COLOR};
        border-radius: {BORDER_RADIUS_SMALL};
        padding: {SPACING_SMALL};
    }}
    
    QDateEdit:focus, QTimeEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {{
        border: 2px solid {ACCENT_COLOR};
    }}

    /* ComboBox (Dropdowns) */
    QComboBox {{
        background-color: white;
        border: 1px solid {BORDER_COLOR};
        border-radius: {BORDER_RADIUS_SMALL};
        padding: {SPACING_SMALL};
        min-height: 28px;
    }}

    QComboBox:focus {{
        border: 2px solid {ACCENT_COLOR};
    }}

    QComboBox::drop-down {{
        border: none;
        padding-right: {SPACING_SMALL};
    }}

    QComboBox QAbstractItemView {{
        background-color: white;
        border: 1px solid {BORDER_COLOR};
        selection-background-color: {ACCENT_COLOR};
        selection-color: white;
    }}

    /* Tables */
    QTableWidget {{
        background-color: white;
        border: 1px solid {BORDER_COLOR};
        border-radius: {BORDER_RADIUS_SMALL};
        gridline-color: {BORDER_COLOR};
        selection-background-color: {ACCENT_COLOR};
        selection-color: white;
    }}

    QTableWidget::item {{
        padding: {SPACING_SMALL};
    }}

    QTableWidget::item:hover {{
        background-color: #e8f4f8;
    }}

    QHeaderView::section {{
        background-color: {SECONDARY_COLOR};
        color: white;
        padding: {SPACING_SMALL};
        border: none;
        font-weight: bold;
    }}
    
    /* Tabs */
    QTabWidget::pane {{
        border: 1px solid {BORDER_COLOR};
        border-radius: {BORDER_RADIUS_MEDIUM};
        background-color: white;
        padding: 5px;
    }}
    
    QTabBar::tab {{
        background-color: {BACKGROUND_COLOR};
        color: {TEXT_SECONDARY};
        border: 1px solid {BORDER_COLOR};
        border-bottom: none;
        border-top-left-radius: {BORDER_RADIUS_SMALL};
        border-top-right-radius: {BORDER_RADIUS_SMALL};
        padding: 10px 20px;
        margin-right: 2px;
        font-weight: bold;
    }}
    
    QTabBar::tab:selected {{
        background-color: white;
        color: {ACCENT_COLOR};
    }}
    
    QTabBar::tab:hover {{
        background-color: white;
    }}

    /* ScrollBars */
    QScrollBar:vertical {{
        background-color: {BACKGROUND_COLOR};
        width: 12px;
        border-radius: 6px;
    }}

    QScrollBar::handle:vertical {{
        background-color: {BORDER_COLOR};
        border-radius: 6px;
        min-height: 20px;
    }}

    QScrollBar::handle:vertical:hover {{
        background-color: {TEXT_SECONDARY};
    }}

    QScrollBar:horizontal {{
        background-color: {BACKGROUND_COLOR};
        height: 12px;
        border-radius: 6px;
    }}

    QScrollBar::handle:horizontal {{
        background-color: {BORDER_COLOR};
        border-radius: 6px;
        min-width: 20px;
    }}
    
    QScrollBar::add-line, QScrollBar::sub-line {{
        border: none;
        background: none;
    }}
    
    /* Checkboxes */
    QCheckBox {{
        spacing: 8px;
        color: {TEXT_PRIMARY};
    }}
    
    QCheckBox::indicator {{
        width: 18px;
        height: 18px;
        border: 2px solid {BORDER_COLOR};
        border-radius: 4px;
        background-color: white;
    }}
    
    QCheckBox::indicator:checked {{
        background-color: {ACCENT_COLOR};
        border-color: {ACCENT_COLOR};
    }}
    
    QCheckBox::indicator:checked:hover {{
        background-color: #2980b9;
    }}

    /* Dialogs */
    QDialog {{
        background-color: {CARD_BACKGROUND};
    }}

    /* Labels */
    QLabel {{
        color: {TEXT_PRIMARY};
    }}

    QLabel[cssClass="form-label"] {{
        font-weight: bold;
        color: {PRIMARY_COLOR};
    }}

    QLabel[cssClass="help-text"] {{
        color: {TEXT_SECONDARY};
        font-size: {FONT_SIZE_SMALL};
    }}

    /* Form Layouts */
    QGroupBox {{
        border: 1px solid {BORDER_COLOR};
        border-radius: {BORDER_RADIUS_MEDIUM};
        margin-top: {SPACING_MEDIUM};
        padding-top: {SPACING_MEDIUM};
        font-weight: bold;
    }}

    QGroupBox::title {{
        color: {PRIMARY_COLOR};
        subcontrol-origin: margin;
        left: {SPACING_MEDIUM};
        padding: 0 {SPACING_SMALL};
    }}

    /* Status Bar */
    QStatusBar {{
        background-color: {SECONDARY_COLOR};
        color: white;
    }}

    /* ToolTips */
    QToolTip {{
        background-color: {PRIMARY_COLOR};
        color: white;
        border: none;
        padding: {SPACING_SMALL};
    }}
    """
