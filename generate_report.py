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
    'Running a pharmacy involves far more record-keeping than most people realise. Every tablet '
    'sold, every prescription received, every new batch delivered from a supplier - all of it '
    'needs to be logged somewhere. When that somewhere is a paper notebook, things go wrong '
    'quickly. A medicine gets billed at the wrong price. Someone sells a batch that expired '
    'two weeks ago. A customer\'s prescription history disappears when the register gets full '
    'and a new one is started. These are not theoretical scenarios - they happen regularly in '
    'pharmacies that have not moved away from manual record keeping.'
))
story.append(body(
    'Our group chose to build a desktop application for pharmacy management as our semester '
    'project. The application runs on Java with a visual front end built using JavaFX. '
    'A staff member can look up any medicine in seconds, raise an invoice with automatic '
    'calculations, store patient prescriptions digitally, and see a live warning the moment '
    'any medicine drops below the minimum stock level or approaches its expiry date. '
    'Two separate background processes keep watch over stock and expiry round the clock, '
    'completely independent of whatever the staff member is doing on screen at the time.'
))
story.append(body(
    'The project gave us a concrete reason to use OOP properly rather than just reading '
    'about it. Every concept from the syllabus ended up appearing naturally - private fields '
    'with controlled access, classes that share behaviour through parent classes, the same '
    'method name behaving differently depending on the arguments passed, shared behaviour '
    'defined through interfaces, type-independent data storage through generics, and '
    'background workers through threads. Nothing felt forced. The structure of a real '
    'pharmacy application just happens to need all of these things.'
))

# ── PROBLEM STATEMENT ──────────────────────────────────────────────────────
story += [sp(4)]
story.append(sec_hdr('Problem Statement'))
story += [sp(6)]
story.append(sub_hdr('Pharmacy Management System with Inventory Control and Billing Automation'))
story.append(body(
    'A typical neighbourhood pharmacy juggles stock from dozens of suppliers, serves hundreds '
    'of patients, and processes prescriptions from multiple doctors - all in a single working '
    'day. Without a proper system, the staff end up spending more time searching for information '
    'than actually serving customers. A patient asks whether a particular antibiotic is '
    'available and the pharmacist has to flip through pages of a register to find out. '
    'An invoice gets calculated by hand and the arithmetic is off. A box of injections sits '
    'on the shelf a month past its expiry date because nobody checked.'
))
story.append(body(
    'The problem is not a lack of effort - it\'s a lack of the right tools. Our project '
    'addresses this directly. We designed the system around four core needs: knowing exactly '
    'what is in stock at all times, generating accurate bills without manual calculations, '
    'maintaining a searchable record of every patient and prescription, and receiving automatic '
    'alerts when something needs attention. Two background threads run continuously - one '
    'watching for medicines whose stock has dropped too low, and another checking expiry '
    'dates on a schedule - so the staff are warned before a problem becomes a crisis, '
    'not after.'
))

# ── IMPLEMENTATION DETAILS ─────────────────────────────────────────────────
story.append(sec_hdr('Implementation Details'))
story += [sp(6)]
story.append(body(
    'The project is written entirely in Java. For the visual side we chose JavaFX, which '
    'gave us proper desktop-grade UI components - tables, forms, dropdowns, and layout '
    'containers - without needing a web stack. The source code is spread across 32 files '
    'grouped under four packages. The model package is purely data - each class there '
    'describes one kind of record the system deals with. The service package contains all '
    'the processing logic, completely separated from any visual code. The ui package has '
    'one file per screen. The util package holds anything shared across the rest of the '
    'code, like the file storage engine and the ID numbering system.'
))
story.append(body(
    'Keeping the service and UI layers separate was a deliberate choice we made after '
    'an early draft where a screen class was also doing database operations - it became '
    'unreadable fast. Once we separated them, each class had one clear job. The service '
    'classes don\'t know anything about buttons or text fields. The screens don\'t know '
    'anything about files or serialization. And because multiple threads run in the '
    'background accessing the same data, every method in the service layer that writes '
    'anything carries a lock to prevent two threads from colliding.'
))
story.append(body('All 32 source files included in this project:'))

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
        'This class describes a single medicine entry - everything worth knowing about one '
        'product sitting on the pharmacy shelf. The quantity field is typed as Integer rather '
        'than the primitive int, and price uses Double rather than double. This was intentional '
        'to show how Java automatically wraps and unwraps primitive values when assigning '
        'between the two forms. The class has two versions of the constructor: one that '
        'includes a supplier reference and one that leaves it out, demonstrating how '
        'constructors can be overloaded. A compareTo method was added so that when a list '
        'of medicines gets sorted, the natural ordering is alphabetical by name.',
    'MedicineCategory.java':
        'Rather than letting someone type "tablet" in one place and "Tablet" in another and '
        'have the system treat them as different things, we locked the allowed categories '
        'into an enum. The eight values cover the full range of what a typical pharmacy '
        'stocks: tablets, capsules, syrups, injections, ointments, drops, inhalers, and '
        'powders. Every category carries a display name alongside it so the UI can show '
        'something readable without any extra conversion step.',
    'UserRole.java':
        'Two roles exist in the system - one for administrators who need access to '
        'everything, and one for pharmacists whose access is more restricted. We put both '
        'in an enum rather than comparing strings at login time. Each role carries a boolean '
        'flag that answers whether that role is permitted to manage other user accounts. '
        'Checking permission anywhere in the app is then just a matter of calling that flag.',
    'Customer.java':
        'Five pieces of information describe a customer in this system: an ID we generate, '
        'their full name, phone number, email address, and physical address. The class is '
        'tagged so Java\'s built-in object serialisation can write it to disk and read it '
        'back on the next launch. The toString method produces a short summary string '
        'that shows up in dropdowns and log outputs.',
    'Supplier.java':
        'A supplier record tracks the company that delivers medicines to the pharmacy. '
        'Beyond the company name we also store a specific contact person\'s name, their '
        'phone and email, and the company address. Each medicine in the inventory can '
        'carry a supplier ID pointing back to whichever supplier provided that batch. '
        'Like all the model classes, this one is serialisable so it persists across sessions.',
    'Bill.java':
        'A bill is more than just a total - it records who bought what, when, and who '
        'at the pharmacy processed the sale. The list of individual items is stored inside '
        'the bill object itself. The discount logic was written as two separate methods '
        'sharing the same name: one accepts a percentage, the other accepts an amount and '
        'a flag that says whether to treat it as fixed or percentage. This is the clearest '
        'example of method overloading in the project.',
    'BillItem.java':
        'One row on a receipt maps to one BillItem object. It knows the medicine name, '
        'how many units were sold, the price per unit, and the line total. The numeric '
        'fields are all object types rather than primitives - Integer for the count and '
        'Double for the money values - so that autoboxing and unboxing are visibly '
        'happening when we assign plain numbers to them in the constructor.',
    'Prescription.java':
        'A doctor writes a prescription for a specific patient. This class captures that '
        'relationship: it stores which patient the prescription belongs to, the name of '
        'the prescribing doctor, the date, any special notes, and a collection of the '
        'individual medicines prescribed. The medicine list grows one entry at a time '
        'as items are added through the addItem method.',
    'PrescriptionItem.java':
        'Each medicine that appears in a prescription is stored as its own object. '
        'Beyond the medicine name and quantity, it also stores the dosage string - '
        'something like "1 tablet morning and night" - which is specific to that '
        'prescription and cannot come from the general inventory record.',
    'User.java':
        'Staff members who can log into the system are stored as User objects. The '
        'class holds a login name, a password, the person\'s full name, and their role. '
        'Password checking is handled by a method inside this class rather than in the '
        'login screen, so the credential comparison logic stays in one place. '
        'User objects are serialisable so accounts survive application restarts.',
    'InventoryManager.java':
        'This service class is the backbone of the stock management side. It keeps the '
        'medicine data in two parallel structures at once: an ordered list for things like '
        'displaying all medicines in sequence, and a lookup table keyed by medicine ID '
        'for instant retrieval when you know what you\'re looking for. Because two background '
        'threads are also reading this data at runtime, every write operation is locked so '
        'only one thread can change anything at a time. Removing medicines while iterating '
        'is done through a traversal object that handles removal safely rather than '
        'modifying the list mid-loop. Sorting supports three modes: alphabetical by name '
        'using the natural ordering defined in Medicine.java, by price, and by expiry date.',
    'BillingService.java':
        'This class sits between the billing screen and the data layer. When a bill comes '
        'in, it checks that sufficient stock exists for every item, deducts the quantities, '
        'saves the bill record, and writes a plain-text invoice file to disk. The invoice '
        'writing is done through a character stream writer pointed at a .txt file. '
        'Early in development this code used graphical border characters that only render '
        'correctly in UTF-8 but caused garbled output on Windows systems using a different '
        'default encoding, so those were replaced with plain dashes and pipes.',
    'CustomerService.java':
        'Adding, updating, searching, and removing customer records all live here. '
        'The data sits in two structures simultaneously - a list that preserves insertion '
        'order and a map that gives instant access by customer ID. Removal uses a traversal '
        'cursor rather than index-based deletion, which avoids a structural modification '
        'error that Java throws if you delete from a collection while directly looping it. '
        'All changes are pushed to disk immediately through the generic storage class.',
    'SupplierService.java':
        'Structured identically to the customer service but operating on supplier records '
        'instead. The same dual-storage pattern applies: list plus map. The search feature '
        'here matches against company name rather than a person\'s name, using a '
        'case-folded substring comparison so partial matches work regardless of how '
        'the user types the name.',
    'PrescriptionService.java':
        'Prescription records are added, retrieved, and deleted through this class. '
        'The lookup-by-patient method is particularly useful in the UI - when a staff '
        'member pulls up a customer\'s profile, all their past prescriptions can be '
        'fetched with a single call. Storage and retrieval from disk is entirely '
        'delegated to the generic DataStore class.',
    'UserService.java':
        'The first time the application launches with no saved user data, this class '
        'quietly creates two default accounts so there is always something to log in with. '
        'When a login attempt comes in, it walks the user list looking for a name match '
        'and then asks the User object itself to verify the password - so the password '
        'comparison logic is not spread across multiple files.',
    'ExpiryAlertThread.java':
        'This is one of two background workers in the system and it uses direct class '
        'extension rather than the interface approach. It is flagged as a daemon so the '
        'JVM does not wait for it to finish before shutting down. After pausing for thirty '
        'seconds it wakes up and asks the inventory manager for two lists: medicines '
        'already past their date, and medicines within thirty days of expiring. '
        'A wait/notify pair lets other threads block on this one and receive the results '
        'safely once they are ready.',
    'StockAlertThread.java':
        'The second background worker, written using the interface-based threading '
        'approach rather than subclassing. A volatile flag controls whether the loop '
        'keeps running - marking it volatile ensures the main thread\'s update to that '
        'flag is visible to this thread immediately without caching issues. '
        'The stock check itself is wrapped in a lock so that if both this thread and '
        'the inventory screen try to read inventory data at the same moment, they queue '
        'rather than collide.',
    'BillingThread.java':
        'Processing a bill - checking stock, writing the invoice file, saving the record - '
        'takes a noticeable amount of time if done on the same thread as the UI. '
        'Doing so would freeze the interface while the user waits. This class moves that '
        'work onto a separate thread. When finished, it needs to update labels on screen, '
        'but UI elements can only be touched from the main thread, so the result is handed '
        'back through a scheduled task that runs on the correct thread. A join call in a '
        'separate watcher thread demonstrates how one thread can pause until another '
        'has fully completed.',
    'BackupService.java':
        'Written as a task rather than a thread subclass, this class can be handed to '
        'any thread the caller creates. When it runs, it goes through each of the five '
        'service classes one by one and asks each to write a plain-text copy of its data '
        'to the backup folder, with brief pauses between each one. A callback interface '
        'lets the caller know when everything is done so the UI can show a confirmation.',
    'PharmacyApp.java':
        'The application\'s starting point. It extends the JavaFX base class and overrides '
        'the startup method where all initialisation happens: service objects are created, '
        'the two monitoring workers are started, demo data is loaded if the data folder '
        'is empty, and the login window appears. Screen navigation works by calling one '
        'of several named methods, each of which builds the target screen and hands it '
        'to the window to display.',
    'LoginScreen.java':
        'A grid-based form with username and password fields, the second of which masks '
        'its input. On submission, the credentials go to the user service for checking. '
        'A wrong entry makes a red message appear below the form. A correct entry '
        'stores the authenticated user and hands control to the dashboard screen. '
        'The role attached to the user object at this point determines what '
        'options will appear throughout the rest of the session.',
    'DashboardScreen.java':
        'The home screen after login is deliberately simple - a dark header bar showing '
        'who is logged in, and six large buttons arranged in a grid, one for each module. '
        'A logout button in the header clears the session and returns to the login screen. '
        'The whole layout uses a border container at the outer level with a horizontal '
        'bar at the top and a grid in the centre.',
    'InventoryScreen.java':
        'This screen has the most going on visually. A scrollable table fills most of '
        'the space, showing every medicine in stock. A form on the left handles adding '
        'new entries and editing existing ones - clicking any table row copies that '
        'row\'s data into the form automatically. Above the table, a text search box, '
        'a sort selector, and a category filter all operate on the displayed list '
        'independently of each other.',
    'BillingScreen.java':
        'The left panel of this screen is where a new bill gets built up piece by piece. '
        'Typing a customer ID causes the name to appear automatically. Each medicine is '
        'added by ID and quantity, and the running total updates after each addition. '
        'When the cashier clicks the generate button, the bill is handed off to a '
        'background worker so the interface stays usable during processing. '
        'The right panel shows the current bill items and a history of past bills.',
    'SupplierScreen.java':
        'A table of supplier records on the right, a form on the left, and four action '
        'buttons in between. Selecting a table row fills the form. Clicking Add creates '
        'a new record with a freshly generated ID. Update and Delete act on whatever '
        'is currently selected. A search field above the table filters by company name.',
    'CustomerScreen.java':
        'Laid out the same way as the supplier screen but dealing with patient records. '
        'The search runs against the patient name field. IDs are generated automatically '
        'in the CUS-prefixed format. The form clears itself and deselects the table row '
        'when the Clear button is pressed.',
    'PrescriptionScreen.java':
        'This screen is a step more involved than the others because one prescription '
        'contains multiple medicine entries. After filling in the patient and doctor '
        'details, the staff member adds medicines one at a time - each addition appears '
        'in a list on screen. Saving commits the whole prescription as a single record. '
        'Clicking an existing prescription in the table populates a text area below '
        'with the complete details including every prescribed medicine.',
    'ReportsScreen.java':
        'A navigation panel on the left switches between different views. The landing '
        'view shows summary cards - coloured boxes each displaying one key number like '
        'total medicines or total revenue. Other views show the full transaction history, '
        'the complete stock list, medicines nearing expiry, and medicines running low. '
        'The backup button starts the backup worker in a fresh thread and shows a '
        'spinning indicator until the callback fires with a completion message.',
    'DataStore.java':
        'Every service class needs to save its list to disk and load it back on startup. '
        'Rather than writing that file handling code five separate times, we wrote it '
        'once as a generic class that works with any saveable object type. The save '
        'operation wraps the list in a binary stream and writes it out as a .dat file. '
        'The load operation reverses that. A separate method writes the same data as '
        'readable text for the backup copies. All four methods carry locks to prevent '
        'a background thread from reading a file mid-write.',
    'IDGenerator.java':
        'Every record type needs a unique identifier that does not repeat across sessions. '
        'This class keeps a counter for each type - medicines, customers, suppliers, bills, '
        'and prescriptions - and increments it each time a new ID is needed. The increment '
        'step is locked so two threads asking for a new ID simultaneously always get '
        'different values. On startup, the counters are nudged up to at least the highest '
        'value already present in the saved data.',
    'SampleDataLoader.java':
        'The first time someone runs the application there is nothing in the database. '
        'Rather than staring at empty tables, this class fills in ten medicines spanning '
        'all eight categories, three customers, and three suppliers. It checks first '
        'whether medicines already exist - if they do, the whole method returns immediately '
        'so the demo data is never loaded twice.',
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
    'Getting the class structure right early on made an enormous difference to how the '
    'rest of the project went. The first version we sketched out had screen classes doing '
    'their own file operations, which quickly became hard to follow. Separating that out '
    'into proper service classes meant each file had one clear responsibility. After that '
    'split, adding the reports screen or the prescription module meant writing a new screen '
    'file and a new service file - nothing else needed to change.'
))
story.append(body(
    'The background thread work was something none of us had done in a full application '
    'before this project. Getting the expiry alerts to update the UI correctly took several '
    'tries - early attempts updated JavaFX components directly from the background thread, '
    'which caused intermittent crashes. The fix was to wrap those updates inside a call '
    'that schedules them back onto the main thread. Once we understood why that was needed, '
    'the rest of the threading work went much more smoothly.'
))
story.append(body(
    'Stepping back, this project touched every concept on the lab syllabus - but more '
    'importantly, each one appeared because the problem needed it, not because we were '
    'looking for a place to slot it in. Private fields with accessor methods kept data '
    'from being changed arbitrarily. The generic storage class eliminated four copies of '
    'identical file-handling code. The enum types caught category mismatches at compile '
    'time rather than runtime. Locks on the service methods protected data that two '
    'threads could otherwise corrupt simultaneously. The application ended up being a '
    'genuinely working piece of software, which made the whole exercise worth doing.'
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
    'The work was divided based on each person\'s strengths, but the nature of an OOP '
    'project means the parts are never truly independent. Kenneth\'s login flow needed '
    'the User and UserRole classes Sam had started. Rayyan\'s billing screen needed '
    'the DataStore and IDGenerator that Vedank was building. We spent a lot of time '
    'on a shared call resolving method signature mismatches and missing imports. '
    'That kind of back-and-forth might sound inefficient but it\'s actually what '
    'kept the four parts from drifting into four different styles - the final codebase '
    'reads like it was written by one person, which we consider the best outcome.'
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
