package com.pharmacy.model;

import java.io.Serializable;

/**
 * Medicine model class representing a medicine in the pharmacy.
 * Demonstrates: Encapsulation, Serialization, Constructors, Wrapper classes.
 */
public class Medicine implements Serializable, Comparable<Medicine> {
    private static final long serialVersionUID = 1L;

    private String medicineId;
    private String name;
    private String manufacturer;
    private MedicineCategory category;
    private String batchNumber;
    private String expiryDate; // Format: YYYY-MM-DD
    private Integer quantity; // Wrapper class demonstration
    private Double price; // Wrapper class demonstration
    private String supplierId;

    // Default constructor
    public Medicine() {
    }

    // Parameterized constructor
    public Medicine(String medicineId, String name, String manufacturer,
                    MedicineCategory category, String batchNumber,
                    String expiryDate, int quantity, double price, String supplierId) {
        this.medicineId = medicineId;
        this.name = name;
        this.manufacturer = manufacturer;
        this.category = category;
        this.batchNumber = batchNumber;
        this.expiryDate = expiryDate;
        this.quantity = quantity; // Autoboxing: int -> Integer
        this.price = price; // Autoboxing: double -> Double
        this.supplierId = supplierId;
    }

    // Constructor overloading (without supplier)
    public Medicine(String medicineId, String name, String manufacturer,
                    MedicineCategory category, String batchNumber,
                    String expiryDate, int quantity, double price) {
        this(medicineId, name, manufacturer, category, batchNumber,
             expiryDate, quantity, price, "");
    }

    // Getters and Setters (Encapsulation)
    public String getMedicineId() { return medicineId; }
    public void setMedicineId(String medicineId) { this.medicineId = medicineId; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getManufacturer() { return manufacturer; }
    public void setManufacturer(String manufacturer) { this.manufacturer = manufacturer; }

    public MedicineCategory getCategory() { return category; }
    public void setCategory(MedicineCategory category) { this.category = category; }

    public String getBatchNumber() { return batchNumber; }
    public void setBatchNumber(String batchNumber) { this.batchNumber = batchNumber; }

    public String getExpiryDate() { return expiryDate; }
    public void setExpiryDate(String expiryDate) { this.expiryDate = expiryDate; }

    public Integer getQuantity() { return quantity; }
    public void setQuantity(Integer quantity) { this.quantity = quantity; }

    public Double getPrice() { return price; }
    public void setPrice(Double price) { this.price = price; }

    public String getSupplierId() { return supplierId; }
    public void setSupplierId(String supplierId) { this.supplierId = supplierId; }

    // Unboxing demonstration
    public int getQuantityPrimitive() {
        return quantity; // Unboxing: Integer -> int
    }

    public double getPricePrimitive() {
        return price; // Unboxing: Double -> double
    }

    // Comparable implementation for sorting
    @Override
    public int compareTo(Medicine other) {
        return this.name.compareToIgnoreCase(other.name);
    }

    @Override
    public String toString() {
        return medicineId + " | " + name + " | " + category + " | Qty: " + quantity
               + " | Rs." + String.format("%.2f", price) + " | Exp: " + expiryDate;
    }
}
