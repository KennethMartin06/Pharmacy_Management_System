package com.pharmacy.service;

import com.pharmacy.model.Medicine;
import com.pharmacy.model.MedicineCategory;
import com.pharmacy.util.DataStore;

import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.Iterator;

/**
 * Manages the medicine inventory.
 * Demonstrates: ArrayList, HashMap, Iterator, Collections.sort, Generics, Synchronization.
 */
public class InventoryManager {

    private ArrayList<Medicine> medicineList;
    private HashMap<String, Medicine> medicineMap; // Maps medicineId -> Medicine object
    private DataStore<Medicine> dataStore;

    private static final String DATA_FILE = "data/medicines.dat";
    private static final String BACKUP_FILE = "data/backup_medicines.txt";
    private static final int LOW_STOCK_THRESHOLD = 10;

    public InventoryManager() {
        this.dataStore = new DataStore<>(DATA_FILE);
        this.medicineList = dataStore.loadAll();
        this.medicineMap = new HashMap<>();

        // Populate HashMap from loaded list
        for (Medicine med : medicineList) {
            medicineMap.put(med.getMedicineId(), med);
        }
    }

    // Add medicine (synchronized for thread safety)
    public synchronized void addMedicine(Medicine medicine) {
        medicineList.add(medicine);
        medicineMap.put(medicine.getMedicineId(), medicine);
        saveData();
    }

    // Update medicine
    public synchronized void updateMedicine(Medicine medicine) {
        medicineMap.put(medicine.getMedicineId(), medicine);
        // Update in list as well
        for (int i = 0; i < medicineList.size(); i++) {
            if (medicineList.get(i).getMedicineId().equals(medicine.getMedicineId())) {
                medicineList.set(i, medicine);
                break;
            }
        }
        saveData();
    }

    // Delete medicine using Iterator
    public synchronized void deleteMedicine(String medicineId) {
        Iterator<Medicine> iterator = medicineList.iterator();
        while (iterator.hasNext()) {
            Medicine med = iterator.next();
            if (med.getMedicineId().equals(medicineId)) {
                iterator.remove();
                break;
            }
        }
        medicineMap.remove(medicineId);
        saveData();
    }

    // Get medicine by ID using HashMap
    public Medicine getMedicineById(String medicineId) {
        return medicineMap.get(medicineId);
    }

    // Search medicines by name
    public ArrayList<Medicine> searchByName(String name) {
        ArrayList<Medicine> results = new ArrayList<>();
        for (Medicine med : medicineList) {
            if (med.getName().toLowerCase().contains(name.toLowerCase())) {
                results.add(med);
            }
        }
        return results;
    }

    // Filter by category
    public ArrayList<Medicine> filterByCategory(MedicineCategory category) {
        ArrayList<Medicine> results = new ArrayList<>();
        for (Medicine med : medicineList) {
            if (med.getCategory() == category) {
                results.add(med);
            }
        }
        return results;
    }

    // Sort by name using Collections.sort (Comparable)
    public ArrayList<Medicine> getSortedByName() {
        ArrayList<Medicine> sorted = new ArrayList<>(medicineList);
        Collections.sort(sorted); // Uses Medicine's compareTo
        return sorted;
    }

    // Sort by price using Comparator
    public ArrayList<Medicine> getSortedByPrice() {
        ArrayList<Medicine> sorted = new ArrayList<>(medicineList);
        Collections.sort(sorted, new Comparator<Medicine>() {
            @Override
            public int compare(Medicine m1, Medicine m2) {
                return Double.compare(m1.getPrice(), m2.getPrice());
            }
        });
        return sorted;
    }

    // Sort by expiry date
    public ArrayList<Medicine> getSortedByExpiry() {
        ArrayList<Medicine> sorted = new ArrayList<>(medicineList);
        Collections.sort(sorted, new Comparator<Medicine>() {
            @Override
            public int compare(Medicine m1, Medicine m2) {
                return m1.getExpiryDate().compareTo(m2.getExpiryDate());
            }
        });
        return sorted;
    }

    // Get low stock medicines
    public ArrayList<Medicine> getLowStockMedicines() {
        ArrayList<Medicine> lowStock = new ArrayList<>();
        for (Medicine med : medicineList) {
            if (med.getQuantity() < LOW_STOCK_THRESHOLD) {
                lowStock.add(med);
            }
        }
        return lowStock;
    }

    // Get expired medicines (compare with current date string YYYY-MM-DD)
    public ArrayList<Medicine> getExpiredMedicines(String currentDate) {
        ArrayList<Medicine> expired = new ArrayList<>();
        for (Medicine med : medicineList) {
            if (med.getExpiryDate().compareTo(currentDate) <= 0) {
                expired.add(med);
            }
        }
        return expired;
    }

    // Get medicines expiring soon (within 30 days approximation)
    public ArrayList<Medicine> getExpiringSoon(String currentDate, String thresholdDate) {
        ArrayList<Medicine> expiring = new ArrayList<>();
        for (Medicine med : medicineList) {
            if (med.getExpiryDate().compareTo(currentDate) > 0
                && med.getExpiryDate().compareTo(thresholdDate) <= 0) {
                expiring.add(med);
            }
        }
        return expiring;
    }

    // Reduce stock (for billing)
    public synchronized boolean reduceStock(String medicineId, int quantity) {
        Medicine med = medicineMap.get(medicineId);
        if (med != null && med.getQuantity() >= quantity) {
            med.setQuantity(med.getQuantity() - quantity);
            saveData();
            return true;
        }
        return false;
    }

    // Get all medicines
    public ArrayList<Medicine> getAllMedicines() {
        return medicineList;
    }

    // Save data
    private void saveData() {
        dataStore.saveAll(medicineList);
    }

    // Create backup
    public void createBackup() {
        dataStore.backupToText(medicineList, BACKUP_FILE);
    }

    public int getMedicineCount() {
        return medicineList.size();
    }
}
