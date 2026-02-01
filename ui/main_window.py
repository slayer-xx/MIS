"""
Main Window
Central application window managing navigation and page display.
"""
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QStackedWidget,
    QPushButton, QFrame, QLabel, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import config
from ui.styles import get_stylesheet
from core.database import db_manager

# Import all module pages
from modules.deals.ui.deals_list_page import DealsListPage
from modules.deals.ui.deal_details_page import DealDetailsPage
from modules.dashboard.ui.dashboard_page import DashboardPage
from modules.actions.ui.actions_list_page import ActionsListPage
from modules.commission.ui.commission_list_page import CommissionListPage
from modules.clients.ui.clients_list_page import ClientsListPage
from modules.partners.ui.partners_list_page import PartnersListPage
from modules.expenses.ui.expenses_list_page import ExpensesListPage

# Import services
from modules.deals.services.deal_service import DealService
from modules.deals.repositories.deal_repository import DealRepository
from modules.dashboard.services.dashboard_service import DashboardService
from modules.actions.services.action_service import ActionService
from modules.actions.repositories.action_repository import ActionRepository
from modules.commission.services.commission_service import CommissionService
from modules.commission.repositories.commission_repository import CommissionRepository
from modules.clients.services.client_service import ClientService
from modules.clients.repositories.client_repository import ClientRepository
from modules.partners.services.partner_service import PartnerService
from modules.partners.repositories.partner_repository import PartnerRepository
from modules.expenses.services.expense_service import ExpenseService
from modules.expenses.repositories.expense_repository import ExpenseRepository


class MainWindow(QMainWindow):
    """
    Main application window with sidebar navigation.
    Manages navigation between different pages/modules.
    """

    def __init__(self):
        super().__init__()
        self.setup_services()
        self.setup_window()
        self.setup_ui()
        self.apply_styles()

    def setup_services(self):
        """Initialize all services and repositories."""
        # Get database session for repositories that need it
        # Initialize repositories
        # Some repos use self-managed sessions, others use injected session
        self.deal_repo = DealRepository()  # Self-managed
        self.action_repo = ActionRepository()
        self.commission_repo = CommissionRepository()
        self.client_repo = ClientRepository()
        self.partner_repo = PartnerRepository()
        self.expense_repo = ExpenseRepository()
        
        # Initialize services
        self.deal_service = DealService(self.deal_repo)
        self.action_service = ActionService(self.action_repo)
        self.commission_service = CommissionService(self.commission_repo)
        self.client_service = ClientService(self.client_repo)
        self.partner_service = PartnerService(self.partner_repo)
        self.expense_service = ExpenseService(self.expense_repo)
        
        # Initialize dashboard service with other services
        self.dashboard_service = DashboardService(
            deal_service=self.deal_service,
            action_service=self.action_service,
            commission_service=self.commission_service,
            expense_service=self.expense_service
        )

    def setup_window(self):
        """Configure main window properties."""
        self.setWindowTitle(f"{config.APP_NAME} - v{config.APP_VERSION}")
        self.setMinimumSize(config.WINDOW_MIN_WIDTH, config.WINDOW_MIN_HEIGHT)
        self.resize(config.WINDOW_DEFAULT_WIDTH, config.WINDOW_DEFAULT_HEIGHT)

    def setup_ui(self):
        """Initialize the user interface."""
        # Central widget
        central_widget = QWidget()
        central_widget.setObjectName("centralWidget")
        self.setCentralWidget(central_widget)
        
        # Main layout (horizontal: sidebar + content)
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        sidebar = self.create_sidebar()
        main_layout.addWidget(sidebar)
        
        # Content area
        content_widget = QWidget()
        content_layout = QVBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)
        
        # Stacked widget for page navigation
        self.stacked_widget = QStackedWidget()
        content_layout.addWidget(self.stacked_widget)
        
        content_widget.setLayout(content_layout)
        main_layout.addWidget(content_widget, 1)
        
        central_widget.setLayout(main_layout)
        
        # Add pages
        self.setup_pages()
        
        # Status bar
        self.statusBar().showMessage("Ready")

    def create_sidebar(self):
        """Create the navigation sidebar."""
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)
        sidebar.setFrameShape(QFrame.StyledPanel)
        
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 20, 10, 20)
        layout.setSpacing(5)
        
        # App title
        title = QLabel(config.APP_NAME)
        title.setObjectName("appTitle")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        layout.addSpacing(20)
        
        # Navigation buttons
        self.nav_buttons = []
        
        # Dashboard
        self.add_nav_button(layout, "📊 Dashboard", 0)
        
        # Deals
        self.add_nav_button(layout, "🏠 Deals", 1)
        
        # Actions
        self.add_nav_button(layout, "📋 Actions", 2)
        
        # Commission
        self.add_nav_button(layout, "💰 Commission", 3)
        
        # Clients
        self.add_nav_button(layout, "👥 Clients", 4)
        
        # Partners
        self.add_nav_button(layout, "🤝 Partners", 5)
        
        # Expenses
        self.add_nav_button(layout, "💸 Expenses", 6)
        
        layout.addStretch()
        
        # Version info
        version_label = QLabel(f"v{config.APP_VERSION}")
        version_label.setObjectName("versionLabel")
        version_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(version_label)
        
        sidebar.setLayout(layout)
        return sidebar
    
    def add_nav_button(self, layout, text, page_index):
        """Add a navigation button to the sidebar."""
        btn = QPushButton(text)
        btn.setObjectName("navButton")
        btn.setCheckable(True)
        btn.clicked.connect(lambda: self.navigate_to_page(page_index))
        layout.addWidget(btn)
        self.nav_buttons.append(btn)
        
        # Set first button as checked
        if page_index == 0:
            btn.setChecked(True)
    
    def navigate_to_page(self, page_index):
        """Navigate to a specific page."""
        # Update button states
        for i, btn in enumerate(self.nav_buttons):
            btn.setChecked(i == page_index)
        
        # Switch to page
        self.stacked_widget.setCurrentIndex(page_index)
        
        # Refresh the page
        current_page = self.stacked_widget.currentWidget()
        if hasattr(current_page, 'refresh'):
            current_page.refresh()

    def setup_pages(self):
        """Initialize and add all application pages."""
        # Dashboard (index 0)
        self.dashboard_page = DashboardPage(
            self.dashboard_service,
            self.action_service
        )
        self.stacked_widget.addWidget(self.dashboard_page)
        
        # Deals list page (index 1)
        self.deals_list_page = DealsListPage(self.deal_service)
        self.deals_list_page.deal_selected.connect(self.show_deal_details)
        self.stacked_widget.addWidget(self.deals_list_page)
        
        # Actions page (index 2)
        self.actions_page = ActionsListPage(self.action_service)
        self.stacked_widget.addWidget(self.actions_page)
        
        # Commission page (index 3)
        self.commission_page = CommissionListPage(
            self.commission_service,
            self.deal_service
        )
        self.stacked_widget.addWidget(self.commission_page)
        
        # Clients page (index 4)
        self.clients_page = ClientsListPage(self.client_service)
        self.stacked_widget.addWidget(self.clients_page)
        
        # Partners page (index 5)
        self.partners_page = PartnersListPage(self.partner_service)
        self.stacked_widget.addWidget(self.partners_page)
        
        # Expenses page (index 6)
        self.expenses_page = ExpensesListPage(self.expense_service)
        self.stacked_widget.addWidget(self.expenses_page)
        
        # Show dashboard as default page
        self.stacked_widget.setCurrentIndex(0)

    def show_deal_details(self, deal_id: int):
        """
        Show details page for a specific deal.
        
        Args:
            deal_id: ID of the deal to display
        """
        # Create new deal details page
        deal_details_page = DealDetailsPage(self.deal_service, deal_id)
        deal_details_page.close_requested.connect(self.show_deals_list)
        
        # Add to stack and show
        self.stacked_widget.addWidget(deal_details_page)
        self.stacked_widget.setCurrentWidget(deal_details_page)

    def show_deals_list(self):
        """Navigate back to deals list page."""
        # Remove current page if it's a details page
        current_widget = self.stacked_widget.currentWidget()
        if isinstance(current_widget, DealDetailsPage):
            self.stacked_widget.removeWidget(current_widget)
            current_widget.deleteLater()
        
        # Show deals list and refresh
        self.navigate_to_page(1)

    def apply_styles(self):
        """Apply the global stylesheet."""
        self.setStyleSheet(get_stylesheet())

    def closeEvent(self, event):
        """Handle application close event."""
        # Cleanup can be done here if needed
        event.accept()
