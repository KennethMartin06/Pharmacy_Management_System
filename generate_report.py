from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                 TableStyle, HRFlowable, PageBreak)
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
T_CODE  = mks('cd',  fontName='Courier', fontSize=8, leading=11,
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

def hr():
    return HRFlowable(width='100%', thickness=0.5, color=colors.HexColor('#cccccc'), spaceAfter=6)

def simple_table(headers, rows, col_widths=None):
    data = [[Paragraph(h, T_CELLB) for h in headers]]
    for r in rows:
        data.append([Paragraph(str(c), T_CELL) for c in r])
    if not col_widths:
        col_widths = [COLW / len(headers)] * len(headers)
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),DARK),
        ('BACKGROUND',(0,1),(-1,-1),colors.HexColor('#ecf0f1')),
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

OUT = '/home/user/Pharmacy_management_system/PharmacyManagementSystem_Report.pdf'
doc = SimpleDocTemplate(OUT, pagesize=A4,
                        leftMargin=2.5*cm, rightMargin=2.5*cm,
                        topMargin=2.2*cm, bottomMargin=1.8*cm)

story = []

# ── TITLE PAGE ─────────────────────────────────────────────────────────────
story += [sp(40)]
story.append(Paragraph('PHARMACY MANAGEMENT SYSTEM', T_TITLE))
story.append(Paragraph('Object-Oriented Programming – Mini Project Report', T_SUB))
story += [sp(8)]
story.append(Paragraph('Submitted in partial fulfillment of the requirements for the', T_SUB))
story.append(Paragraph('Bachelor of Technology in Computer Science and Engineering', T_SUB))
story += [sp(20)]

info_data = [
    [Paragraph('Project Title', T_CELLB), Paragraph('Pharmacy Management System', T_CELL)],
    [Paragraph('Subject', T_CELLB),       Paragraph('Object-Oriented Programming (OOP)', T_CELL)],
    [Paragraph('Academic Year', T_CELLB), Paragraph('2024 – 2025', T_CELL)],
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
    ['Name','Register Number','Roll No.'],
    [['Kenneth Martin','230905001','01'],
     ['Arun Prakash',  '230905002','02'],
     ['Divya Nair',    '230905003','03'],
     ['Sanjay Kumar',  '230905004','04']],
    [COLW*0.45, COLW*0.35, COLW*0.20]
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
    'This project was implemented in the Java programming language. The application utilizes '
    'object-oriented programming principles to manage pharmacy operations effectively.'
))
story.append(body('The system has the following files, containing the mentioned classes and methods:'))

files = ['PharmacyApp.java','LoginScreen.java','DashboardScreen.java','Medicine.java',
         'InventoryManager.java','BillingService.java','Customer.java / CustomerService.java',
         'DataStore.java']
for f in files:
    story.append(bul(f))

story += [sp(8)]
print("Part 1 ok")

# ── FILE EXPLANATIONS ──────────────────────────────────────────────────────

# 1. PharmacyApp.java
story.append(sec_hdr('Detailed Explanation of Each File'))
story += [sp(6)]
story.append(sub_hdr('1. PharmacyApp.java'))
story.append(body(
    'This file serves as the main entry point of the Pharmacy Management System. It extends '
    'the JavaFX Application class and overrides the start() method, which is the JavaFX '
    'lifecycle entry point. This class initializes all service objects, starts background '
    'monitoring threads for expiry and stock alerts, loads sample data on first run, and '
    'manages navigation between all screens using Stage.setScene(). It also handles graceful '
    'shutdown of background threads when the application is closed. This file contains JavaFX codes.'
))
story.append(body('Code for PharmacyApp.java file:'))
story.append(code(
'''package com.pharmacy.ui;

import com.pharmacy.service.*;
import com.pharmacy.model.User;
import javafx.application.Application;
import javafx.stage.Stage;
import java.io.File;

public class PharmacyApp extends Application {

    private UserService userService;
    private InventoryManager inventoryManager;
    private BillingService billingService;
    private ExpiryAlertThread expiryAlertThread;
    private Stage primaryStage;

    @Override
    public void start(Stage primaryStage) {
        this.primaryStage = primaryStage;
        new File("data/invoices").mkdirs();

        // Initialize all services
        userService       = new UserService();
        inventoryManager  = new InventoryManager();
        billingService    = new BillingService(inventoryManager);

        // Start background threads (Thread subclass + Runnable)
        expiryAlertThread = new ExpiryAlertThread(inventoryManager);
        expiryAlertThread.setDaemon(true);
        expiryAlertThread.start();

        StockAlertThread stockRunnable = new StockAlertThread(inventoryManager);
        Thread stockThread = new Thread(stockRunnable, "StockAlertThread");
        stockThread.setDaemon(true);
        stockThread.start();

        showLoginScreen();
        primaryStage.setTitle("PharmaCare - Pharmacy Management System");
        primaryStage.show();
    }

    public void showDashboard(User user) {
        DashboardScreen dashboard = new DashboardScreen(this, user);
        primaryStage.setScene(dashboard.getScene());
    }

    public static void main(String[] args) { launch(args); }
}'''))

# 2. LoginScreen.java
story.append(sub_hdr('2. LoginScreen.java'))
story.append(body(
    'This file handles the login interface of the Pharmacy Management System. The user must '
    'enter a valid username and password to access the system. The system supports two roles '
    '— Admin and Pharmacist — each with different access levels. If credentials are incorrect '
    'or empty, a red error message is displayed. After a successful login, the user is '
    'redirected to the Dashboard. The screen uses a GridPane for the form layout and '
    'PasswordField to securely mask the password input. This file contains JavaFX codes.'
))
story.append(body('Code for LoginScreen.java file:'))
story.append(code(
'''package com.pharmacy.ui;

import com.pharmacy.model.User;
import com.pharmacy.service.UserService;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;

public class LoginScreen {
    private Scene scene;

    public LoginScreen(PharmacyApp app, UserService userService) {
        VBox mainLayout = new VBox(20);
        mainLayout.setAlignment(Pos.CENTER);
        mainLayout.setStyle("-fx-background-color: #2c3e50;");

        Label titleLabel = new Label("PharmaCare");
        titleLabel.setFont(Font.font("Arial", FontWeight.BOLD, 36));
        titleLabel.setStyle("-fx-text-fill: #ecf0f1;");

        // GridPane for form layout
        GridPane grid = new GridPane();
        grid.setHgap(10);  grid.setVgap(15);
        grid.setPadding(new Insets(30));
        grid.setStyle("-fx-background-color: #34495e; -fx-background-radius: 10;");

        TextField usernameField = new TextField();
        PasswordField passwordField = new PasswordField();
        Label messageLabel = new Label();
        messageLabel.setStyle("-fx-text-fill: #e74c3c;");

        Button loginBtn = new Button("Login");
        loginBtn.setOnAction(e -> {
            String username = usernameField.getText().trim();
            String password = passwordField.getText().trim();
            if (username.isEmpty() || password.isEmpty()) {
                messageLabel.setText("Username and password cannot be empty.");
                return;
            }
            User user = userService.authenticate(username, password);
            if (user != null) {
                app.showDashboard(user);
            } else {
                messageLabel.setText("Invalid credentials! Please try again.");
            }
        });

        grid.add(new Label("Username:"), 0, 0); grid.add(usernameField, 1, 0);
        grid.add(new Label("Password:"), 0, 1); grid.add(passwordField, 1, 1);
        grid.add(loginBtn, 0, 2, 2, 1);
        grid.add(messageLabel, 0, 3, 2, 1);

        mainLayout.getChildren().addAll(titleLabel, grid);
        scene = new Scene(mainLayout, 1100, 700);
    }

    public Scene getScene() { return scene; }
}'''))

print("Part 2 ok")

# 3. DashboardScreen.java
story.append(sub_hdr('3. DashboardScreen.java'))
story.append(body(
    'This file handles the main dashboard screen displayed after a successful login. The user '
    'can navigate to any of the six modules: Inventory Management, Sales and Billing, Supplier '
    'Management, Customer Records, Prescription Handling, and Reports and Alerts. The dashboard '
    'displays the logged-in user\'s name and role in the top navigation bar. A logout button '
    'redirects back to the login screen. This file contains JavaFX codes.'
))
story.append(body('Code for DashboardScreen.java file:'))
story.append(code(
'''package com.pharmacy.ui;

import com.pharmacy.model.User;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;

public class DashboardScreen {
    private Scene scene;

    public DashboardScreen(PharmacyApp app, User currentUser) {
        BorderPane root = new BorderPane();

        // Top navigation bar (HBox)
        HBox topBar = new HBox(20);
        topBar.setStyle("-fx-background-color: #2c3e50;");
        Label title = new Label("PharmaCare Dashboard");
        title.setFont(Font.font("Arial", FontWeight.BOLD, 22));
        title.setStyle("-fx-text-fill: white;");
        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);
        Button logoutBtn = new Button("Logout");
        logoutBtn.setOnAction(e -> app.showLoginScreen());
        topBar.getChildren().addAll(title, spacer, logoutBtn);

        // Center - 3x2 GridPane of module buttons
        GridPane moduleGrid = new GridPane();
        moduleGrid.setAlignment(Pos.CENTER);
        moduleGrid.setHgap(25);
        moduleGrid.setVgap(25);

        Button inventoryBtn = createModuleButton("Inventory Management", "#3498db");
        Button billingBtn   = createModuleButton("Sales and Billing",    "#27ae60");
        Button supplierBtn  = createModuleButton("Supplier Management",  "#e67e22");
        Button customerBtn  = createModuleButton("Customer Records",     "#9b59b6");
        Button presBtn      = createModuleButton("Prescription Handling","#1abc9c");
        Button reportsBtn   = createModuleButton("Reports and Alerts",   "#e74c3c");

        inventoryBtn.setOnAction(e -> app.showInventoryScreen());
        billingBtn.setOnAction(e -> app.showBillingScreen());

        moduleGrid.add(inventoryBtn,0,0); moduleGrid.add(billingBtn,1,0);
        moduleGrid.add(supplierBtn,2,0);  moduleGrid.add(customerBtn,0,1);
        moduleGrid.add(presBtn,1,1);      moduleGrid.add(reportsBtn,2,1);

        root.setTop(topBar);
        root.setCenter(moduleGrid);
        scene = new Scene(root, 1100, 700);
    }

    private Button createModuleButton(String title, String color) {
        Button btn = new Button(title);
        btn.setPrefSize(230, 130);
        btn.setStyle("-fx-background-color:" + color + ";-fx-text-fill:white;" +
                     "-fx-font-size:15;-fx-background-radius:10;");
        return btn;
    }

    public Scene getScene() { return scene; }
}'''))

# 4. Medicine.java
story.append(sub_hdr('4. Medicine.java'))
story.append(body(
    'This file handles medicine information. The system uses this file to store all details '
    'of a medicine and pass it to other files as per the requirements. It implements the '
    'Serializable interface so that medicine objects can be saved to and loaded from .dat files '
    'using Java\'s object serialization. It also implements Comparable to allow sorting by name '
    'using Collections.sort(). This class demonstrates Encapsulation through private fields with '
    'public getter/setter methods, Wrapper classes (Integer, Double) with autoboxing/unboxing, '
    'and constructor overloading.'
))
story.append(body('Code for Medicine.java file:'))
story.append(code(
'''package com.pharmacy.model;

import java.io.Serializable;

public class Medicine implements Serializable, Comparable<Medicine> {
    private static final long serialVersionUID = 1L;

    private String medicineId;
    private String name;
    private MedicineCategory category;   // Enum
    private String expiryDate;
    private Integer quantity;   // Wrapper class (autoboxing)
    private Double  price;      // Wrapper class (autoboxing)
    private String  supplierId;

    // Parameterized constructor
    public Medicine(String medicineId, String name, MedicineCategory category,
                    String expiryDate, int quantity, double price, String supplierId) {
        this.medicineId = medicineId;
        this.name       = name;
        this.category   = category;
        this.expiryDate = expiryDate;
        this.quantity   = quantity;   // Autoboxing: int -> Integer
        this.price      = price;      // Autoboxing: double -> Double
        this.supplierId = supplierId;
    }

    // Constructor overloading (without supplierId)
    public Medicine(String medicineId, String name, MedicineCategory category,
                    String expiryDate, int quantity, double price) {
        this(medicineId, name, category, expiryDate, quantity, price, "");
    }

    // Comparable for Collections.sort()
    @Override
    public int compareTo(Medicine other) {
        return this.name.compareToIgnoreCase(other.name);
    }

    // Encapsulation - Getters and Setters
    public String  getMedicineId() { return medicineId; }
    public String  getName()       { return name; }
    public Integer getQuantity()   { return quantity; }
    public Double  getPrice()      { return price; }
    public int     getQuantityPrimitive() { return quantity; } // Unboxing

    public void setQuantity(Integer qty)  { this.quantity = qty; }
    public void setPrice(Double price)    { this.price = price;  }

    @Override
    public String toString() {
        return medicineId + " | " + name + " | Qty:" + quantity
               + " | Rs." + String.format("%.2f", price)
               + " | Exp:" + expiryDate;
    }
}'''))

print("Part 3 ok")

# 5. InventoryManager.java
story.append(sub_hdr('5. InventoryManager.java'))
story.append(body(
    'This file manages the medicine inventory. It uses an ArrayList for sequential storage '
    'and a HashMap to map medicine IDs to objects for fast O(1) lookup. The Iterator is used '
    'during deletion to avoid ConcurrentModificationException. Collections.sort() sorts '
    'medicines by name, price, or expiry date. All critical methods are synchronized for '
    'thread safety when multiple threads access the inventory simultaneously.'
))
story.append(body('Code for InventoryManager.java file:'))
story.append(code(
'''package com.pharmacy.service;

import com.pharmacy.model.Medicine;
import com.pharmacy.util.DataStore;
import java.util.*;

public class InventoryManager {

    private ArrayList<Medicine> medicineList;
    private HashMap<String, Medicine> medicineMap;
    private DataStore<Medicine> dataStore;
    private static final int LOW_STOCK_THRESHOLD = 10;

    public InventoryManager() {
        dataStore    = new DataStore<>("data/medicines.dat");
        medicineList = dataStore.loadAll();
        medicineMap  = new HashMap<>();
        for (Medicine med : medicineList)
            medicineMap.put(med.getMedicineId(), med);
    }

    public synchronized void addMedicine(Medicine medicine) {
        medicineList.add(medicine);
        medicineMap.put(medicine.getMedicineId(), medicine);
        dataStore.saveAll(medicineList);
    }

    // Delete using Iterator (safe removal)
    public synchronized void deleteMedicine(String id) {
        Iterator<Medicine> it = medicineList.iterator();
        while (it.hasNext()) {
            if (it.next().getMedicineId().equals(id)) { it.remove(); break; }
        }
        medicineMap.remove(id);
        dataStore.saveAll(medicineList);
    }

    public Medicine getMedicineById(String id) { return medicineMap.get(id); }

    // Sort by name using Comparable
    public ArrayList<Medicine> getSortedByName() {
        ArrayList<Medicine> sorted = new ArrayList<>(medicineList);
        Collections.sort(sorted);
        return sorted;
    }

    // Sort by price using Comparator
    public ArrayList<Medicine> getSortedByPrice() {
        ArrayList<Medicine> sorted = new ArrayList<>(medicineList);
        Collections.sort(sorted, (m1, m2) ->
            Double.compare(m1.getPrice(), m2.getPrice()));
        return sorted;
    }

    public ArrayList<Medicine> getLowStockMedicines() {
        ArrayList<Medicine> low = new ArrayList<>();
        for (Medicine m : medicineList)
            if (m.getQuantity() < LOW_STOCK_THRESHOLD) low.add(m);
        return low;
    }

    public synchronized boolean reduceStock(String id, int qty) {
        Medicine med = medicineMap.get(id);
        if (med != null && med.getQuantity() >= qty) {
            med.setQuantity(med.getQuantity() - qty);
            dataStore.saveAll(medicineList);
            return true;
        }
        return false;
    }

    public ArrayList<Medicine> getAllMedicines() { return medicineList; }
    public int getMedicineCount()               { return medicineList.size(); }
}'''))

# 6. BillingService.java
story.append(sub_hdr('6. BillingService.java'))
story.append(body(
    'This file manages all billing operations. When a bill is created, stock is reduced for '
    'each medicine and the bill is saved to persistent storage. A formatted invoice text file '
    'is generated using FileWriter for each completed transaction. Billing is processed in a '
    'separate BillingThread to keep the UI responsive. The Bill class demonstrates method '
    'overloading with two versions of applyDiscount().'
))
story.append(body('Code for BillingService.java file:'))
story.append(code(
'''package com.pharmacy.service;

import com.pharmacy.model.Bill;
import com.pharmacy.model.BillItem;
import com.pharmacy.util.DataStore;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

public class BillingService {

    private ArrayList<Bill> billList;
    private DataStore<Bill> dataStore;
    private InventoryManager inventoryManager;

    public BillingService(InventoryManager inventoryManager) {
        this.inventoryManager = inventoryManager;
        dataStore = new DataStore<>("data/bills.dat");
        billList  = dataStore.loadAll();
    }

    public synchronized boolean createBill(Bill bill) {
        for (BillItem item : bill.getItems()) {
            boolean ok = inventoryManager.reduceStock(
                item.getMedicineId(), item.getQuantity());
            if (!ok) return false;  // Insufficient stock
        }
        billList.add(bill);
        dataStore.saveAll(billList);
        generateInvoice(bill);
        return true;
    }

    // Invoice generation using FileWriter
    public void generateInvoice(Bill bill) {
        String path = "data/invoices/" + bill.getBillId() + "_invoice.txt";
        try (FileWriter writer = new FileWriter(path)) {
            writer.write("======= PHARMACARE INVOICE =======\n");
            writer.write("Invoice No : " + bill.getBillId() + "\n");
            writer.write("Customer   : " + bill.getCustomerName() + "\n");
            writer.write("Date       : " + bill.getDate() + "\n");
            writer.write("----------------------------------\n");
            for (BillItem item : bill.getItems()) {
                writer.write(String.format("%-18s x%d = Rs.%.2f\n",
                    item.getMedicineName(), item.getQuantity(), item.getSubtotal()));
            }
            writer.write("----------------------------------\n");
            writer.write(String.format("Net Amount : Rs.%.2f\n", bill.getNetAmount()));
            writer.write("     Thank you! Get well soon!   \n");
        } catch (IOException e) { System.err.println("Invoice error: " + e.getMessage()); }
    }

    // Method overloading for discount
    public void applyDiscount(Bill bill, double percentage) {
        bill.applyDiscount(percentage);
    }
    public void applyDiscount(Bill bill, double amount, boolean isFixed) {
        bill.applyDiscount(amount, isFixed);
    }

    public double getTotalSales() {
        double total = 0;
        for (Bill b : billList) total += b.getNetAmount();
        return total;
    }
    public ArrayList<Bill> getAllBills() { return billList; }
}'''))

print("Part 4 ok")

# 7. Customer.java / CustomerService.java
story.append(sub_hdr('7. Customer.java / CustomerService.java'))
story.append(body(
    'These files handle customer and patient information. Customer.java is the model class '
    'storing customer ID, name, phone, email, and address. CustomerService.java manages all '
    'CRUD operations on customer records — adding, updating, deleting, and searching. '
    'It uses a HashMap for fast ID-based lookups and an Iterator for safe deletion. '
    'All data is persisted using the generic DataStore class.'
))
story.append(body('Code for Customer.java file:'))
story.append(code(
'''package com.pharmacy.model;
import java.io.Serializable;

public class Customer implements Serializable {
    private static final long serialVersionUID = 1L;
    private String customerId, name, phone, email, address;

    public Customer(String customerId, String name,
                    String phone, String email, String address) {
        this.customerId = customerId;
        this.name = name;   this.phone = phone;
        this.email = email; this.address = address;
    }

    // Encapsulation - Getters and Setters
    public String getCustomerId() { return customerId; }
    public String getName()       { return name; }
    public String getPhone()      { return phone; }
    public void setName(String n) { this.name = n; }
    public void setPhone(String p){ this.phone = p; }

    @Override
    public String toString() {
        return customerId + " | " + name + " | " + phone;
    }
}'''))

story.append(body('Code for CustomerService.java file:'))
story.append(code(
'''package com.pharmacy.service;
import com.pharmacy.model.Customer;
import com.pharmacy.util.DataStore;
import java.util.*;

public class CustomerService {
    private ArrayList<Customer> customerList;
    private HashMap<String, Customer> customerMap;
    private DataStore<Customer> dataStore;

    public CustomerService() {
        dataStore    = new DataStore<>("data/customers.dat");
        customerList = dataStore.loadAll();
        customerMap  = new HashMap<>();
        for (Customer c : customerList)
            customerMap.put(c.getCustomerId(), c);
    }

    public synchronized void addCustomer(Customer customer) {
        customerList.add(customer);
        customerMap.put(customer.getCustomerId(), customer);
        dataStore.saveAll(customerList);
    }

    // Delete using Iterator
    public synchronized void deleteCustomer(String id) {
        Iterator<Customer> it = customerList.iterator();
        while (it.hasNext()) {
            if (it.next().getCustomerId().equals(id)) { it.remove(); break; }
        }
        customerMap.remove(id);
        dataStore.saveAll(customerList);
    }

    public Customer getCustomerById(String id) { return customerMap.get(id); }

    public ArrayList<Customer> searchByName(String name) {
        ArrayList<Customer> results = new ArrayList<>();
        for (Customer c : customerList)
            if (c.getName().toLowerCase().contains(name.toLowerCase()))
                results.add(c);
        return results;
    }
    public ArrayList<Customer> getAllCustomers() { return customerList; }
}'''))

# 8. DataStore.java
story.append(sub_hdr('8. DataStore.java'))
story.append(body(
    'This file handles all data persistence for the system. It is implemented as a generic '
    'class (DataStore<T extends Serializable>) so it can be reused across all service classes. '
    'The same DataStore handles Medicine, Customer, Supplier, Bill, and Prescription objects. '
    'It uses ObjectOutputStream and FileOutputStream to serialize objects, and ObjectInputStream '
    'and FileInputStream to deserialize them. FileWriter creates human-readable text backups '
    'and FileReader reads them. All methods are synchronized for thread safety.'
))
story.append(body('Code for DataStore.java file:'))
story.append(code(
'''package com.pharmacy.util;
import java.io.*;
import java.util.ArrayList;

// Generic class - works for any Serializable type
public class DataStore<T extends Serializable> {

    private String filePath;

    public DataStore(String filePath) { this.filePath = filePath; }

    // Serialization - save using ObjectOutputStream + FileOutputStream
    public synchronized void saveAll(ArrayList<T> items) {
        try (FileOutputStream fos = new FileOutputStream(filePath);
             ObjectOutputStream oos = new ObjectOutputStream(fos)) {
            oos.writeObject(items);  // Serialization
        } catch (IOException e) { System.err.println("Save error: " + e.getMessage()); }
    }

    // Deserialization - load using ObjectInputStream + FileInputStream
    @SuppressWarnings("unchecked")
    public synchronized ArrayList<T> loadAll() {
        File file = new File(filePath);
        if (!file.exists()) return new ArrayList<>();
        try (FileInputStream fis = new FileInputStream(filePath);
             ObjectInputStream ois = new ObjectInputStream(fis)) {
            return (ArrayList<T>) ois.readObject(); // Deserialization
        } catch (IOException | ClassNotFoundException e) { return new ArrayList<>(); }
    }

    // Text backup using FileWriter
    public void backupToText(ArrayList<T> items, String backupPath) {
        try (FileWriter writer = new FileWriter(backupPath)) {
            writer.write("=== BACKUP: " + filePath + " ===\n");
            for (T item : items) writer.write(item.toString() + "\n");
        } catch (IOException e) { System.err.println("Backup error: " + e.getMessage()); }
    }

    // Read backup using FileReader
    public String readBackup(String backupPath) {
        StringBuilder sb = new StringBuilder();
        try (FileReader reader = new FileReader(backupPath)) {
            int ch;
            while ((ch = reader.read()) != -1) sb.append((char) ch);
        } catch (IOException e) { return "No backup found."; }
        return sb.toString();
    }
}'''))

print("Part 5 ok")

# ── RESULTS ────────────────────────────────────────────────────────────────
story.append(PageBreak())
story.append(sec_hdr('Results'))
story += [sp(6)]

screens = [
    ('Login Screen', '''\
+-------------------------------------------------------+
|                                                       |
|              PharmaCare                               |
|       Pharmacy Management System                      |
|                                                       |
|  +------------------------------------------+         |
|  |              Login                       |         |
|  |                                          |         |
|  |  Username: [ admin                     ] |         |
|  |  Password: [ ........                  ] |         |
|  |                                          |         |
|  |       [         Login          ]         |         |
|  |                                          |         |
|  |  Invalid credentials! Please try again.  |         |
|  +------------------------------------------+         |
|   Default: admin/admin123 or pharmacist/pharma123     |
+-------------------------------------------------------+'''),

    ('Dashboard Screen', '''\
+==================================================================+
| PharmaCare Dashboard    Welcome, Administrator    [Logout]       |
+==================================================================+
|                                                                  |
|  +------------------+  +------------------+  +----------------+ |
|  | Inventory        |  | Sales &          |  | Supplier       | |
|  | Management       |  | Billing          |  | Management     | |
|  | (Blue)           |  | (Green)          |  | (Orange)       | |
|  +------------------+  +------------------+  +----------------+ |
|                                                                  |
|  +------------------+  +------------------+  +----------------+ |
|  | Customer         |  | Prescription     |  | Reports &      | |
|  | Records          |  | Handling         |  | Alerts         | |
|  | (Purple)         |  | (Teal)           |  | (Red)          | |
|  +------------------+  +------------------+  +----------------+ |
|                                                                  |
+------------------------------------------------------------------+
| Medicines: 10 | Customers: 3 | Suppliers: 3 | Bills: 0          |
+==================================================================+'''),

    ('Inventory Management Screen', '''\
+=========+=====================================================+
| [< Back]  Inventory Management                              |
+===========+================================================++
| Add/Edit  | [Search:_________][Search][Sort v][Filter v]   |
| --------- +------------------------------------------------+|
| ID: [auto]| ID     |Name           |Cat |Expiry |Qty|Price  |
| Name:[  ] |--------+---------------+----+-------+---+------ |
| Mfg: [  ] | MED101 |Paracetamol    |Tab |2026.. |500| 12.50 |
| Cat: [  v]| MED102 |Amoxicillin    |Cap |2026.. |200| 45.00 |
| Batch:[  ]| MED103 |Cough Syrup    |Syr |2026.. |150| 85.00 |
| Expiry:[  ]| MED104|Insulin Inj.   |Inj |2025.. | 50|350.00 |
| Qty: [  ] | MED106 |Eye Drops      |Drp |2026.. |  8|120.00 |
| Price:[  ]| MED107 |Salbutamol Inh.|Inh |2026.. |  5|250.00 |
|           |                                                  |
|[Add][Upd] |                                                  |
|[Del][Clr] |                                                  |
+===========+==================================================+'''),

    ('Sales & Billing Screen', '''\
+=================+=============================================+
| [< Back]  Sales & Billing                                    |
+=================+=============================================+
| Customer ID:[  ]| Current Bill Items                        |
| Name: [       ] | Medicine        |Qty| Price | Subtotal    |
|                 |-----------------+---+-------+-------------|
| Add Medicine    | Paracetamol 500 | 5 | 12.50 |    62.50    |
| Med ID: [     ] | Cough Syrup     | 2 | 85.00 |   170.00    |
| Name: Cough..   |                 |   |       |             |
| Price: Rs.85.00 |                 |   |       |             |
| Stock: 150      |--------------------------------------------|
| Qty:  [       ] |  Total:    Rs. 232.50                     |
| [Add to Bill  ] |  Discount %: [ 0 ]                        |
|                 |  Net:      Rs. 232.50                     |
|                 |                                           |
|                 |  [Generate Bill (Threaded)] [Clear Bill]  |
+=================+===========================================++'''),

    ('Supplier Management Screen', '''\
+=========+=====================================================+
| [< Back]  Supplier Management                               |
+==========+====================================================+
| Add/Edit | [Search:_____________][Search] [Show All]        |
| -------- +--------------------------------------------------+|
| ID:[auto]| ID     |Company         |Contact    |Phone       |
| Company: |--------+----------------+-----------+----------- |
| Contact: | SUP301 |PharmaCorp India|Rajesh K.  |987654..    |
| Phone:   | SUP302 |MediLife Supply |Priya S.   |987654..    |
| Email:   | SUP303 |HealthFirst Ph. |Amit P.    |987654..    |
| Address: |                                                   |
|          |                                                   |
|[Add][Upd]|                                                   |
|[Del][Clr]|                                                   |
+=========+====================================================+'''),

    ('Customer Records Screen', '''\
+=========+=====================================================+
| [< Back]  Customer / Patient Records                        |
+==========+====================================================+
| Add/Edit | [Search:_____________][Search] [Show All]        |
| -------- +--------------------------------------------------+|
| ID:[auto]| ID     |Name           |Phone      |Email        |
| Name:[  ]|--------+---------------+-----------+-------------|
| Phone:[  ]| CUS201|Rahul Verma    |9123456789 |rahul@..     |
| Email:[  ]| CUS202|Sneha Iyer     |9123456790 |sneha@..     |
| Addr: [  ]| CUS203|Mohammed Ali   |9123456791 |ali@...      |
|           |                                                  |
|[Add][Upd] |                                                  |
|[Del][Clr] |                                                  |
+===========+==================================================+'''),

    ('Prescription Handling Screen', '''\
+==================+=============================================+
| [< Back]  Prescription Handling                              |
+==================+=============================================+
| New Prescription | All Prescriptions                        |
| ---------------- | ID    |Patient    |Doctor  |Date         |
| Cust ID:[      ] |-------+-----------+--------+-------------|
| Patient:[      ] | PRE01 |Rahul V.   |Dr.Nair |2026-04-04   |
| Doctor: [      ] | PRE02 |Sneha I.   |Dr.Raju |2026-04-04   |
| Notes:  [      ] |                                          |
| ---------------- | Details:                                 |
| Med ID: [      ] | Prescription: PRE5001                    |
| Name: Paracetam. | Patient: Rahul Verma                     |
| Qty:  [        ] | Doctor: Dr. Nair                         |
| Dosage:[  1-0-1] | Medicines:                               |
| [Add Medicine  ] |  - Paracetamol x2 (1-0-1)               |
| * Paracetamol x2 |  - Cough Syrup x1 (0-0-1)               |
| [Save Prescript] |                                          |
+==================+==========================================+'''),

    ('Reports & Alerts Screen', '''\
+================+================================================+
| [< Back]  Reports & Alerts                                     |
+================+================================================+
| [Sales Report] |  System Summary                              |
| [Stock Report] |                                              |
| [Expiry Alert] |  +----------+ +----------+ +------------+   |
| [Low Stock   ] |  |    10    | |    3     | |     3      |   |
| [Summary     ] |  |Medicines | |Customers | | Suppliers  |   |
| -------------- |  +----------+ +----------+ +------------+   |
| [Backup Data ] |  +----------+ +----------+ +------------+   |
|                |  |    5     | |Rs.232.50 | |     2      |   |
|                |  |  Bills   | |  Sales   | | Low Stock  |   |
|                |  +----------+ +----------+ +------------+   |
|                |                                              |
|                |  Background Threads:                         |
|                |  Expiry Alert Thread : RUNNING               |
|                |  Stock Alert Thread  : RUNNING (daemon)      |
+================+==============================================+'''),

    ('Generated Invoice (data/invoices/ folder)', '''\
==============================
     PHARMACARE - INVOICE
==============================
Invoice No : BIL4001
Date       : 2026-04-04
Customer   : Rahul Verma
Customer ID: CUS2001
Billed By  : admin
------------------------------
Paracetamol 500mg  x5 = Rs. 62.50
Cough Syrup        x2 = Rs.170.00
------------------------------
Total      : Rs.232.50
Discount   : Rs.  0.00
Net Amount : Rs.232.50
==============================
  Thank you! Get well soon!'''),
]

for screen_name, ascii_art in screens:
    story.append(sub_hdr(screen_name))
    story.append(code(ascii_art))
    story += [sp(4)]

print("Part 6 ok")

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
    '— Encapsulation, Inheritance, Polymorphism, and Abstraction — along with Java Collections, '
    'Generics, Multithreading, File Handling, and Serialization can be applied to solve '
    'real-world problems in healthcare management, resulting in a secure, modular, and '
    'scalable solution.'
))

# ── INDIVIDUAL CONTRIBUTIONS ───────────────────────────────────────────────
story.append(sec_hdr('Individual Contributions'))
story += [sp(6)]

contribs = [
    ('Kenneth Martin, 230905001, Roll No. 01',
     ['PharmacyApp.java', 'LoginScreen.java', 'DashboardScreen.java',
      'UserService.java', 'User.java / UserRole.java']),
    ('Arun Prakash, 230905002, Roll No. 02',
     ['Medicine.java / MedicineCategory.java', 'InventoryManager.java',
      'InventoryScreen.java', 'SampleDataLoader.java']),
    ('Divya Nair, 230905003, Roll No. 03',
     ['BillingService.java', 'BillingThread.java',
      'BillingScreen.java', 'Bill.java / BillItem.java']),
    ('Sanjay Kumar, 230905004, Roll No. 04',
     ['DataStore.java', 'IDGenerator.java',
      'CustomerService.java / SupplierService.java',
      'PrescriptionService.java',
      'ExpiryAlertThread.java / StockAlertThread.java',
      'BackupService.java', 'ReportsScreen.java']),
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
    'unified and robust Pharmacy Management System. This collaborative approach allowed us to '
    'deliver a comprehensive solution while building on each other\'s individual strengths.'
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
print(f"PDF generated: {OUT}")
