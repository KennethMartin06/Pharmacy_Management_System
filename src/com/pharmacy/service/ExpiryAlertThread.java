package com.pharmacy.service;

import com.pharmacy.model.Medicine;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;

/**
 * Background thread that checks for expired and soon-to-expire medicines.
 * Demonstrates: Thread class, sleep(), join(), synchronized, Runnable.
 */
public class ExpiryAlertThread extends Thread {

    private InventoryManager inventoryManager;
    private volatile boolean running = true;
    private ArrayList<Medicine> expiredMedicines;
    private ArrayList<Medicine> expiringMedicines;
    private final Object lock = new Object();
    private AlertListener listener;

    // Interface for callback (Abstraction demonstration)
    public interface AlertListener {
        void onAlertUpdate(ArrayList<Medicine> expired, ArrayList<Medicine> expiringSoon);
    }

    public ExpiryAlertThread(InventoryManager inventoryManager) {
        super("ExpiryAlertThread");
        this.inventoryManager = inventoryManager;
        this.expiredMedicines = new ArrayList<>();
        this.expiringMedicines = new ArrayList<>();
        setDaemon(true); // Daemon thread - will stop when main thread stops
    }

    public void setAlertListener(AlertListener listener) {
        this.listener = listener;
    }

    @Override
    public void run() {
        while (running) {
            try {
                checkExpiry();

                // Sleep for 30 seconds between checks
                Thread.sleep(30000);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                break;
            }
        }
    }

    // Synchronized method for thread-safe expiry checking
    private synchronized void checkExpiry() {
        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        String currentDate = sdf.format(new Date());

        // Calculate date 30 days from now
        Calendar cal = Calendar.getInstance();
        cal.add(Calendar.DAY_OF_MONTH, 30);
        String thresholdDate = sdf.format(cal.getTime());

        synchronized (lock) {
            expiredMedicines = inventoryManager.getExpiredMedicines(currentDate);
            expiringMedicines = inventoryManager.getExpiringSoon(currentDate, thresholdDate);

            // Notify waiting threads using wait/notify mechanism
            lock.notifyAll();
        }

        // Callback to listener
        if (listener != null) {
            listener.onAlertUpdate(expiredMedicines, expiringMedicines);
        }
    }

    // Method for other threads to wait for alert data
    public ArrayList<Medicine> waitForExpiredList() throws InterruptedException {
        synchronized (lock) {
            lock.wait(5000); // Wait up to 5 seconds
            return new ArrayList<>(expiredMedicines);
        }
    }

    public ArrayList<Medicine> getExpiredMedicines() {
        synchronized (lock) {
            return new ArrayList<>(expiredMedicines);
        }
    }

    public ArrayList<Medicine> getExpiringMedicines() {
        synchronized (lock) {
            return new ArrayList<>(expiringMedicines);
        }
    }

    public void stopChecking() {
        running = false;
        this.interrupt();
    }
}
