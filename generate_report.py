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
    'Pharmacies handle a surprisingly large amount of data every day. From tracking which medicines '
    'are running low to generating bills for dozens of customers, the workload adds up fast. '
    'Most small and mid-sized pharmacies still rely on paper registers or basic spreadsheets, '
    'which honestly just creates more problems than it solves. Entries get missed, stock counts '
    'go wrong, and nobody notices a batch of medicines is about to expire until it\'s too late.'
))
story.append(body(
    'We built this Pharmacy Management System to fix exactly those kinds of problems. The system '
    'is written in Java, with a JavaFX-based desktop interface that any pharmacy staff member '
    'can use without much training. It covers the main things a pharmacy needs to keep track of: '
    'the medicine stock, customer records, supplier contacts, billing and invoices, and '
    'prescriptions from doctors. There\'s also a background alert system that automatically '
    'warns staff when stock is low or medicines are close to their expiry date, without anyone '
    'having to manually check.'
))
story.append(body(
    'From an academic standpoint, this project was a chance for us to apply the OOP concepts '
    'we\'ve been studying. Encapsulation, inheritance, polymorphism, abstraction, generics, '
    'multithreading, serialization, collections - every one of those is used somewhere in this '
    'codebase, not just as a checkbox but because it genuinely made the code cleaner and easier '
    'to manage. Data is saved between sessions using Java Serialization, and access is controlled '
    'by role so admins see everything while pharmacists only get what they need.'
))

# ── PROBLEM STATEMENT ──────────────────────────────────────────────────────
story += [sp(4)]
story.append(sec_hdr('Problem Statement'))
story += [sp(6)]
story.append(sub_hdr('Pharmacy Management System with Inventory Control and Billing Automation'))
story.append(body(
    'Walk into almost any small pharmacy and you\'ll likely see someone squinting at a handwritten '
    'stock register trying to figure out whether a particular medicine is still available. '
    'Billing is done on paper, which means calculation errors are common. Prescriptions get '
    'stacked in a drawer and there\'s no easy way to look one up later. And when a medicine '
    'expires on the shelf, nobody really knows until a customer points it out.'
))
story.append(body(
    'These aren\'t edge cases - they\'re everyday problems that affect patient safety and '
    'pharmacy efficiency. The goal of our project was to build a system that directly addresses '
    'these issues. Instead of paper records, everything is stored digitally and can be searched '
    'in seconds. Billing is automated so there are no arithmetic mistakes. Background threads '
    'continuously monitor stock levels and expiry dates, sending alerts before problems occur. '
    'The whole system is designed for the kind of pharmacy that doesn\'t have a dedicated IT '
    'team but still needs reliable software to run smoothly.'
))

# ── IMPLEMENTATION DETAILS ─────────────────────────────────────────────────
story.append(sec_hdr('Implementation Details'))
story += [sp(6)]
story.append(body(
    'The entire project is built in Java, using JavaFX for the graphical front-end. '
    'We organized everything into four packages - model, service, ui, and util - which kept '
    'the code from turning into a mess as it grew. There are 32 Java source files in total. '
    'The model package holds all the data classes. Service classes handle the actual logic '
    'and talk to the data layer. The ui package contains every screen in the application. '
    'And util has the shared helper stuff like ID generation and file persistence.'
))
story.append(body(
    'One design decision we made early on was to keep the service layer completely separate '
    'from the UI. That way the business logic doesn\'t get tangled up with button clicks and '
    'text fields, and it\'s much easier to test individual parts. We also made all write '
    'operations synchronized since the app runs background threads that could otherwise '
    'cause data corruption.'
))
story.append(body('All 32 source files in the project:'))

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
        'This is the core data class for a medicine item in the inventory. It implements both '
        'Serializable (so it can be saved to disk) and Comparable<Medicine> (so we can sort '
        'lists of medicines by name). We used Integer and Double wrapper classes for the '
        'quantity and price fields specifically to show autoboxing and unboxing in action. '
        'There are two constructors - one that takes a supplierId and one that doesn\'t - '
        'which covers constructor overloading. The compareTo() method is what powers '
        'Collections.sort() when we sort the inventory list.',
    'MedicineCategory.java':
        'A simple but useful enum for medicine types. Rather than storing category as a raw '
        'String (which is error-prone), we defined a proper enum with values like TABLET, '
        'CAPSULE, SYRUP, INJECTION, OINTMENT, DROPS, INHALER, and POWDER. Each value has '
        'a display-friendly name string attached. This gets used in the inventory form\'s '
        'dropdown and for filtering the inventory table by category.',
    'UserRole.java':
        'Another enum, this one for controlling what a logged-in user is allowed to do. '
        'ADMIN gets full access across the system while PHARMACIST has a more limited view. '
        'We stored the canManageUsers flag directly inside the enum so the permission check '
        'is just a method call rather than a series of if-else comparisons scattered around '
        'the codebase.',
    'Customer.java':
        'A straightforward model class for storing patient/customer information. It holds '
        'the customer ID, name, phone, email, and address. Implements Serializable so the '
        'CustomerService can persist the list to disk. Most of the code here is getters and '
        'setters plus a toString() that gives a readable summary line.',
    'Supplier.java':
        'Stores details about a medicine supplier company - the company name, a contact '
        'person\'s name, phone number, email, and address. Like all the model classes, it '
        'implements Serializable so the data survives application restarts. Supplier records '
        'are linked to medicines through the supplierId field in Medicine.java.',
    'Bill.java':
        'The billing model was one of the more interesting ones to design. It holds the full '
        'details of a transaction: customer info, date, who billed it, and an ArrayList of '
        'BillItem objects. The applyDiscount() method is overloaded twice - once that takes '
        'a percentage and one that takes an amount plus a boolean flag indicating whether '
        'it\'s a fixed amount or a percentage. That overloading was deliberate to cover the '
        'polymorphism requirement.',
    'BillItem.java':
        'Each individual line in a bill is a BillItem. It stores the medicine name, quantity '
        '(as Integer - wrapper class), unit price and subtotal (both Double - wrapper class). '
        'The subtotal is calculated in the constructor itself so it\'s always consistent. '
        'The autoboxing happens when we assign int/double literals to the Integer/Double fields.',
    'Prescription.java':
        'Represents a prescription that a doctor has issued for a patient. It links to a '
        'customer via customerId and holds the doctor\'s name, date, and any notes. The list '
        'of prescribed medicines is kept as an ArrayList<PrescriptionItem>. '
        'Implements Serializable for persistence through DataStore.',
    'PrescriptionItem.java':
        'Each line within a prescription is stored as a PrescriptionItem. It records which '
        'medicine, how many, and the dosage instructions (like "1-0-1" meaning once in the '
        'morning and once at night). Simple class but important for linking prescriptions '
        'to actual inventory items.',
    'User.java':
        'Represents someone who can log in to the system. Has a username, password, full name, '
        'and a UserRole enum. The authenticate() method checks whether a given password matches, '
        'which keeps the credential-checking logic inside the model rather than scattered '
        'across the login screen. Implements Serializable so user accounts persist.',
    'InventoryManager.java':
        'Probably the most used service class in the whole project. It manages the full list '
        'of medicines, stored in both an ArrayList (for ordered access) and a HashMap (for '
        'instant lookup by ID). Every method that changes data is synchronized since the '
        'expiry and stock alert threads also access this data in the background. Deletions '
        'use an Iterator to avoid ConcurrentModificationException. Sorting uses '
        'Collections.sort() in combination with compareTo() from the Comparable interface, '
        'and we added a Comparator-based sort for price and expiry date as well.',
    'BillingService.java':
        'Takes care of everything billing-related: creating new bills, saving them, '
        'calculating totals, and writing invoice files to disk. The invoice generation '
        'uses FileWriter, which is one of the File I/O requirements. We had a bug early on '
        'where the invoice used Unicode box-drawing characters that caused encoding errors '
        'on Windows machines, so we switched to plain ASCII borders instead. All public '
        'methods are synchronized.',
    'CustomerService.java':
        'Handles the full create, read, update, delete cycle for customer records. Under the '
        'hood it keeps an ArrayList for iteration order and a HashMap for fast lookups by ID. '
        'When deleting, it uses an Iterator rather than removing inside a for-each loop, '
        'which would throw an exception. The DataStore<Customer> instance handles saving '
        'everything to disk as a serialized file.',
    'SupplierService.java':
        'Same structure as CustomerService but for supplier records. CRUD operations backed '
        'by ArrayList + HashMap, Iterator used for deletion, and DataStore handles the '
        'serialized file storage. Also has a searchByName() method that does a '
        'case-insensitive substring search through the supplier list.',
    'PrescriptionService.java':
        'Manages prescription records. Add and delete operations are supported. The getByCustomerId() '
        'method is useful when you want to pull up all prescriptions for a specific patient. '
        'Like the other service classes, it delegates persistence entirely to DataStore<Prescription>.',
    'UserService.java':
        'Handles login validation and user management. On the very first run, when no users '
        'exist yet, it automatically creates a default admin and a default pharmacist account. '
        'The authenticate() method loops through the user list looking for a matching username '
        'and then calls User.authenticate() to check the password, keeping the logic clean.',
    'ExpiryAlertThread.java':
        'One of two background monitoring threads. This one extends the Thread class directly '
        '(the other uses Runnable, so we cover both approaches). It\'s marked as a daemon '
        'thread so it stops automatically when the main application closes. Every 30 seconds '
        'it wakes up via sleep(), checks the inventory for expired and about-to-expire medicines, '
        'and uses wait()/notify() so other threads can safely read the results.',
    'StockAlertThread.java':
        'The second monitoring thread, this time implementing Runnable rather than extending '
        'Thread directly. It checks for medicines with fewer than 10 units in stock and '
        'notifies a listener if any are found. A volatile boolean flag named "running" is '
        'used to stop the thread cleanly without calling interrupt() or using deprecated '
        'Thread.stop(). The checkStock() method is synchronized.',
    'BillingThread.java':
        'When a bill is ready to be processed, instead of doing everything on the JavaFX '
        'application thread (which would freeze the UI), we hand it off to a BillingThread. '
        'It extends Thread, sleeps for a bit to simulate processing time, then calls '
        'BillingService.createBill() inside a synchronized block. A BillingCallback interface '
        'is used to pass the result back to the UI. The UI then uses Platform.runLater() to '
        'update labels and tables safely. We also demonstrated join() by having a separate '
        'watcher thread wait for BillingThread to finish.',
    'BackupService.java':
        'Implements Runnable so it can be passed to any Thread or ExecutorService. When run, '
        'it calls createBackup() on each of the five service classes in sequence, with short '
        'sleep() calls between each one. This writes human-readable text copies of all the '
        'data into the data/ directory. A BackupCallback interface lets the UI show a '
        'completion message once the backup is done.',
    'PharmacyApp.java':
        'This is where the application starts. It extends JavaFX\'s Application class and '
        'the start() method sets everything up: all service objects are created, the expiry '
        'and stock alert threads are started, sample data is loaded on the first run, and '
        'the login screen is shown. Navigation between screens is handled through a '
        'showXxxScreen() pattern where each call to one of these methods creates a new scene '
        'and passes it to Stage.setScene().',
    'LoginScreen.java':
        'The first thing users see when they open the app. Built with a GridPane layout, '
        'PasswordField to keep the password hidden, and a Label that shows a red error '
        'message if login fails. After successful authentication through UserService, '
        'the user gets redirected to the dashboard. The role (Admin or Pharmacist) is '
        'stored in the User object that comes back from authentication.',
    'DashboardScreen.java':
        'After logging in, this is the home screen. It uses a BorderPane as the root, '
        'with a dark-colored HBox at the top showing the app name and the logged-in '
        'user\'s details. The center has a GridPane with six buttons, each leading to '
        'a different module. There\'s also a Logout button that returns to the login screen '
        'and clears the current user from UserService.',
    'InventoryScreen.java':
        'The most feature-rich screen in the system. Shows all medicines in a TableView. '
        'On the left side there\'s a form for adding and editing medicines, with a ComboBox '
        'for selecting the medicine category (populated from the MedicineCategory enum). '
        'There\'s a search box, a sort dropdown, and a category filter at the top of the '
        'table. Clicking a row auto-fills the form fields for editing.',
    'BillingScreen.java':
        'The billing screen is split into two sections. On the left you build the bill: '
        'enter a customer ID (auto-fills the name), add medicines by ID and quantity, '
        'optionally apply a discount percentage, then hit Generate Bill. The processing '
        'runs in a BillingThread so the UI stays responsive. On the right, current bill '
        'items are shown in one table and past bills in another.',
    'SupplierScreen.java':
        'Standard CRUD screen for supplier records. Table on the right shows all suppliers, '
        'clicking a row populates the form on the left for editing. Add, Update, Delete, '
        'and Clear buttons. Search by company name filters the table in real time. '
        'Supplier IDs are auto-generated by IDGenerator.',
    'CustomerScreen.java':
        'Same layout pattern as SupplierScreen but for customer/patient records. The '
        'search function does a case-insensitive name search through CustomerService. '
        'Customer IDs follow the CUS-xxxx format from IDGenerator. '
        'Selected table rows populate the form automatically.',
    'PrescriptionScreen.java':
        'Slightly more complex than the other CRUD screens because a prescription has nested '
        'items. You fill in the patient and doctor details, then add medicines one by one '
        'into a ListView showing the current list. Once you save, the full prescription '
        '(with all items) goes into PrescriptionService. Selecting a saved prescription '
        'shows its complete details in a TextArea below the main table.',
    'ReportsScreen.java':
        'The reports screen has a menu on the left side with buttons for different report '
        'types. The default view is a summary dashboard showing coloured cards with counts '
        'for medicines, customers, bills, and total sales. Other views show the full sales '
        'report, stock levels, expiry alerts (pulled from the running ExpiryAlertThread), '
        'and low stock items. The backup button runs BackupService in a new thread and '
        'shows a progress indicator while it runs.',
    'DataStore.java':
        'This is the generic persistence class that all five service classes use. It\'s '
        'declared as DataStore<T extends Serializable>, so it works with any model class '
        'that implements Serializable. saveAll() takes an ArrayList and writes it to a '
        '.dat file using ObjectOutputStream wrapped around FileOutputStream. loadAll() '
        'reads it back with ObjectInputStream and FileInputStream. backupToText() writes '
        'a readable version using FileWriter. All methods are synchronized to handle '
        'concurrent access from background threads.',
    'IDGenerator.java':
        'A small but important utility class. It keeps static integer counters for each '
        'type of record and generates IDs like MED1001, CUS2001, SUP3001 etc. Every '
        'generation method is synchronized so that even if two threads try to get an ID '
        'at the same time, they\'ll always get different values. There\'s also an '
        'updateCounters() method that gets called on startup to continue from where the '
        'last saved data left off.',
    'SampleDataLoader.java':
        'On the very first run, before any real data exists, this class populates the '
        'system with 10 sample medicines (covering all the enum categories), 3 sample '
        'customers, and 3 sample suppliers. It checks whether medicines already exist '
        'before loading anything so it never doubles up on runs after the first.',
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
    'By the end of this project we had a fully working pharmacy application that we could '
    'actually demonstrate with real data. Looking back, the part that took the most thought '
    'wasn\'t the UI or even the threading - it was getting the class structure right. '
    'Once the model and service layers were cleanly separated, everything else fell into '
    'place a lot more naturally. Adding a new feature meant touching one service class and '
    'one screen, not rewriting things all over the codebase.'
))
story.append(body(
    'The threading part was genuinely useful to implement. Running expiry and stock checks '
    'in the background means the user never has to manually refresh anything - the system '
    'just tells them when something needs attention. Using BillingThread for invoice '
    'processing also showed us why Platform.runLater() matters: without it, UI updates '
    'from a background thread would just silently fail or cause exceptions.'
))
story.append(body(
    'On the academic side, this project ended up covering every OOP concept from the syllabus '
    'and then some. Encapsulation is in every model class. Inheritance shows up in the '
    'Thread subclasses and the Application extension. Polymorphism comes through with '
    'overloaded methods in Bill.java and the callback interfaces used in the threading '
    'classes. Abstraction is in those same interfaces. Generics in DataStore<T>. '
    'Collections, Serialization, File I/O, Enums, Wrapper classes - they\'re all '
    'genuinely used, not just added as decorations. That made the code feel like a real '
    'project rather than just a lab exercise.'
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
    'We split the work based on what each person was comfortable with, but we all ended up '
    'reviewing and testing each other\'s code anyway. OOP projects are inherently '
    'interconnected - Kenneth\'s login screen needed Sam\'s Medicine class to exist, '
    'Rayyan\'s billing needed Vedank\'s DataStore to work. So even though we had clear '
    'ownership of different parts, we were constantly in each other\'s code fixing import '
    'paths, adjusting method signatures, and debugging integration issues together. '
    'That back-and-forth is actually what made the final result consistent.'
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
