package com.pharmacy.service;

import com.pharmacy.model.Bill;

/**
 * Multi-threaded billing simulation.
 * Demonstrates: Thread, Runnable, synchronized, sleep(), join().
 *
 * Simulates billing processing in a separate thread to keep UI responsive.
 */
public class BillingThread extends Thread {

    private BillingService billingService;
    private Bill bill;
    private boolean success;
    private String message;
    private BillingCallback callback;

    // Callback interface for billing result (Abstraction)
    public interface BillingCallback {
        void onBillingComplete(boolean success, String message, Bill bill);
    }

    public BillingThread(BillingService billingService, Bill bill, BillingCallback callback) {
        super("BillingThread-" + bill.getBillId());
        this.billingService = billingService;
        this.bill = bill;
        this.callback = callback;
        this.success = false;
        this.message = "";
    }

    @Override
    public void run() {
        try {
            // Simulate processing time
            System.out.println("[" + getName() + "] Processing bill " + bill.getBillId() + "...");
            Thread.sleep(1000); // Simulate processing delay

            // Process the bill
            synchronized (billingService) {
                success = billingService.createBill(bill);
            }

            if (success) {
                message = "Bill " + bill.getBillId() + " processed successfully!";
                System.out.println("[" + getName() + "] " + message);
            } else {
                message = "Failed to process bill " + bill.getBillId() + ". Insufficient stock.";
                System.out.println("[" + getName() + "] " + message);
            }

            // Simulate invoice generation time
            Thread.sleep(500);

        } catch (InterruptedException e) {
            message = "Billing interrupted for " + bill.getBillId();
            Thread.currentThread().interrupt();
        }

        // Callback
        if (callback != null) {
            callback.onBillingComplete(success, message, bill);
        }
    }

    public boolean isSuccess() {
        return success;
    }

    public String getMessage() {
        return message;
    }
}
