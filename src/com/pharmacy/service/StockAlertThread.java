package com.pharmacy.service;

import com.pharmacy.model.Medicine;

import java.util.ArrayList;

/**
 * Background thread that monitors low stock levels.
 * Demonstrates: Runnable interface, Thread, sleep(), synchronized.
 */
public class StockAlertThread implements Runnable {

    private InventoryManager inventoryManager;
    private volatile boolean running = true;
    private ArrayList<Medicine> lowStockMedicines;
    private AlertListener listener;

    // Callback interface (Abstraction)
    public interface AlertListener {
        void onLowStockUpdate(ArrayList<Medicine> lowStockMedicines);
    }

    public StockAlertThread(InventoryManager inventoryManager) {
        this.inventoryManager = inventoryManager;
        this.lowStockMedicines = new ArrayList<>();
    }

    public void setAlertListener(AlertListener listener) {
        this.listener = listener;
    }

    @Override
    public void run() {
        while (running) {
            try {
                checkStock();
                Thread.sleep(30000); // Check every 30 seconds
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }

    private synchronized void checkStock() {
        lowStockMedicines = inventoryManager.getLowStockMedicines();
        if (listener != null) {
            listener.onLowStockUpdate(lowStockMedicines);
        }
    }

    public synchronized ArrayList<Medicine> getLowStockMedicines() {
        return new ArrayList<>(lowStockMedicines);
    }

    public void stopChecking() {
        running = false;
    }
}
