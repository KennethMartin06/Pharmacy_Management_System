package com.pharmacy.service;

import com.pharmacy.model.Supplier;
import com.pharmacy.util.DataStore;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;

/**
 * Manages supplier records.
 * Demonstrates: ArrayList, HashMap, Iterator, Generics.
 */
public class SupplierService {

    private ArrayList<Supplier> supplierList;
    private HashMap<String, Supplier> supplierMap;
    private DataStore<Supplier> dataStore;

    private static final String DATA_FILE = "data/suppliers.dat";
    private static final String BACKUP_FILE = "data/backup_suppliers.txt";

    public SupplierService() {
        this.dataStore = new DataStore<>(DATA_FILE);
        this.supplierList = dataStore.loadAll();
        this.supplierMap = new HashMap<>();

        for (Supplier sup : supplierList) {
            supplierMap.put(sup.getSupplierId(), sup);
        }
    }

    public synchronized void addSupplier(Supplier supplier) {
        supplierList.add(supplier);
        supplierMap.put(supplier.getSupplierId(), supplier);
        saveData();
    }

    public synchronized void updateSupplier(Supplier supplier) {
        supplierMap.put(supplier.getSupplierId(), supplier);
        for (int i = 0; i < supplierList.size(); i++) {
            if (supplierList.get(i).getSupplierId().equals(supplier.getSupplierId())) {
                supplierList.set(i, supplier);
                break;
            }
        }
        saveData();
    }

    public synchronized void deleteSupplier(String supplierId) {
        Iterator<Supplier> iterator = supplierList.iterator();
        while (iterator.hasNext()) {
            Supplier sup = iterator.next();
            if (sup.getSupplierId().equals(supplierId)) {
                iterator.remove();
                break;
            }
        }
        supplierMap.remove(supplierId);
        saveData();
    }

    public Supplier getSupplierById(String supplierId) {
        return supplierMap.get(supplierId);
    }

    public ArrayList<Supplier> searchByName(String name) {
        ArrayList<Supplier> results = new ArrayList<>();
        for (Supplier sup : supplierList) {
            if (sup.getCompanyName().toLowerCase().contains(name.toLowerCase())) {
                results.add(sup);
            }
        }
        return results;
    }

    public ArrayList<Supplier> getAllSuppliers() {
        return supplierList;
    }

    private void saveData() {
        dataStore.saveAll(supplierList);
    }

    public void createBackup() {
        dataStore.backupToText(supplierList, BACKUP_FILE);
    }

    public int getSupplierCount() {
        return supplierList.size();
    }
}
