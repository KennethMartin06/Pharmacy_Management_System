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
    'When we started looking for a project idea, one of our team members mentioned his uncle '
    'owns a small pharmacy near his house. The pharmacy still runs on paper - a thick register '
    'for stock entries, handwritten bills, prescriptions tucked into folders. He said the '
    'staff spends at least an hour every day just searching through records. That gave us the '
    'idea. A pharmacy is actually a perfect use case for everything we were learning in our '
    'OOP lab - it has multiple types of data, multiple users with different access levels, '
    'operations that need to happen in the background, and files that need to be saved and '
    'loaded between sessions.'
))
story.append(body(
    'So we built a desktop application for pharmacy management using Java and JavaFX. '
    'The system handles six main areas: medicine inventory, billing and invoices, customer '
    'records, supplier information, prescriptions, and a reports section. Staff can search '
    'for any medicine instantly, build a bill by adding items one by one with automatic '
    'price calculation, and save prescription records linked to specific patients. '
    'Two monitoring threads run in the background the entire time the application is open - '
    'one checks for medicines running low on stock, the other watches expiry dates - '
    'so the staff get warnings without having to check anything manually.'
))
story.append(body(
    'From a learning perspective, this project made OOP concepts feel real rather than '
    'textbook exercises. We needed encapsulation to protect medicine and billing data '
    'from being changed accidentally. We needed inheritance when building threads and the '
    'main application class. We needed method overloading in the billing logic where '
    'discount can be applied as either a percentage or a flat amount. Interfaces gave us '
    'a clean way to pass results back from background threads to the UI. Generics let us '
    'write a single file-storage class that works for medicines, customers, suppliers, '
    'bills, and prescriptions without duplicating any code. Every concept earned its place.'
))

# ── PROBLEM STATEMENT ──────────────────────────────────────────────────────
story += [sp(4)]
story.append(sec_hdr('Problem Statement'))
story += [sp(6)]
story.append(sub_hdr('Pharmacy Management System with Inventory Control and Billing Automation'))
story.append(body(
    'The core problem with paper-based pharmacy management is not just that it is slow. '
    'It is that mistakes are invisible until they cause damage. A billing error in a '
    'handwritten invoice is discovered only when the patient questions it. An expired '
    'medicine batch is noticed only when someone picks it up to dispense it. A stock '
    'shortage is caught only when the shelf is empty and a customer is waiting. '
    'None of these are acceptable situations in a healthcare setting, yet they are '
    'a daily reality for pharmacies that have not upgraded their systems.'
))
story.append(body(
    'Our system targets these three failure points directly. Every invoice is calculated '
    'by the software, so arithmetic errors are not possible. Expiry dates are monitored '
    'continuously by a background thread that flags anything expiring within thirty days, '
    'giving staff time to act before the medicine becomes unusable. Stock levels trigger '
    'a separate alert the moment any item drops below ten units. Beyond these alerts, '
    'the system also stores prescription history per patient, tracks which supplier '
    'provided which batch, and generates text-format invoice files that can be printed '
    'or archived. The whole application is designed to run on a standard pharmacy counter '
    'PC with no internet connection required.'
))

# ── IMPLEMENTATION DETAILS ─────────────────────────────────────────────────
story.append(sec_hdr('Implementation Details'))
story += [sp(6)]
story.append(body(
    'The entire codebase is in Java, with JavaFX handling the visual interface. '
    'We picked JavaFX because it gives proper desktop UI components out of the box - '
    'tables that sort when you click a column header, form layouts that align fields '
    'neatly, styled buttons, dropdown selectors - all without needing a browser or '
    'a web framework. The 32 source files are split into four packages based on what '
    'they do rather than how they look. Model classes are just data containers. '
    'Service classes hold all the logic and have no knowledge of the interface. '
    'UI classes build and display screens. Utility classes provide shared tools '
    'like ID generation and file storage that every other package depends on.'
))
story.append(body(
    'We initially wrote the inventory screen so that it handled its own data loading '
    'and saving. It quickly became a 600-line class that was difficult to follow. '
    'Splitting the data operations out into a separate service class cut the screen '
    'file in half and made both halves individually readable. That experience shaped '
    'how we structured the rest of the project. Every screen does only three things: '
    'build the layout, react to user input, and call the right service method. '
    'The service layer does the actual work. Since background threads are also '
    'reading and writing the same data that the service classes manage, '
    'every write operation inside those classes is locked - only one thread '
    'can execute it at a time, which prevents data from getting corrupted '
    'when two operations overlap.'
))
story.append(body('All 32 source files in this project:'))

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
        'Medicine.java is the data class for a single stock item. Each medicine object '
        'stores its ID, name, manufacturer, category, batch number, expiry date, quantity, '
        'price, and supplier ID. We deliberately declared quantity as Integer (capital I) '
        'and price as Double (capital D) rather than using the primitive forms int and double. '
        'The reason was to have autoboxing and unboxing visible in the code - whenever we '
        'assign a plain number to those fields, Java silently wraps it into an object, and '
        'when we use it in a calculation, it unwraps it back. The class has two constructors: '
        'one that takes all nine fields including the supplier ID, and another shorter one '
        'that leaves the supplier ID out for cases where it is not known yet. That is '
        'constructor overloading. There is also a compareTo method which makes it possible '
        'to sort a list of medicines alphabetically by name without writing any extra '
        'comparison logic at the call site.',
    'MedicineCategory.java':
        'This is an enum with eight values: TABLET, CAPSULE, SYRUP, INJECTION, OINTMENT, '
        'DROPS, INHALER, and POWDER. Before we introduced this, category was stored as a '
        'plain String, which caused problems - one part of the code would write "Tablet" '
        'and another would write "tablet" and they would not match. An enum fixes that '
        'completely because there is only one possible value and Java enforces it at '
        'compile time. Each enum value also carries a human-readable display name so '
        'the UI can show "Tablet" instead of "TABLET" without any extra formatting code.',
    'UserRole.java':
        'The system supports two account types: ADMIN for full access and PHARMACIST '
        'for a restricted view. Both are defined in this enum. Each value carries a '
        'boolean field that says whether that role is allowed to manage user accounts. '
        'Using an enum here instead of a String or integer constant means the compiler '
        'will catch any typo in a role check at build time rather than at runtime.',
    'Customer.java':
        'Stores five details for each patient: a system-generated ID, their name, '
        'phone number, email, and address. The class is marked as serialisable, which '
        'is the flag Java needs to be able to write the object to a file and read it '
        'back correctly on the next startup. A toString method returns a compact one-line '
        'summary that is used in tables and status messages.',
    'Supplier.java':
        'A supplier entry covers the company name, a specific contact person at that '
        'company, their phone and email, and the company address. Medicines in the '
        'inventory link back to a supplier through a supplier ID stored in the medicine '
        'record itself, so you can trace any batch back to where it came from. '
        'Serialisable like all the other model classes.',
    'Bill.java':
        'A complete billing record contains the customer details, the transaction date, '
        'the username of whoever processed the bill, and a list of all the line items. '
        'The discount feature is written using method overloading - there are two methods '
        'both named applyDiscount, but they take different parameters. One takes just a '
        'percentage value. The other takes an amount and a boolean flag: if the flag is '
        'true, the amount is treated as a fixed rupee deduction; if false, it is treated '
        'as a percentage. This is one of the clearer demonstrations of polymorphism in '
        'the project.',
    'BillItem.java':
        'One line in a bill - one medicine, its quantity, unit price, and calculated '
        'subtotal. The quantity is stored as Integer and the prices as Double, both '
        'capital-letter object types rather than lowercase primitives. The constructor '
        'takes plain int and double values as parameters and assigns them to these fields, '
        'which is where autoboxing happens: Java wraps the primitive into the object form '
        'automatically without us having to call any conversion method.',
    'Prescription.java':
        'A prescription belongs to a specific patient and was written by a specific doctor '
        'on a specific date. This class holds all of that, plus any notes (dosage '
        'instructions, special warnings), and a list of PrescriptionItem objects - one '
        'for each medicine the doctor prescribed. The addItem method grows that list one '
        'entry at a time as items are added in the prescription screen.',
    'PrescriptionItem.java':
        'Each medicine in a prescription is its own PrescriptionItem. It records the '
        'medicine name, how many units were prescribed, and a dosage instruction string '
        'like "twice daily after meals". The dosage text is entered by the staff member '
        'at the time of creating the prescription - it is not pulled from the inventory '
        'because dosage instructions vary by patient even for the same medicine.',
    'User.java':
        'Login accounts for pharmacy staff. Each User object stores a username, a '
        'password, the person\'s full name, and their role as a UserRole enum value. '
        'The authenticate method inside the class accepts a password string and returns '
        'true or false depending on whether it matches. We put that check inside the '
        'model class deliberately so the login screen does not need to know anything '
        'about how passwords are compared - it just calls the method and acts on the result.',
    'InventoryManager.java':
        'This is the most heavily used service class in the whole project. '
        'It holds all medicines in two data structures at once. There is a list, which '
        'keeps medicines in the order they were added and can be iterated for display. '
        'There is also a map keyed by medicine ID, which gives you any specific medicine '
        'in constant time without scanning through the whole list. Both are kept in sync '
        'on every add, update, and delete. Deletion is done using Java\'s iterator cursor '
        'rather than removing inside a regular loop, because removing from a list while '
        'iterating it normally throws an error. Since the expiry alert thread and the stock '
        'alert thread both read inventory data while the user might be adding or editing, '
        'every write method is locked - only one caller can run it at a time. Sorting '
        'is available in three ways: by name using the compareTo method in Medicine.java, '
        'by price using a custom comparator, and by expiry date using another comparator.',
    'BillingService.java':
        'All billing operations go through here. When a bill is submitted, this class '
        'checks each item against current stock levels, rejects the whole transaction if '
        'anything is short, otherwise deducts all quantities and saves the bill. It also '
        'writes a plain-text invoice to a .txt file using a character-based file writer. '
        'We hit a problem during testing where the invoice used line-drawing characters '
        'that displayed correctly on our machines but came out as garbled symbols on '
        'Windows computers set to a different text encoding. We fixed it by switching '
        'to plain dashes and vertical bars instead, which encode the same in everything.',
    'CustomerService.java':
        'Manages patient records: add, update, delete, search, and fetch by ID. '
        'The storage structure is a list and a map in parallel, same as InventoryManager. '
        'The list is used when displaying all customers in a table. The map is used when '
        'the billing screen or prescription screen needs a specific customer by their ID '
        'without scanning the whole list. The search method does a case-insensitive '
        'name match, returning every customer whose name contains the search text anywhere '
        'within it. Every change is written to disk immediately after it happens.',
    'SupplierService.java':
        'Handles supplier records with the same structure as CustomerService. List plus '
        'map, iterator-based deletion, immediate persistence after each change. '
        'The only difference is that search runs against the company name field rather '
        'than a person\'s name. This class is also called by the backup service, which '
        'asks it to write a readable text copy of all supplier data to a separate file.',
    'PrescriptionService.java':
        'Prescriptions can be added, deleted, and retrieved here. One method worth '
        'mentioning is getByCustomerId, which returns all prescriptions belonging to a '
        'specific patient. The prescription screen uses this when a staff member selects '
        'a patient to see their prescription history. The persistence mechanism is '
        'identical to the other service classes - a DataStore instance handles reading '
        'and writing the serialised file.',
    'UserService.java':
        'This class handles login and user account management. On first run, when the '
        'data folder has no user file yet, it creates two default accounts: one admin '
        'and one pharmacist. The login process searches the user list for a matching '
        'username, then calls the authenticate method on the User object to check the '
        'password. We made that check a method on User rather than in this service class '
        'so the password comparison logic is in exactly one place and is not duplicated '
        'if we add a password-change feature later.',
    'ExpiryAlertThread.java':
        'The expiry monitor runs as a background thread by directly extending the Thread '
        'class. It is configured as a daemon thread, which means the JVM will shut it '
        'down automatically when the application closes without needing any manual stop '
        'call. The run loop sleeps for thirty seconds, then wakes up and asks the '
        'inventory manager for two lists: medicines already past their expiry date and '
        'medicines expiring within the next thirty days. A wait/notify mechanism is used '
        'so that any external code that wants to read those lists can safely wait until '
        'the thread has finished its current check before accessing the results.',
    'StockAlertThread.java':
        'The stock monitor uses the Runnable interface rather than extending Thread '
        'directly. This was deliberate - we wanted to show both approaches in the same '
        'project since the syllabus covers both. The thread runs a loop that pauses for '
        'thirty seconds at a time, then calls the inventory manager for a list of any '
        'medicines below ten units. A volatile boolean controls whether the loop '
        'continues. It is volatile specifically so that when the main thread sets it '
        'to false to stop the worker, the worker thread sees the change immediately '
        'rather than reading a cached copy of the old value.',
    'BillingThread.java':
        'When the cashier clicks "Generate Bill", the actual processing - stock checks, '
        'quantity deduction, file writing, record saving - runs here rather than on the '
        'main application thread. Running it on the main thread would freeze the entire '
        'interface for a second or two. This thread does the work, then needs to update '
        'status labels in the UI when done. UI updates must happen on the JavaFX main '
        'thread, so the result is passed to a scheduling method that queues the update '
        'to run on the correct thread as soon as it is available. Separately, a small '
        'watcher thread calls join on this billing thread, which demonstrates how one '
        'thread can pause and wait for another to complete before continuing.',
    'BackupService.java':
        'This class implements the Runnable interface and is designed to be passed to '
        'whichever Thread the caller creates for it. When it executes, it calls the '
        'backup method on each of the five service classes in order - inventory, '
        'customers, suppliers, bills, prescriptions - with a short pause between each. '
        'Each service class writes its data out as a human-readable text file in the '
        'data folder. A callback interface carries the completion message back to the '
        'UI, which shows it to the user once the backup finishes.',
    'PharmacyApp.java':
        'This is the main class where execution begins. It extends Application, which '
        'is the base class JavaFX requires as the entry point. The start method, which '
        'JavaFX calls automatically, creates all the service objects, starts the two '
        'background alert threads, loads sample data if the data folder is empty, '
        'and shows the login screen. Navigation between screens is handled through '
        'dedicated show methods - showInventoryScreen, showBillingScreen, and so on - '
        'each of which creates the target screen object and calls setScene on the '
        'application window to replace what is currently visible.',
    'LoginScreen.java':
        'The login form is built using a grid layout that keeps the labels and fields '
        'neatly aligned. The password field uses JavaFX\'s PasswordField component, '
        'which shows dots instead of the actual characters. When the user clicks Login, '
        'the username and password are passed to UserService. If authentication fails, '
        'a red label appears below the button explaining why. If it succeeds, the '
        'authenticated user object is stored in the service and the dashboard screen '
        'is loaded. The role stored in that user object shapes what options are '
        'available for the rest of the session.',
    'DashboardScreen.java':
        'After logging in successfully, the dashboard is the first thing the user sees. '
        'The layout has a dark-coloured header bar across the top containing the '
        'application name and the logged-in user\'s name and role. Below that, six '
        'equal-sized buttons are arranged in two rows of three, each one opening a '
        'different module. A Logout button in the header ends the session by clearing '
        'the current user in UserService and returning to the login screen.',
    'InventoryScreen.java':
        'The inventory screen is the most visually complex in the system. A large table '
        'in the centre shows all medicines currently in stock, with columns for ID, name, '
        'category, batch, expiry date, quantity, and price. Clicking a row fills the form '
        'on the left side with that medicine\'s details so staff can edit and save. '
        'Above the table there are three controls: a search box that filters by medicine '
        'name as you type, a dropdown to sort the table by name, price, or expiry date, '
        'and a category dropdown that shows only medicines matching the selected category.',
    'BillingScreen.java':
        'The billing screen is divided into two sides. The left side is where a new bill '
        'is assembled: the staff member enters a customer ID (the name fills automatically '
        'from the customer database), then adds medicines one by one by entering the '
        'medicine ID and desired quantity. The running total updates after each item is '
        'added. An optional discount percentage can be applied before the final generate '
        'button is clicked. Once clicked, the bill goes to a BillingThread so the '
        'interface is not blocked during processing. The right side shows a table of '
        'current bill items and below it a table of all past bills.',
    'SupplierScreen.java':
        'Supplier records are managed from this screen. The layout mirrors the customer '
        'screen: table on the right showing all suppliers, form on the left for data '
        'entry, and a row of four buttons for Add, Update, Delete, and Clear. Clicking '
        'a row in the table copies all its fields into the form so the staff member can '
        'make changes without retyping everything. A search box above the table narrows '
        'results by company name.',
    'CustomerScreen.java':
        'Patient records live in this screen. Same table-and-form layout as the supplier '
        'screen. The search matches against the patient name. When a new customer is '
        'added, the ID is generated automatically using IDGenerator - the staff member '
        'does not type it. Pressing Clear empties the form and removes any table row '
        'selection so the form is ready for a new entry.',
    'PrescriptionScreen.java':
        'Prescriptions are more complex than other records because they contain nested '
        'items. The form on the left starts with the patient details and doctor name. '
        'Below that is a mini-form to add one medicine at a time: enter the medicine ID, '
        'quantity, and dosage text, then click Add Medicine. Each addition appears in a '
        'small list on screen. Once all items are added, clicking Save builds the full '
        'prescription object with all its items and sends it to PrescriptionService. '
        'Clicking an existing prescription in the main table shows a full text summary '
        'in a text area at the bottom, listing every medicine in that prescription.',
    'ReportsScreen.java':
        'The reports section is more of a dashboard than a single report. A menu column '
        'on the left has buttons for Sales Report, Stock Report, Expiry Alerts, Low Stock '
        'Alerts, Summary, and Backup. The summary view - which is what opens by default - '
        'shows colour-coded cards displaying total medicines, total customers, total '
        'suppliers, total bills, and total revenue. The expiry and low stock views pull '
        'data from the live inventory rather than a cached snapshot. The backup button '
        'creates a BackupService instance, starts it in a fresh thread, and shows a '
        'spinning progress indicator in the content area until the backup callback fires.',
    'DataStore.java':
        'This is the generic file storage class used by all five service classes. '
        'It is declared as a generic class with a type parameter that must be serialisable, '
        'written as DataStore of T where T extends Serializable. This means the same class '
        'handles file operations for medicines, customers, suppliers, bills, and '
        'prescriptions without any duplication. The saveAll method takes a list and writes '
        'it to a binary .dat file using Java\'s object stream classes. The loadAll method '
        'reads it back and returns the list. A separate backupToText method writes the '
        'same data as a readable text file using a character-based writer. All methods '
        'are locked to prevent a background thread from reading a file while a save '
        'is still in progress.',
    'IDGenerator.java':
        'Generates unique IDs for every record type in the system. Five counters, one '
        'per record type, start at specific values - medicines at 1000, customers at 2000, '
        'suppliers at 3000, bills at 4000, prescriptions at 5000. Each counter increments '
        'every time a new ID of that type is requested, giving IDs like MED1001, CUS2001, '
        'BIL4001, and so on. Each method is locked so that if two threads request an ID '
        'at the same moment, they get different values. An updateCounters method is called '
        'at startup so the counters continue from where the saved data left off rather '
        'than resetting and producing duplicate IDs.',
    'SampleDataLoader.java':
        'On a fresh installation there is no data, which makes the application look broken. '
        'This class solves that by loading a set of demo records on first run: ten '
        'medicines covering all eight category types, three customers, and three suppliers. '
        'The first thing the method does is check whether medicines already exist. If they '
        'do, the method returns immediately without loading anything. This check ensures '
        'the demo data loads exactly once and never overwrites real data that was added later.',
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
    'The Pharmacy Management System came together as a working application that we could '
    'run, demo with real data, and actually use to process a bill end-to-end. That matters '
    'to us because a lot of lab projects stop at "it compiles and the output is correct." '
    'This one has a real interface, saves data between sessions, and runs background '
    'monitoring without the user doing anything. The design decisions we made early on - '
    'separating service logic from screen code, using a generic class for file storage, '
    'building the threading around proper daemon threads and volatile flags - all of those '
    'paid off when it came to adding the later modules. Adding the prescription screen '
    'or the reports section did not require changes to any existing class.'
))
story.append(body(
    'Threading was the part that took the most time to get right. Our first version of '
    'the billing screen updated a status label directly from inside the BillingThread. '
    'The application crashed sometimes and worked other times - which is exactly the '
    'kind of intermittent bug that is hard to track down. After reading about JavaFX\'s '
    'threading rules, we understood that UI components can only be modified from the '
    'main application thread. The fix - wrapping the label update inside a call that '
    'schedules it to run on the correct thread - was a one-line change that made the '
    'crashes disappear entirely. It was a frustrating bug to hit but a genuinely useful '
    'thing to understand.'
))
story.append(body(
    'Looking at the complete file list, every OOP concept from the course syllabus '
    'is present and used for a real reason. Encapsulation in the model classes keeps '
    'fields from being set to invalid values from outside. Inheritance appears in the '
    'Thread subclasses and in extending Application. Polymorphism shows up in the '
    'overloaded discount methods and in the callback interfaces shared between threads '
    'and UI classes. Generics in DataStore removed four copies of identical persistence '
    'code. Enums in MedicineCategory and UserRole removed whole categories of runtime '
    'bugs. The project ended up being a solid demonstration of why these concepts exist, '
    'not just what they are called.'
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
    'We split the work by module but spent a lot of time in each other\'s code anyway. '
    'When Kenneth was building the login screen he needed the User class and UserRole enum '
    'that Sam was still writing - so they sat together and finalised those first before '
    'the login screen could be completed. Rayyan could not test the billing screen until '
    'Vedank had the DataStore class working because nothing could be saved otherwise. '
    'That kind of dependency forced us to communicate constantly, which turned out to be '
    'good for the project. We caught mismatches in method signatures early, agreed on '
    'naming conventions together, and reviewed each other\'s code before merging. '
    'The result is a codebase that is consistent throughout - not four separate pieces '
    'written by four people independently, but one system built by a team.'
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
