package com.pharmacy.model;

import java.io.Serializable;

/**
 * Individual item in a bill.
 * Demonstrates: Encapsulation, Serialization, Wrapper classes.
 */
public class BillItem implements Serializable {
    private static final long serialVersionUID = 1L;

    private String medicineId;
    private String medicineName;
    private Integer quantity; // Wrapper class
    private Double unitPrice; // Wrapper class
    private Double subtotal; // Wrapper class

    public BillItem() {
    }

    public BillItem(String medicineId, String medicineName, int quantity, double unitPrice) {
        this.medicineId = medicineId;
        this.medicineName = medicineName;
        this.quantity = quantity; // Autoboxing
        this.unitPrice = unitPrice; // Autoboxing
        this.subtotal = quantity * unitPrice; // Autoboxing result
    }

    // Getters and Setters
    public String getMedicineId() { return medicineId; }
    public void setMedicineId(String medicineId) { this.medicineId = medicineId; }

    public String getMedicineName() { return medicineName; }
    public void setMedicineName(String medicineName) { this.medicineName = medicineName; }

    public Integer getQuantity() { return quantity; }
    public void setQuantity(Integer quantity) { this.quantity = quantity; }

    public Double getUnitPrice() { return unitPrice; }
    public void setUnitPrice(Double unitPrice) { this.unitPrice = unitPrice; }

    public Double getSubtotal() { return subtotal; }
    public void setSubtotal(Double subtotal) { this.subtotal = subtotal; }

    @Override
    public String toString() {
        return medicineName + " x" + quantity + " @ Rs." + String.format("%.2f", unitPrice)
               + " = Rs." + String.format("%.2f", subtotal);
    }
}
