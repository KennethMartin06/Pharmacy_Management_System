package com.pharmacy.util;

import com.pharmacy.model.*;
import com.pharmacy.service.*;

/**
 * Loads sample data for demonstration purposes.
 * Demonstrates: Object creation, Enum usage, ArrayList operations.
 */
public class SampleDataLoader {

    public static void loadSampleData(InventoryManager inventoryManager,
                                       CustomerService customerService,
                                       SupplierService supplierService) {

        // Only load if no data exists
        if (inventoryManager.getMedicineCount() > 0) {
            return;
        }

        // Sample Suppliers
        Supplier s1 = new Supplier("SUP3001", "PharmaCorp India", "Rajesh Kumar",
                "9876543210", "rajesh@pharmacorp.com", "Mumbai, Maharashtra");
        Supplier s2 = new Supplier("SUP3002", "MediLife Supplies", "Priya Sharma",
                "9876543211", "priya@medilife.com", "Delhi, India");
        Supplier s3 = new Supplier("SUP3003", "HealthFirst Pharma", "Amit Patel",
                "9876543212", "amit@healthfirst.com", "Ahmedabad, Gujarat");

        supplierService.addSupplier(s1);
        supplierService.addSupplier(s2);
        supplierService.addSupplier(s3);

        // Sample Medicines
        inventoryManager.addMedicine(new Medicine("MED1001", "Paracetamol 500mg", "Sun Pharma",
                MedicineCategory.TABLET, "BT001", "2026-12-15", 500, 12.50, "SUP3001"));
        inventoryManager.addMedicine(new Medicine("MED1002", "Amoxicillin 250mg", "Cipla",
                MedicineCategory.CAPSULE, "BT002", "2026-06-20", 200, 45.00, "SUP3001"));
        inventoryManager.addMedicine(new Medicine("MED1003", "Cough Syrup", "Himalaya",
                MedicineCategory.SYRUP, "BT003", "2026-03-10", 150, 85.00, "SUP3002"));
        inventoryManager.addMedicine(new Medicine("MED1004", "Insulin Injection", "Novo Nordisk",
                MedicineCategory.INJECTION, "BT004", "2025-08-25", 50, 350.00, "SUP3003"));
        inventoryManager.addMedicine(new Medicine("MED1005", "Dettol Ointment", "Reckitt",
                MedicineCategory.OINTMENT, "BT005", "2027-01-30", 300, 65.00, "SUP3002"));
        inventoryManager.addMedicine(new Medicine("MED1006", "Eye Drops", "Alcon",
                MedicineCategory.DROPS, "BT006", "2026-09-15", 8, 120.00, "SUP3003"));
        inventoryManager.addMedicine(new Medicine("MED1007", "Salbutamol Inhaler", "Cipla",
                MedicineCategory.INHALER, "BT007", "2026-11-20", 5, 250.00, "SUP3001"));
        inventoryManager.addMedicine(new Medicine("MED1008", "ORS Powder", "WHO Standard",
                MedicineCategory.POWDER, "BT008", "2027-06-10", 1000, 15.00, "SUP3002"));
        inventoryManager.addMedicine(new Medicine("MED1009", "Azithromycin 500mg", "Zydus",
                MedicineCategory.TABLET, "BT009", "2026-04-05", 100, 75.00, "SUP3001"));
        inventoryManager.addMedicine(new Medicine("MED1010", "Vitamin D3", "HealthVit",
                MedicineCategory.CAPSULE, "BT010", "2026-10-30", 400, 30.00, "SUP3003"));

        // Sample Customers
        customerService.addCustomer(new Customer("CUS2001", "Rahul Verma", "9123456789",
                "rahul@email.com", "Bangalore, Karnataka"));
        customerService.addCustomer(new Customer("CUS2002", "Sneha Iyer", "9123456790",
                "sneha@email.com", "Chennai, Tamil Nadu"));
        customerService.addCustomer(new Customer("CUS2003", "Mohammed Ali", "9123456791",
                "ali@email.com", "Hyderabad, Telangana"));

        // Update ID counters
        IDGenerator.updateCounters(1010, 2003, 3003, 4000, 5000);
    }
}
