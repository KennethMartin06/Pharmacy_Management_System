package com.pharmacy.service;

/**
 * Backup service that creates file backups of all data.
 * Demonstrates: Runnable, Thread, FileWriter (via DataStore).
 */
public class BackupService implements Runnable {

    private InventoryManager inventoryManager;
    private CustomerService customerService;
    private SupplierService supplierService;
    private BillingService billingService;
    private PrescriptionService prescriptionService;
    private BackupCallback callback;

    public interface BackupCallback {
        void onBackupComplete(String message);
    }

    public BackupService(InventoryManager inventoryManager, CustomerService customerService,
                          SupplierService supplierService, BillingService billingService,
                          PrescriptionService prescriptionService) {
        this.inventoryManager = inventoryManager;
        this.customerService = customerService;
        this.supplierService = supplierService;
        this.billingService = billingService;
        this.prescriptionService = prescriptionService;
    }

    public void setCallback(BackupCallback callback) {
        this.callback = callback;
    }

    @Override
    public void run() {
        try {
            System.out.println("[BackupService] Starting backup...");
            Thread.sleep(500);

            inventoryManager.createBackup();
            Thread.sleep(200);

            customerService.createBackup();
            Thread.sleep(200);

            supplierService.createBackup();
            Thread.sleep(200);

            billingService.createBackup();
            Thread.sleep(200);

            prescriptionService.createBackup();
            Thread.sleep(200);

            String msg = "All data backed up successfully!";
            System.out.println("[BackupService] " + msg);

            if (callback != null) {
                callback.onBackupComplete(msg);
            }
        } catch (InterruptedException e) {
            Thread.currentThread().interrupt();
            if (callback != null) {
                callback.onBackupComplete("Backup interrupted!");
            }
        }
    }
}
