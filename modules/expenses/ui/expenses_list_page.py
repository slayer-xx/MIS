"""
Expenses List Page
View and manage all business expenses with filtering and monthly summaries.
"""
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QHeaderView, QLabel, QComboBox, QLineEdit,
    QFrame, QMessageBox, QDateEdit
)
from PySide6.QtCore import Qt, Signal, QDate
from PySide6.QtGui import QFont
from datetime import datetime
QFont().setPointSize(10)  # ensure Qt has a valid default size


class ExpensesListPage(QWidget):
    """Expenses list page with date filtering and summaries."""
    
    expense_selected = Signal(int)
    
    def __init__(self, expense_service):
        super().__init__()
        self.expense_service = expense_service
        self.init_ui()
        self.load_data()
    
    def init_ui(self):
        """Initialize the expenses list UI."""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Header
        header_layout = QHBoxLayout()
        
        title = QLabel("💸 Business Expenses")
        title.setObjectName("pageTitle")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        # Add expense button
        add_btn = QPushButton("➕ Add New Expense")
        add_btn.setObjectName("primaryButton")
        add_btn.clicked.connect(self.add_expense)
        header_layout.addWidget(add_btn)
        
        layout.addLayout(header_layout)
        
        # Summary card
        self.summary_card = self.create_summary_card()
        layout.addWidget(self.summary_card)
        
        # Filters
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)
        
        # Date range
        date_label = QLabel("From:")
        filter_layout.addWidget(date_label)
        
        self.from_date_input = QDateEdit()
        self.from_date_input.setCalendarPopup(True)
        self.from_date_input.setDate(QDate.currentDate().addMonths(-1))
        self.from_date_input.dateChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.from_date_input)
    
        to_label = QLabel("To:")
        filter_layout.addWidget(to_label)
        
        self.to_date_input = QDateEdit()
        self.to_date_input.setCalendarPopup(True)
        self.to_date_input.setDate(QDate.currentDate())
        self.to_date_input.dateChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.to_date_input)
        
        # Category filter
        category_label = QLabel("Category:")
        filter_layout.addWidget(category_label)
        
        self.category_filter = QComboBox()
        self.category_filter.addItems([
            "All", "Marketing", "Office", "Travel", "Utilities",
            "Salary", "Commission", "Legal", "Other"
        ])
        self.category_filter.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.category_filter)
        
        # Search
        search_label = QLabel("Search:")
        filter_layout.addWidget(search_label)
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search expenses...")
        self.search_input.textChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.search_input, 1)
        
        filter_layout.addStretch()
        layout.addLayout(filter_layout)
        
        # Table
        self.table = self.create_expenses_table()
        layout.addWidget(self.table)
        
        self.setLayout(layout)
    
    def create_summary_card(self):
        """Create expense summary card."""
        frame = QFrame()
        frame.setObjectName("summaryCard")
        frame.setFrameShape(QFrame.Box)
        
        card_layout = QHBoxLayout()
        card_layout.setContentsMargins(20, 15, 20, 15)
        card_layout.setSpacing(30)
        
        # This Month
        month_layout = QVBoxLayout()
        month_layout.setSpacing(5)
        month_label = QLabel("This Month")
        month_label.setObjectName("cardTitle")
        month_layout.addWidget(month_label)
        
        self.month_value = QLabel("₹0")
        self.month_value.setObjectName("cardValue")
        value_font = QFont()
        size = 18
        if size <= 0:
            size = 12
        value_font.setPointSize(size)
        value_font.setBold(True)
        self.month_value.setFont(value_font)
        month_layout.addWidget(self.month_value)
        card_layout.addLayout(month_layout)
        
        # Last Month
        last_month_layout = QVBoxLayout()
        last_month_layout.setSpacing(5)
        last_month_label = QLabel("Last Month")
        last_month_label.setObjectName("cardTitle")
        last_month_layout.addWidget(last_month_label)
        
        self.last_month_value = QLabel("₹0")
        self.last_month_value.setObjectName("cardValue")
        self.last_month_value.setFont(value_font)
        last_month_layout.addWidget(self.last_month_value)
        card_layout.addLayout(last_month_layout)
        
        # Selected Period
        period_layout = QVBoxLayout()
        period_layout.setSpacing(5)
        period_label = QLabel("Selected Period")
        period_label.setObjectName("cardTitle")
        period_layout.addWidget(period_label)
        
        self.period_value = QLabel("₹0")
        self.period_value.setObjectName("cardValue")
        self.period_value.setFont(value_font)
        period_layout.addWidget(self.period_value)
        card_layout.addLayout(period_layout)
        
        card_layout.addStretch()
        frame.setLayout(card_layout)
        return frame
    
    def create_expenses_table(self):
        """Create the expenses table widget."""
        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels([
            "Date", "Title", "Category", "Sub-Category", "Amount", "Payment Type", "Vendor"
        ])
        
        # Configure table
        table.setSelectionBehavior(QTableWidget.SelectRows)
        table.setEditTriggers(QTableWidget.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        table.setAlternatingRowColors(True)
        
        # Column widths
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # Date
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # Title
        header.setSectionResizeMode(2, QHeaderView.ResizeToContents)  # Category
        header.setSectionResizeMode(3, QHeaderView.ResizeToContents)  # Sub-Category
        header.setSectionResizeMode(4, QHeaderView.ResizeToContents)  # Amount
        header.setSectionResizeMode(5, QHeaderView.ResizeToContents)  # Payment Type
        header.setSectionResizeMode(6, QHeaderView.Stretch)  # Vendor
        
        # Double click to view details
        table.doubleClicked.connect(self.view_expense_details)
        
        return table
    
    def load_data(self):
        """Load expenses data."""
        try:
            # Load summaries
            from_date = self.from_date_input.date().toPython()
            to_date = self.to_date_input.date().toPython()
            
            # Current month
            current_date = datetime.now()
            month_total = self.expense_service.get_monthly_total(
                current_date.year, current_date.month
            )
            self.month_value.setText(self.format_currency(month_total))
            
            # Last month
            if current_date.month == 1:
                last_month = 12
                last_year = current_date.year - 1
            else:
                last_month = current_date.month - 1
                last_year = current_date.year
            
            last_month_total = self.expense_service.get_monthly_total(last_year, last_month)
            self.last_month_value.setText(self.format_currency(last_month_total))
            
            # Load expenses
            self.all_expenses = self.expense_service.get_by_date_range(from_date, to_date)
            self.filter_and_display()

            
        except Exception as e:
            print(f"Error loading expenses: {e}")
            QMessageBox.warning(self, "Error", f"Failed to load expenses: {str(e)}")
    
    def populate_table(self, expenses):
        """Populate the table with expenses data."""
        self.table.setRowCount(0)
        total = 0
        
        for expense in expenses:
            row = self.table.rowCount()
            self.table.insertRow(row)
            
            # Date
            date_str = expense.expense_date.strftime('%d %b %Y')
            self.table.setItem(row, 0, QTableWidgetItem(date_str))
            
            # Title
            self.table.setItem(row, 1, QTableWidgetItem(expense.title))
            
            # Category
            category = expense.category.replace('_', ' ').title()
            self.table.setItem(row, 2, QTableWidgetItem(category))
            
            # Sub-Category
            sub_cat = expense.sub_category or '-'
            self.table.setItem(row, 3, QTableWidgetItem(sub_cat))
            
            # Amount
            amount_str = self.format_currency(expense.amount)
            amount_item = QTableWidgetItem(amount_str)
            amount_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
            self.table.setItem(row, 4, amount_item)
            total += expense.amount
            
            # Payment Type
            payment_type = expense.payment_type.replace('_', ' ').title()
            self.table.setItem(row, 5, QTableWidgetItem(payment_type))
            
            # Vendor
            vendor = expense.vendor_name or '-'
            self.table.setItem(row, 6, QTableWidgetItem(vendor))
            
            # Store expense_id
            self.table.item(row, 0).setData(Qt.UserRole, expense.id)
        
        # Update period total
        self.period_value.setText(self.format_currency(total))
    
    def view_expense_details(self, index):
        """Open edit dialog for the selected expense."""
        from modules.expenses.ui.expense_dialog import ExpenseDialog
        
        row = index.row()
        item = self.table.item(row, 0)
        
        if not item:
            return
        
        expense_id = item.data(Qt.UserRole)
        if not expense_id:
            return
        
        try:
            expense = self.expense_service.get_by_id(expense_id)
            if expense:
                dialog = ExpenseDialog(self.expense_service, expense=expense, parent=self)
                if dialog.exec():
                    self.refresh()
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            print(f"\n=== ERROR in expense details ===")
            print(f"Error: {e}")
            print(f"Traceback:\n{error_details}")
            print("=" * 50)
            QMessageBox.warning(self, "Error", f"Failed to open expense:\n{str(e)}\n\nCheck console for details")
    def add_expense(self):
        """Open add expense dialog."""
        from modules.expenses.ui.expense_dialog import ExpenseDialog
        
        dialog = ExpenseDialog(self.expense_service, parent=self)
        if dialog.exec():
            self.refresh()
    
    def apply_filters(self):
        """Apply filters without reloading summaries."""
        self.filter_and_display()
    
    def format_currency(self, amount):
        """Format amount as Indian currency."""
        if amount >= 10000000:  # 1 Crore
            return f"₹{amount/10000000:.2f} Cr"
        elif amount >= 100000:  # 1 Lakh
            return f"₹{amount/100000:.2f} L"
        elif amount >= 1000:
            return f"₹{amount/1000:.1f}K"
        else:
            return f"₹{amount:,.0f}"
    
    def refresh(self):
        """Refresh the expenses data."""
        self.load_data()
    
    def filter_and_display(self):
        """Filter expenses based on category and search text."""
        if not hasattr(self, "all_expenses"):
            return

        category_filter = self.category_filter.currentText().lower()
        search_text = self.search_input.text().lower().strip()

        filtered = []
        total = 0

        for expense in self.all_expenses:
            # Category filter
            if category_filter != "all" and expense.category.lower() != category_filter:
                continue

            # Search filter (title, vendor, description)
            if search_text:
                haystack = f"{expense.title} {expense.vendor_name or ''} {expense.description or ''}".lower()
                if search_text not in haystack:
                    continue

            filtered.append(expense)
            total += expense.amount

        self.populate_table(filtered)
        self.period_value.setText(self.format_currency(total))

