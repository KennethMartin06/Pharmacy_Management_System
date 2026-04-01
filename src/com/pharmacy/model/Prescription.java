package com.pharmacy.model;

import java.io.Serializable;
import java.util.ArrayList;

/**
 * Prescription model class linking customer to prescribed medicines.
 * Demonstrates: Encapsulation, Serialization, ArrayList usage.
 */
public class Prescription implements Serializable {
    private static final long serialVersionUID = 1L;

    private String prescriptionId;
    private String customerId;
    private String customerName;
    private String doctorName;
    private String date;
    private ArrayList<PrescriptionItem> items;
    private String notes;

    // Default constructor
    public Prescription() {
        this.items = new ArrayList<>();
    }

    // Parameterized constructor
    public Prescription(String prescriptionId, String customerId, String customerName,
                        String doctorName, String date, String notes) {
        this.prescriptionId = prescriptionId;
        this.customerId = customerId;
        this.customerName = customerName;
        this.doctorName = doctorName;
        this.date = date;
        this.notes = notes;
        this.items = new ArrayList<>();
    }

    // Add item to prescription
    public void addItem(PrescriptionItem item) {
        items.add(item);
    }

    // Getters and Setters
    public String getPrescriptionId() { return prescriptionId; }
    public void setPrescriptionId(String prescriptionId) { this.prescriptionId = prescriptionId; }

    public String getCustomerId() { return customerId; }
    public void setCustomerId(String customerId) { this.customerId = customerId; }

    public String getCustomerName() { return customerName; }
    public void setCustomerName(String customerName) { this.customerName = customerName; }

    public String getDoctorName() { return doctorName; }
    public void setDoctorName(String doctorName) { this.doctorName = doctorName; }

    public String getDate() { return date; }
    public void setDate(String date) { this.date = date; }

    public ArrayList<PrescriptionItem> getItems() { return items; }
    public void setItems(ArrayList<PrescriptionItem> items) { this.items = items; }

    public String getNotes() { return notes; }
    public void setNotes(String notes) { this.notes = notes; }

    @Override
    public String toString() {
        return prescriptionId + " | Patient: " + customerName + " | Dr. " + doctorName + " | " + date;
    }
}
