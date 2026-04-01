package com.pharmacy.model;

import java.io.Serializable;

/**
 * Individual item within a prescription.
 * Demonstrates: Encapsulation, Serialization.
 */
public class PrescriptionItem implements Serializable {
    private static final long serialVersionUID = 1L;

    private String medicineId;
    private String medicineName;
    private Integer quantity;
    private String dosage;

    public PrescriptionItem() {
    }

    public PrescriptionItem(String medicineId, String medicineName, int quantity, String dosage) {
        this.medicineId = medicineId;
        this.medicineName = medicineName;
        this.quantity = quantity; // Autoboxing
        this.dosage = dosage;
    }

    public String getMedicineId() { return medicineId; }
    public void setMedicineId(String medicineId) { this.medicineId = medicineId; }

    public String getMedicineName() { return medicineName; }
    public void setMedicineName(String medicineName) { this.medicineName = medicineName; }

    public Integer getQuantity() { return quantity; }
    public void setQuantity(Integer quantity) { this.quantity = quantity; }

    public String getDosage() { return dosage; }
    public void setDosage(String dosage) { this.dosage = dosage; }

    @Override
    public String toString() {
        return medicineName + " x" + quantity + " (" + dosage + ")";
    }
}
