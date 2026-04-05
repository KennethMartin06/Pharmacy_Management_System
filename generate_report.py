from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, PageBreak, Image)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
import os

W, H = A4
DARK  = colors.HexColor('#2c3e50')
BLUE  = colors.HexColor('#3498db')
LGRAY = colors.HexColor('#f4f4f4')
WHITE = colors.white

styles = getSampleStyleSheet()

def mks(name, **kw):
    return ParagraphStyle(name, parent=styles.get('Normal', styles['Normal']), **kw)

T_TITLE = mks('ttl', fontName='Helvetica-Bold', fontSize=22, textColor=DARK,
               alignment=TA_CENTER, spaceAfter=8, leading=28)
T_SUB   = mks('sub', fontName='Helvetica', fontSize=12,
               textColor=colors.HexColor('#7f8c8d'), alignment=TA_CENTER, spaceAfter=6)
T_H1    = mks('h1',  fontName='Helvetica-Bold', fontSize=13, textColor=WHITE,
               spaceAfter=4, spaceBefore=12, leading=18, leftIndent=0)
T_H2    = mks('h2',  fontName='Helvetica-Bold', fontSize=11, textColor=DARK,
               spaceAfter=3, spaceBefore=8, leading=15)
T_BODY  = mks('bd',  fontName='Helvetica', fontSize=10, leading=14,
               spaceAfter=5, alignment=TA_JUSTIFY)
T_BUL   = mks('bl',  fontName='Helvetica', fontSize=10, leading=14,
               spaceAfter=2, leftIndent=20)
T_CODE  = mks('cd',  fontName='Courier', fontSize=7.5, leading=10.5,
               backColor=LGRAY, leftIndent=6, rightIndent=6, spaceAfter=8, spaceBefore=2)
T_CELL  = mks('cl',  fontName='Helvetica', fontSize=10, leading=13)
T_CELLB = mks('clb', fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=WHITE)

COLW = W - 5*cm

def sec_hdr(text):
    tbl = Table([[Paragraph(text, T_H1)]], colWidths=[COLW])
    tbl.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),DARK),
        ('TOPPADDING',(0,0),(-1,-1),6),
        ('BOTTOMPADDING',(0,0),(-1,-1),6),
        ('LEFTPADDING',(0,0),(-1,-1),10),
    ]))
    return tbl

def sub_hdr(text):
    return Paragraph(text, T_H2)

def body(text):
    safe = text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    return Paragraph(safe, T_BODY)

def bul(text):
    safe = text.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
    return Paragraph('• ' + safe, T_BUL)

def code(text):
    rows = []
    for line in text.split('\n'):
        safe = line.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
        rows.append([Paragraph(safe, T_CODE)])
    t = Table(rows, colWidths=[COLW])
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,-1),LGRAY),
        ('TOPPADDING',(0,0),(-1,-1),1),
        ('BOTTOMPADDING',(0,0),(-1,-1),1),
        ('LEFTPADDING',(0,0),(-1,-1),8),
        ('RIGHTPADDING',(0,0),(-1,-1),4),
        ('BOX',(0,0),(-1,-1),0.5,colors.HexColor('#cccccc')),
    ]))
    return t

def sp(n=6):
    return Spacer(1, n)

def screenshot(filename, caption):
    base = os.path.splitext(filename)[0]
    folder = '/home/user/Pharmacy_management_system/screenshots/'
    path = None
    for ext in [os.path.splitext(filename)[1], '.png', '.jpg', '.jpeg']:
        candidate = os.path.join(folder, base + ext)
        if os.path.exists(candidate):
            path = candidate
            break
    elems = [sub_hdr(caption)]
    if path:
        img = Image(path, width=COLW, height=COLW*0.62)
        elems.append(img)
    else:
        elems.append(body(f'[Screenshot: {caption}]'))
    elems.append(sp(10))
    return elems

def simple_table(headers, rows, col_widths=None):
    data = [[Paragraph(h, T_CELLB) for h in headers]]
    for r in rows:
        data.append([Paragraph(str(c), T_CELL) for c in r])
    if not col_widths:
        col_widths = [COLW / len(headers)] * len(headers)
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),DARK),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.HexColor('#ecf0f1'), WHITE]),
        ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#bdc3c7')),
        ('TOPPADDING',(0,0),(-1,-1),5),
        ('BOTTOMPADDING',(0,0),(-1,-1),5),
        ('LEFTPADDING',(0,0),(-1,-1),8),
        ('ALIGN',(0,0),(-1,-1),'LEFT'),
    ]))
    return t

def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(DARK)
    canvas.rect(doc.leftMargin, H - 1.5*cm, COLW, 1.2*cm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont('Helvetica-Bold', 9)
    canvas.drawString(doc.leftMargin + 10, H - 0.95*cm,
                      'PharmaCare - Pharmacy Management System')
    canvas.setFillColor(colors.HexColor('#7f8c8d'))
    canvas.setFont('Helvetica', 8)
    canvas.drawCentredString(W/2, 0.6*cm, f'Page {doc.page}')
    canvas.restoreState()

def read_java(rel_path):
    full = os.path.join('/home/user/Pharmacy_management_system/src', rel_path)
    with open(full, 'r', encoding='utf-8') as f:
        return f.read()

OUT = '/home/user/Pharmacy_management_system/PharmacyManagementSystem_Report.pdf'
doc = SimpleDocTemplate(OUT, pagesize=A4,
                        leftMargin=2.5*cm, rightMargin=2.5*cm,
                        topMargin=2.2*cm, bottomMargin=1.8*cm)

story = []

# ── TITLE PAGE ─────────────────────────────────────────────────────────────
story += [sp(40)]
story.append(Paragraph('PHARMACY MANAGEMENT SYSTEM', T_TITLE))
story.append(Paragraph('Object-Oriented Programming - Mini Project Report', T_SUB))
story += [sp(8)]
story.append(Paragraph('Submitted in partial fulfillment of the requirements for the', T_SUB))
story.append(Paragraph('Bachelor of Technology in Computer Science and Engineering', T_SUB))
story += [sp(20)]

info_data = [
    [Paragraph('Project Title', T_CELLB), Paragraph('Pharmacy Management System', T_CELL)],
    [Paragraph('Subject', T_CELLB),       Paragraph('Object-Oriented Programming (OOP)', T_CELL)],
    [Paragraph('Academic Year', T_CELLB), Paragraph('2025 - 2026', T_CELL)],
]
info_tbl = Table(info_data, colWidths=[COLW*0.35, COLW*0.65])
info_tbl.setStyle(TableStyle([
    ('BACKGROUND',(0,0),(0,-1),DARK),
    ('BACKGROUND',(1,0),(1,-1),colors.HexColor('#ecf0f1')),
    ('GRID',(0,0),(-1,-1),0.4,colors.HexColor('#bdc3c7')),
    ('TOPPADDING',(0,0),(-1,-1),6), ('BOTTOMPADDING',(0,0),(-1,-1),6),
    ('LEFTPADDING',(0,0),(-1,-1),10),
]))
story.append(info_tbl)
story += [sp(20)]

story.append(Paragraph('Team Members', mks('tmh', fontName='Helvetica-Bold', fontSize=12,
                                            textColor=DARK, alignment=TA_CENTER, spaceAfter=6)))
team_tbl = simple_table(
    ['Name', 'Register Number', 'Roll No.'],
    [['Kenneth Martin',        '240962047', '8'],
     ['Sam Thomas',            '240962242', '18'],
     ['Mohammed Rayyan Sheik', '240962073', '12'],
     ['Vedank Singh',          '240962043', '7']],
    [COLW*0.50, COLW*0.30, COLW*0.20]
)
story.append(team_tbl)
story.append(PageBreak())

# ── INTRODUCTION ───────────────────────────────────────────────────────────
story.append(sec_hdr('Introduction'))
story += [sp(6)]
story.append(body(
    'The objective of this project is to design and implement a Pharmacy Management System (PMS) '
    'using Java and JavaFX to manage medicine inventory, customer records, billing transactions, '
    'supplier details, and prescription handling. This system enables pharmacy staff to register '
    'and manage medicines in stock, generate bills and invoices for customers, handle prescriptions '
    'provided by doctors, and receive automated alerts for low stock or expiring medicines. '
    'The system also focuses on ensuring secure data handling through role-based access control '
    'and persistent file-based storage using Java Serialization.'
))

# ── PROBLEM STATEMENT ──────────────────────────────────────────────────────
story += [sp(4)]
story.append(sec_hdr('Problem Statement'))
story += [sp(6)]
story.append(sub_hdr('Pharmacy Management System with Inventory Control and Billing Automation'))
story.append(body(
    'Manual pharmacy operations are heavily dependent on paper-based records, leading to '
    'frequent billing errors, poor stock management, and difficulty in tracking medicine '
    'availability and expiry. Patients may receive incorrect medicines due to outdated records. '
    'There is no automated mechanism to alert staff about low stock or expired medicines. '
    'The Pharmacy Management System aims to automate and digitize all core pharmacy operations, '
    'improving accuracy, efficiency, and reliability.'
))

# ── IMPLEMENTATION DETAILS ─────────────────────────────────────────────────
story.append(sec_hdr('Implementation Details'))
story += [sp(6)]
story.append(body(
    'This project was implemented in the Java programming language using JavaFX for the '
    'graphical user interface. The application utilizes object-oriented programming principles '
    'to manage pharmacy operations effectively. The project contains 32 Java source files '
    'organized into four packages: model, service, ui, and util.'
))
story.append(body('The complete list of source files is:'))

all_files = [
    # model
    'com/pharmacy/model/Medicine.java',
    'com/pharmacy/model/MedicineCategory.java',
    'com/pharmacy/model/UserRole.java',
    'com/pharmacy/model/Customer.java',
    'com/pharmacy/model/Supplier.java',
    'com/pharmacy/model/Bill.java',
    'com/pharmacy/model/BillItem.java',
    'com/pharmacy/model/Prescription.java',
    'com/pharmacy/model/PrescriptionItem.java',
    'com/pharmacy/model/User.java',
    # service
    'com/pharmacy/service/InventoryManager.java',
    'com/pharmacy/service/BillingService.java',
    'com/pharmacy/service/CustomerService.java',
    'com/pharmacy/service/SupplierService.java',
    'com/pharmacy/service/PrescriptionService.java',
    'com/pharmacy/service/UserService.java',
    'com/pharmacy/service/ExpiryAlertThread.java',
    'com/pharmacy/service/StockAlertThread.java',
    'com/pharmacy/service/BillingThread.java',
    'com/pharmacy/service/BackupService.java',
    # ui
    'com/pharmacy/ui/PharmacyApp.java',
    'com/pharmacy/ui/LoginScreen.java',
    'com/pharmacy/ui/DashboardScreen.java',
    'com/pharmacy/ui/InventoryScreen.java',
    'com/pharmacy/ui/BillingScreen.java',
    'com/pharmacy/ui/SupplierScreen.java',
    'com/pharmacy/ui/CustomerScreen.java',
    'com/pharmacy/ui/PrescriptionScreen.java',
    'com/pharmacy/ui/ReportsScreen.java',
    # util
    'com/pharmacy/util/DataStore.java',
    'com/pharmacy/util/IDGenerator.java',
    'com/pharmacy/util/SampleDataLoader.java',
]

for f in all_files:
    story.append(bul(f.split('/')[-1]))

story += [sp(8)]

# ── FILE DESCRIPTIONS ──────────────────────────────────────────────────────
file_descriptions = {
    'Medicine.java':
        'Main model representing a medicine/drug item. Implements Serializable and '
        'Comparable<Medicine>. Uses Integer and Double wrapper classes with autoboxing/unboxing. '
        'Has constructor overloading (with and without supplierId) and a compareTo() method '
        'enabling Collections.sort() by medicine name.',
    'MedicineCategory.java':
        'Enum defining the available medicine categories: TABLET, CAPSULE, SYRUP, INJECTION, '
        'OINTMENT, DROPS, INHALER, and POWDER. Demonstrates the use of Java enumerations.',
    'UserRole.java':
        'Enum defining user roles in the system: ADMIN and PHARMACIST. Used for role-based '
        'access control throughout the application.',
    'Customer.java':
        'Model class representing a pharmacy customer. Implements Serializable for persistent '
        'storage. Contains customerId, name, phone, email, and address fields with getters/setters.',
    'Supplier.java':
        'Model class representing a medicine supplier. Implements Serializable. Contains '
        'supplierId, companyName, contactPerson, phone, email, and address fields.',
    'Bill.java':
        'Model class representing a billing transaction. Contains overloaded applyDiscount() '
        'methods demonstrating method overloading. Stores bill items, total amount, and date.',
    'BillItem.java':
        'Represents a single line item in a bill. Uses Integer for quantity and Double for '
        'unitPrice and subtotal, demonstrating wrapper classes and autoboxing.',
    'Prescription.java':
        'Represents a medical prescription issued to a customer. Contains a list of '
        'PrescriptionItem objects and links to the customer and prescribing doctor.',
    'PrescriptionItem.java':
        'Represents a single medicine entry within a prescription, including medicine name, '
        'dosage, and quantity instructions.',
    'User.java':
        'Represents a system user with username, password, fullName, and UserRole. Contains '
        'an authenticate() method that validates login credentials.',
    'InventoryManager.java':
        'Core service class managing the medicine inventory. Uses ArrayList for ordered storage '
        'and HashMap for fast lookup. All write methods are synchronized for thread safety. '
        'Uses Iterator for safe deletion, and Collections.sort() with both Comparable and '
        'Comparator for flexible sorting.',
    'BillingService.java':
        'Handles all billing operations: creating bills, adding items, calculating totals, '
        'applying discounts, and generating invoice text files using FileWriter. All methods '
        'are synchronized.',
    'CustomerService.java':
        'Provides CRUD operations for customer records using ArrayList and HashMap. Uses '
        'Iterator for safe removal. Persists data using DataStore serialization.',
    'SupplierService.java':
        'Provides CRUD operations for supplier records using ArrayList and HashMap. Uses '
        'Iterator for safe removal. Persists data using DataStore serialization.',
    'PrescriptionService.java':
        'Manages prescription records with full CRUD support. Uses ArrayList and HashMap, '
        'Iterator for deletion, and DataStore for serialized persistence.',
    'UserService.java':
        'Handles user authentication and management. Creates default admin and pharmacist '
        'accounts on first run. Validates credentials using User.authenticate().',
    'ExpiryAlertThread.java':
        'Background thread that monitors medicines approaching their expiry date. Extends the '
        'Thread class directly, runs as a daemon thread, uses sleep(30000) to check every 30 '
        'seconds, and uses wait()/notify() for synchronization.',
    'StockAlertThread.java':
        'Background thread that monitors low stock levels. Implements the Runnable interface '
        '(second threading approach). Uses a volatile boolean flag for graceful shutdown and '
        'a synchronized checkStock() method.',
    'BillingThread.java':
        'Processes billing operations asynchronously. Extends Thread and uses sleep() and '
        'join(). Defines a BillingCallback inner interface for returning results to the UI '
        'thread via Platform.runLater().',
    'BackupService.java':
        'Implements Runnable to perform periodic data backups. Calls DataStore.backupToText() '
        'for all five service classes to write human-readable backup files.',
    'PharmacyApp.java':
        'Main JavaFX Application entry point. Extends Application and overrides start(). '
        'Initializes all service objects, starts background threads, loads sample data on '
        'first run, and manages screen navigation using Stage.setScene().',
    'LoginScreen.java':
        'Login interface built with GridPane. Uses PasswordField to mask passwords and '
        'validates credentials via UserService. Supports Admin and Pharmacist roles and '
        'redirects to the Dashboard on successful login.',
    'DashboardScreen.java':
        'Main dashboard displayed after login. Uses BorderPane with an HBox top bar and a '
        'GridPane of six navigation buttons. Displays the logged-in user\'s name and role, '
        'and provides a Logout button.',
    'InventoryScreen.java':
        'Full inventory management screen with a TableView showing all medicines. Provides '
        'Add, Edit, Delete, Search by name, and Filter by category using a ComboBox. Supports '
        'sorting by clicking column headers.',
    'BillingScreen.java':
        'Billing and sales screen. Allows staff to select a customer, add medicine items to '
        'a bill, apply discounts, and process payment. Uses BillingThread for async processing '
        'and Platform.runLater() to safely update the UI.',
    'SupplierScreen.java':
        'Supplier management screen with a TableView and full CRUD operations. Allows adding, '
        'editing, and deleting supplier records with input validation.',
    'CustomerScreen.java':
        'Customer records screen with a TableView and full CRUD operations. Allows adding, '
        'editing, and deleting customer records with input validation.',
    'PrescriptionScreen.java':
        'Prescription handling screen. Displays prescriptions in a ListView and shows details '
        'in a TextArea. Allows creating new prescriptions with medicine items.',
    'ReportsScreen.java':
        'Reports and backup screen. Shows summary statistics (medicine count, customer count, '
        'bill count) as cards. Provides a Backup button that triggers BackupService in a new '
        'Thread. Also shows low stock and expiry alerts.',
    'DataStore.java':
        'Generic utility class DataStore<T extends Serializable> that handles all persistence. '
        'saveAll() serializes an ArrayList using ObjectOutputStream + FileOutputStream. '
        'loadAll() deserializes using ObjectInputStream + FileInputStream. backupToText() '
        'writes readable text using FileWriter. readBackup() reads with FileReader. All methods '
        'are synchronized.',
    'IDGenerator.java':
        'Utility class with synchronized static methods for generating unique IDs. Generates '
        'IDs in the format MED-001, CUS-001, SUP-001, BIL-001, PRE-001 using an internal '
        'counter for each type.',
    'SampleDataLoader.java':
        'Utility class that loads sample data on the first run of the application. Adds 10 '
        'medicines, 3 customers, and 3 suppliers so the system has data to demonstrate.',
}

# ── DETAILED EXPLANATION OF EACH FILE ─────────────────────────────────────
story.append(sec_hdr('Detailed Explanation of Each File'))
story += [sp(6)]

# Group labels
groups = [
    ('Model Package (com.pharmacy.model)', [
        'com/pharmacy/model/Medicine.java',
        'com/pharmacy/model/MedicineCategory.java',
        'com/pharmacy/model/UserRole.java',
        'com/pharmacy/model/Customer.java',
        'com/pharmacy/model/Supplier.java',
        'com/pharmacy/model/Bill.java',
        'com/pharmacy/model/BillItem.java',
        'com/pharmacy/model/Prescription.java',
        'com/pharmacy/model/PrescriptionItem.java',
        'com/pharmacy/model/User.java',
    ]),
    ('Service Package (com.pharmacy.service)', [
        'com/pharmacy/service/InventoryManager.java',
        'com/pharmacy/service/BillingService.java',
        'com/pharmacy/service/CustomerService.java',
        'com/pharmacy/service/SupplierService.java',
        'com/pharmacy/service/PrescriptionService.java',
        'com/pharmacy/service/UserService.java',
        'com/pharmacy/service/ExpiryAlertThread.java',
        'com/pharmacy/service/StockAlertThread.java',
        'com/pharmacy/service/BillingThread.java',
        'com/pharmacy/service/BackupService.java',
    ]),
    ('UI Package (com.pharmacy.ui)', [
        'com/pharmacy/ui/PharmacyApp.java',
        'com/pharmacy/ui/LoginScreen.java',
        'com/pharmacy/ui/DashboardScreen.java',
        'com/pharmacy/ui/InventoryScreen.java',
        'com/pharmacy/ui/BillingScreen.java',
        'com/pharmacy/ui/SupplierScreen.java',
        'com/pharmacy/ui/CustomerScreen.java',
        'com/pharmacy/ui/PrescriptionScreen.java',
        'com/pharmacy/ui/ReportsScreen.java',
    ]),
    ('Util Package (com.pharmacy.util)', [
        'com/pharmacy/util/DataStore.java',
        'com/pharmacy/util/IDGenerator.java',
        'com/pharmacy/util/SampleDataLoader.java',
    ]),
]

file_num = 1
for group_title, file_list in groups:
    story.append(Paragraph(group_title, mks(f'grp_{file_num}',
        fontName='Helvetica-Bold', fontSize=12, textColor=BLUE,
        spaceBefore=14, spaceAfter=6, leading=16)))
    for rel_path in file_list:
        fname = rel_path.split('/')[-1]
        desc  = file_descriptions.get(fname, '')
        story.append(sub_hdr(f'{file_num}. {fname}'))
        if desc:
            story.append(body(desc))
        story.append(body(f'Code for {fname}:'))
        src = read_java(rel_path)
        story.append(code(src))
        story += [sp(6)]
        file_num += 1
        print(f'  Added {fname}')

print("Code sections done")

# ── RESULTS ────────────────────────────────────────────────────────────────
story.append(PageBreak())
story.append(sec_hdr('Results'))
story += [sp(6)]

for fname, caption in [
    ('login.png',        'Login Screen'),
    ('login2.png',       'Login Screen - with Credentials'),
    ('dashboard.png',    'Dashboard Screen'),
    ('inventory.png',    'Inventory Management Screen'),
    ('billing.png',      'Sales and Billing Screen'),
    ('supplier.png',     'Supplier Management Screen'),
    ('customer.png',     'Customer Records Screen'),
    ('prescription.png', 'Prescription Handling Screen'),
    ('reports.png',      'Reports and Alerts Screen'),
]:
    for elem in screenshot(fname, caption):
        story.append(elem)

# ── CONCLUSION ─────────────────────────────────────────────────────────────
story.append(PageBreak())
story.append(sec_hdr('Conclusion'))
story += [sp(6)]
story.append(body(
    'The Pharmacy Management System (PMS) provides an efficient and reliable platform for '
    'pharmacy staff to manage medicine inventory, process billing transactions, maintain '
    'customer and supplier records, handle prescriptions, and generate automated alerts for '
    'expiring or low-stock medicines. Using Java and JavaFX, the system delivers a clean, '
    'intuitive graphical interface that makes it easy for both administrators and pharmacists '
    'to interact with their data securely and accurately.'
))
story.append(body(
    'By integrating role-based access control, unique auto-generated IDs for each record, '
    'and synchronized thread-safe service methods, the PMS ensures that data integrity is '
    'preserved even under concurrent access conditions. The use of background threads for '
    'expiry and stock monitoring, combined with automatic invoice generation using FileWriter, '
    'makes the system both proactive and practical for day-to-day pharmacy operations.'
))
story.append(body(
    'Overall, the PMS successfully demonstrates how object-oriented programming principles '
    '- Encapsulation, Inheritance, Polymorphism, and Abstraction - along with Java Collections, '
    'Generics, Multithreading, File Handling, and Serialization can be applied to solve '
    'real-world problems in healthcare management, resulting in a secure, modular, and '
    'scalable solution.'
))

# ── INDIVIDUAL CONTRIBUTIONS ───────────────────────────────────────────────
story.append(sec_hdr('Individual Contributions'))
story += [sp(6)]

contribs = [
    ('Kenneth Martin, 240962047, Roll No. 8',
     ['PharmacyApp.java', 'LoginScreen.java', 'DashboardScreen.java',
      'UserService.java', 'User.java / UserRole.java']),
    ('Sam Thomas, 240962242, Roll No. 18',
     ['Medicine.java / MedicineCategory.java', 'InventoryManager.java',
      'InventoryScreen.java', 'SampleDataLoader.java']),
    ('Mohammed Rayyan Sheik, 240962073, Roll No. 12',
     ['BillingService.java', 'BillingThread.java',
      'BillingScreen.java', 'Bill.java / BillItem.java']),
    ('Vedank Singh, 240962043, Roll No. 7',
     ['DataStore.java', 'IDGenerator.java',
      'CustomerService.java / SupplierService.java',
      'PrescriptionService.java',
      'ExpiryAlertThread.java / StockAlertThread.java',
      'BackupService.java', 'ReportsScreen.java',
      'Supplier.java / Customer.java / Prescription.java / PrescriptionItem.java / BillItem.java']),
]

for name, files in contribs:
    story.append(Paragraph(name, mks('cname', fontName='Helvetica-Bold', fontSize=11,
                                      textColor=DARK, spaceBefore=8, spaceAfter=3)))
    for f in files:
        story.append(bul(f))

story += [sp(8)]
story.append(body(
    'While project tasks were divided among the team members, we collaborated closely at every '
    'stage, discussing and refining our design decisions together. Since this system strictly '
    'follows Object-Oriented Programming principles, each file is interdependent, requiring '
    'continuous communication and coordination to ensure seamless integration across all classes '
    'and modules. By regularly reviewing each other\'s work and resolving challenges '
    'collaboratively, we maintained consistency in design and functionality, resulting in a '
    'unified and robust Pharmacy Management System.'
))

# ── REFERENCES ─────────────────────────────────────────────────────────────
story.append(sec_hdr('References'))
story += [sp(6)]
refs = [
    'JavaFX Official Documentation: https://openjfx.io/',
    'JavaFX Tutorials and Codes: https://www.geeksforgeeks.org/tag/javafx/',
    'Java Serialization Guide: https://www.baeldung.com/java-serialization',
    'Java Collections Framework: https://docs.oracle.com/javase/8/docs/technotes/guides/collections/overview.html',
    'Java Multithreading: https://www.geeksforgeeks.org/multithreading-in-java/',
]
for i, ref in enumerate(refs, 1):
    story.append(bul(f'{i}. {ref}'))

# ── BUILD PDF ──────────────────────────────────────────────────────────────
doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"PDF generated successfully: {OUT}")
