package com.pharmacy.service;

import com.pharmacy.model.Bill;
import com.pharmacy.model.BillItem;
import com.pharmacy.util.DataStore;

import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;

/**
 * Manages billing and invoice operations.
 * Demonstrates: ArrayList, Serialization, FileWriter, Method overloading.
 */
public class BillingService {

    private ArrayList<Bill> billList;
    private DataStore<Bill> dataStore;
    private InventoryManager inventoryManager;

    private static final String DATA_FILE = "data/bills.dat";
    private static final String BACKUP_FILE = "data/backup_bills.txt";
    private static final String INVOICE_DIR = "data/invoices/";

    public BillingService(InventoryManager inventoryManager) {
        this.inventoryManager = inventoryManager;
        this.dataStore = new DataStore<>(DATA_FILE);
        this.billList = dataStore.loadAll();
    }

    // Create and save a bill
    public synchronized boolean createBill(Bill bill) {
        // Reduce stock for each item
        for (BillItem item : bill.getItems()) {
            boolean success = inventoryManager.reduceStock(item.getMedicineId(), item.getQuantity());
            if (!success) {
                return false; // Insufficient stock
            }
        }
        billList.add(bill);
        saveData();
        generateInvoice(bill);
        return true;
    }

    /**
     * Generate invoice as text file.
     * Demonstrates: FileWriter usage.
     */
    public void generateInvoice(Bill bill) {
        java.io.File dir = new java.io.File(INVOICE_DIR);
        if (!dir.exists()) {
            dir.mkdirs();
        }
        String invoicePath = INVOICE_DIR + bill.getBillId() + "_invoice.txt";
        try (FileWriter writer = new FileWriter(invoicePath)) {
            writer.write("╔══════════════════════════════════════════════╗\n");
            writer.write("║        PHARMA CARE - INVOICE                ║\n");
            writer.write("╚══════════════════════════════════════════════╝\n\n");
            writer.write("Invoice No  : " + bill.getBillId() + "\n");
            writer.write("Date        : " + bill.getDate() + "\n");
            writer.write("Customer    : " + bill.getCustomerName() + "\n");
            writer.write("Customer ID : " + bill.getCustomerId() + "\n");
            writer.write("Billed By   : " + bill.getBilledBy() + "\n");
            writer.write("──────────────────────────────────────────────\n");
            writer.write(String.format("%-20s %5s %10s %12s\n", "Medicine", "Qty", "Price", "Subtotal"));
            writer.write("──────────────────────────────────────────────\n");

            for (BillItem item : bill.getItems()) {
                writer.write(String.format("%-20s %5d %10.2f %12.2f\n",
                    item.getMedicineName(),
                    item.getQuantity(),
                    item.getUnitPrice(),
                    item.getSubtotal()));
            }

            writer.write("──────────────────────────────────────────────\n");
            writer.write(String.format("%-37s %12.2f\n", "Total:", bill.getTotalAmount()));
            writer.write(String.format("%-37s %12.2f\n", "Discount:", bill.getDiscount()));
            writer.write(String.format("%-37s %12.2f\n", "Net Amount:", bill.getNetAmount()));
            writer.write("══════════════════════════════════════════════\n");
            writer.write("\n        Thank you for your purchase!\n");
            writer.write("           Get well soon!\n");
        } catch (IOException e) {
            System.err.println("Error generating invoice: " + e.getMessage());
        }
    }

    // Get all bills
    public ArrayList<Bill> getAllBills() {
        return billList;
    }

    // Get bills by date
    public ArrayList<Bill> getBillsByDate(String date) {
        ArrayList<Bill> results = new ArrayList<>();
        for (Bill bill : billList) {
            if (bill.getDate().equals(date)) {
                results.add(bill);
            }
        }
        return results;
    }

    // Get total sales
    public double getTotalSales() {
        double total = 0.0;
        for (Bill bill : billList) {
            total += bill.getNetAmount();
        }
        return total;
    }

    // Get total sales for a date
    public double getTotalSalesByDate(String date) {
        double total = 0.0;
        for (Bill bill : billList) {
            if (bill.getDate().equals(date)) {
                total += bill.getNetAmount();
            }
        }
        return total;
    }

    private void saveData() {
        dataStore.saveAll(billList);
    }

    public void createBackup() {
        dataStore.backupToText(billList, BACKUP_FILE);
    }

    public int getBillCount() {
        return billList.size();
    }
}
