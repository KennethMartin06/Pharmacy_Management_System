package com.pharmacy.service;

import com.pharmacy.model.Prescription;
import com.pharmacy.util.DataStore;

import java.util.ArrayList;
import java.util.HashMap;

/**
 * Manages prescription records.
 * Demonstrates: ArrayList, HashMap, Generics, Serialization.
 */
public class PrescriptionService {

    private ArrayList<Prescription> prescriptionList;
    private HashMap<String, Prescription> prescriptionMap;
    private DataStore<Prescription> dataStore;

    private static final String DATA_FILE = "data/prescriptions.dat";
    private static final String BACKUP_FILE = "data/backup_prescriptions.txt";

    public PrescriptionService() {
        this.dataStore = new DataStore<>(DATA_FILE);
        this.prescriptionList = dataStore.loadAll();
        this.prescriptionMap = new HashMap<>();

        for (Prescription pres : prescriptionList) {
            prescriptionMap.put(pres.getPrescriptionId(), pres);
        }
    }

    public synchronized void addPrescription(Prescription prescription) {
        prescriptionList.add(prescription);
        prescriptionMap.put(prescription.getPrescriptionId(), prescription);
        saveData();
    }

    public synchronized void deletePrescription(String prescriptionId) {
        prescriptionList.removeIf(p -> p.getPrescriptionId().equals(prescriptionId));
        prescriptionMap.remove(prescriptionId);
        saveData();
    }

    public Prescription getPrescriptionById(String prescriptionId) {
        return prescriptionMap.get(prescriptionId);
    }

    public ArrayList<Prescription> getByCustomerId(String customerId) {
        ArrayList<Prescription> results = new ArrayList<>();
        for (Prescription pres : prescriptionList) {
            if (pres.getCustomerId().equals(customerId)) {
                results.add(pres);
            }
        }
        return results;
    }

    public ArrayList<Prescription> getAllPrescriptions() {
        return prescriptionList;
    }

    private void saveData() {
        dataStore.saveAll(prescriptionList);
    }

    public void createBackup() {
        dataStore.backupToText(prescriptionList, BACKUP_FILE);
    }

    public int getPrescriptionCount() {
        return prescriptionList.size();
    }
}
