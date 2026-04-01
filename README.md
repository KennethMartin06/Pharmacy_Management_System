# PharmaCare - Pharmacy Management System

## OOSD Lab Project

A complete Pharmacy Management System built with **Java** and **JavaFX**, demonstrating Object-Oriented Software Development concepts.

---

## Features

### Core Modules
1. **Inventory Management** - Add, update, delete, search, filter, and sort medicines
2. **Sales & Billing** - Create bills with multi-threaded processing and auto invoice generation
3. **Supplier Management** - Manage supplier records with CRUD operations
4. **Customer/Patient Records** - Track customer information
5. **Prescription Handling** - Record prescriptions with medicines and dosage
6. **Reports & Alerts** - Sales reports, stock/expiry alerts, data backup

### Smart Enhancements
- Expiry alert system (background thread checks dates)
- Low stock alert system (background thread monitors quantity)
- Auto invoice generator (saves text invoices in `data/invoices/`)
- Search + filter medicines by name and category
- Sorting by price, name, and expiry date
- Multi-threaded billing simulation
- File backup system (serialization + text backup)
- Role-based login (Admin / Pharmacist)

---

## OOP Concepts Demonstrated

| Concept | Where Used |
|---------|-----------|
| **Encapsulation** | All model classes (private fields, getters/setters) |
| **Inheritance** | `PharmacyApp extends Application`, `ExpiryAlertThread extends Thread` |
| **Polymorphism** | Method overloading in `Bill.applyDiscount()`, `Medicine.compareTo()` |
| **Abstraction** | Callback interfaces (`AlertListener`, `BillingCallback`) |
| **Constructors** | Default + parameterized constructors in all models |
| **Method Overloading** | `Bill.applyDiscount(double)` vs `applyDiscount(double, boolean)` |
| **Method Overriding** | `toString()`, `run()`, `compareTo()` |
| **Wrapper Classes** | `Integer`, `Double` in Medicine, Bill (autoboxing/unboxing) |
| **Enum** | `MedicineCategory`, `UserRole` |
| **Multithreading** | `ExpiryAlertThread`, `StockAlertThread`, `BillingThread`, `BackupService` |
| **Thread/Runnable** | Thread class (ExpiryAlert) and Runnable interface (StockAlert, Backup) |
| **sleep/join** | Used in BillingThread and alert threads |
| **Synchronization** | `synchronized` methods in services, `wait/notify` in ExpiryAlertThread |
| **Serialization** | `DataStore<T>` saves/loads objects via ObjectOutputStream/ObjectInputStream |
| **File I/O** | FileWriter (invoices, backups), FileReader (backup reading) |
| **Generics** | `DataStore<T extends Serializable>` - reusable for all model types |
| **ArrayList** | Stores medicines, customers, suppliers, bills, prescriptions |
| **HashMap** | Maps ID -> Object for fast lookups in all services |
| **Iterator** | Used in delete operations (InventoryManager, CustomerService) |
| **Collections.sort** | Sorting medicines by name, price, expiry |
| **JavaFX** | All UI screens using Button, TextField, Label, TableView, GridPane, VBox |

---

## Project Structure

```
src/
└── com/
    └── pharmacy/
        ├── model/              # Data models
        │   ├── Medicine.java
        │   ├── MedicineCategory.java (Enum)
        │   ├── Customer.java
        │   ├── Supplier.java
        │   ├── Prescription.java
        │   ├── PrescriptionItem.java
        │   ├── Bill.java
        │   ├── BillItem.java
        │   ├── User.java
        │   └── UserRole.java (Enum)
        ├── service/            # Business logic
        │   ├── InventoryManager.java
        │   ├── BillingService.java
        │   ├── CustomerService.java
        │   ├── SupplierService.java
        │   ├── PrescriptionService.java
        │   ├── UserService.java
        │   ├── ExpiryAlertThread.java
        │   ├── StockAlertThread.java
        │   ├── BillingThread.java
        │   └── BackupService.java
        ├── util/               # Utilities
        │   ├── DataStore.java (Generic)
        │   ├── IDGenerator.java
        │   └── SampleDataLoader.java
        └── ui/                 # JavaFX GUI
            ├── PharmacyApp.java (Main)
            ├── LoginScreen.java
            ├── DashboardScreen.java
            ├── InventoryScreen.java
            ├── BillingScreen.java
            ├── SupplierScreen.java
            ├── CustomerScreen.java
            ├── PrescriptionScreen.java
            └── ReportsScreen.java
```

---

## How to Run

### Prerequisites
- **Java JDK 17+** (with JavaFX included, or OpenJFX separately)
- If using OpenJDK without JavaFX bundled, download [OpenJFX](https://openjfx.io/)

### Option 1: Using JDK with JavaFX included (e.g., Liberica Full JDK, Azul Zulu FX)
```bash
# Compile
javac -d out src/com/pharmacy/model/*.java src/com/pharmacy/util/*.java src/com/pharmacy/service/*.java src/com/pharmacy/ui/*.java

# Run
java -cp out com.pharmacy.ui.PharmacyApp
```

### Option 2: Using OpenJDK + OpenJFX
```bash
# Set JavaFX path
export PATH_TO_FX=/path/to/javafx-sdk/lib

# Compile
javac --module-path $PATH_TO_FX --add-modules javafx.controls -d out src/com/pharmacy/model/*.java src/com/pharmacy/util/*.java src/com/pharmacy/service/*.java src/com/pharmacy/ui/*.java

# Run
java --module-path $PATH_TO_FX --add-modules javafx.controls -cp out com.pharmacy.ui.PharmacyApp
```

---

## Default Login Credentials

| Role | Username | Password |
|------|----------|----------|
| Admin | admin | admin123 |
| Pharmacist | pharmacist | pharma123 |

---

## Screens Overview

1. **Login Screen** - Username/password authentication with role detection
2. **Dashboard** - 6 module buttons with quick stats in status bar
3. **Inventory** - Left form + right table; search, filter by category, sort by name/price/expiry
4. **Sales & Billing** - Add items to bill, multi-threaded processing, auto invoice generation
5. **Suppliers** - CRUD operations with search
6. **Customers** - CRUD operations with search
7. **Prescriptions** - Add prescriptions with multiple medicines and dosage
8. **Reports** - Sales report, stock report, expiry alerts, low stock alerts, summary, backup

---

## Data Storage

- Data is stored using **Java Serialization** in the `data/` directory
- Text backups are created via **FileWriter** in `data/backup_*.txt`
- Invoices are generated as text files in `data/invoices/`

---

## Authors

OOSD Lab Project - Pharmacy Management System
