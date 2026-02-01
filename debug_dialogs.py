#!/usr/bin/env python3
"""
Debug Script for Real Estate MIS
Tests all dialog operations to identify issues
"""
import sys
import os

# Add project root to path
sys.path.insert(0, '/home/claude/MIS_FIXED')

from PySide6.QtWidgets import QApplication

# Initialize Qt Application
app = QApplication(sys.argv)

print("="*70)
print("REAL ESTATE MIS - DIALOG DEBUGGING SCRIPT")
print("="*70)

# Test 1: Import all modules
print("\n[TEST 1] Importing all modules...")
try:
    from core.database import db_manager
    from modules.clients.repositories.client_repository import ClientRepository
    from modules.clients.services.client_service import ClientService
    from modules.partners.repositories.partner_repository import PartnerRepository
    from modules.partners.services.partner_service import PartnerService
    from modules.expenses.repositories.expense_repository import ExpenseRepository
    from modules.expenses.services.expense_service import ExpenseService
    from modules.actions.repositories.action_repository import ActionRepository
    from modules.actions.services.action_service import ActionService
    from modules.commission.repositories.commission_repository import CommissionRepository
    from modules.commission.services.commission_service import CommissionService
    from modules.deals.repositories.deal_repository import DealRepository
    from modules.deals.services.deal_service import DealService
    print("✓ All modules imported successfully")
except Exception as e:
    print(f"✗ Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 2: Initialize services
print("\n[TEST 2] Initializing services...")
try:
    client_service = ClientService(ClientRepository())
    partner_service = PartnerService(PartnerRepository())
    expense_service = ExpenseService(ExpenseRepository())
    action_service = ActionService(ActionRepository())
    commission_service = CommissionService(CommissionRepository())
    deal_service = DealService(DealRepository())
    print("✓ All services initialized successfully")
except Exception as e:
    print(f"✗ Service initialization error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Test service methods
print("\n[TEST 3] Testing service methods...")

# Test client service
print("\n  Testing ClientService...")
try:
    # Test get_all
    clients = client_service.get_all()
    print(f"    ✓ get_all() returned {len(clients)} clients")
    
    # Test create method signature
    import inspect
    create_sig = inspect.signature(client_service.create)
    print(f"    ✓ create signature: {create_sig}")
    
    update_sig = inspect.signature(client_service.update)
    print(f"    ✓ update signature: {update_sig}")
    
except Exception as e:
    print(f"    ✗ Error: {e}")
    import traceback
    traceback.print_exc()

# Test partner service
print("\n  Testing PartnerService...")
try:
    partners = partner_service.get_all()
    print(f"    ✓ get_all() returned {len(partners)} partners")
    
    create_sig = inspect.signature(partner_service.create)
    print(f"    ✓ create signature: {create_sig}")
    
    update_sig = inspect.signature(partner_service.update)
    print(f"    ✓ update signature: {update_sig}")
    
except Exception as e:
    print(f"    ✗ Error: {e}")

# Test expense service
print("\n  Testing ExpenseService...")
try:
    expenses = expense_service.get_all()
    print(f"    ✓ get_all() returned {len(expenses)} expenses")
    
    create_sig = inspect.signature(expense_service.create)
    print(f"    ✓ create signature: {create_sig}")
    
    update_sig = inspect.signature(expense_service.update)
    print(f"    ✓ update signature: {update_sig}")
    
except Exception as e:
    print(f"    ✗ Error: {e}")

# Test 4: Test dialog imports
print("\n[TEST 4] Testing dialog imports...")
try:
    from modules.clients.ui.client_dialog import ClientDialog
    print("  ✓ ClientDialog imported")
    
    from modules.partners.ui.partner_dialog import PartnerDialog
    print("  ✓ PartnerDialog imported")
    
    from modules.expenses.ui.expense_dialog import ExpenseDialog
    print("  ✓ ExpenseDialog imported")
    
    from modules.actions.ui.action_dialog import ActionDialog
    print("  ✓ ActionDialog imported")
    
    from modules.commission.ui.commission_dialog import CommissionDialog
    print("  ✓ CommissionDialog imported")
    
    from modules.deals.ui.add_deal_dialog import AddDealDialog
    print("  ✓ AddDealDialog imported")
    
except Exception as e:
    print(f"  ✗ Dialog import error: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Test dialog instantiation
print("\n[TEST 5] Testing dialog instantiation (without showing)...")
try:
    # Test ClientDialog
    dialog = ClientDialog(client_service, parent=None)
    print("  ✓ ClientDialog created successfully (add mode)")
    
    if len(clients) > 0:
        dialog = ClientDialog(client_service, client=clients[0], parent=None)
        print("  ✓ ClientDialog created successfully (edit mode)")
    
    # Test PartnerDialog
    dialog = PartnerDialog(partner_service, parent=None)
    print("  ✓ PartnerDialog created successfully (add mode)")
    
    # Test ExpenseDialog
    dialog = ExpenseDialog(expense_service, parent=None)
    print("  ✓ ExpenseDialog created successfully (add mode)")
    
    # Test ActionDialog
    dialog = ActionDialog(action_service, parent=None)
    print("  ✓ ActionDialog created successfully (add mode)")
    
    # Test CommissionDialog
    dialog = CommissionDialog(commission_service, parent=None)
    print("  ✓ CommissionDialog created successfully (add mode)")
    
    # Test AddDealDialog
    dialog = AddDealDialog(deal_service, parent=None)
    print("  ✓ AddDealDialog created successfully")
    
except Exception as e:
    print(f"  ✗ Dialog instantiation error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "="*70)
print("TESTING COMPLETE")
print("="*70)
print("\nIf all tests passed, the dialogs should work correctly.")
print("Run the actual application to test interactively.")
