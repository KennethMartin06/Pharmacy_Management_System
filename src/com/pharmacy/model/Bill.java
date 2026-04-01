package com.pharmacy.model;

import java.io.Serializable;
import java.util.ArrayList;

/**
 * Bill/Invoice model class for sales transactions.
 * Demonstrates: Encapsulation, Serialization, ArrayList, Wrapper classes.
 */
public class Bill implements Serializable {
    private static final long serialVersionUID = 1L;

    private String billId;
    private String customerId;
    private String customerName;
    private String date;
    private ArrayList<BillItem> items;
    private Double totalAmount; // Wrapper class
    private Double discount;
    private Double netAmount;
    private String billedBy; // username of the person who billed

    // Default constructor
    public Bill() {
        this.items = new ArrayList<>();
        this.totalAmount = 0.0;
        this.discount = 0.0;
        this.netAmount = 0.0;
    }

    // Parameterized constructor
    public Bill(String billId, String customerId, String customerName,
                String date, String billedBy) {
        this.billId = billId;
        this.customerId = customerId;
        this.customerName = customerName;
        this.date = date;
        this.billedBy = billedBy;
        this.items = new ArrayList<>();
        this.totalAmount = 0.0;
        this.discount = 0.0;
        this.netAmount = 0.0;
    }

    // Add item and recalculate total
    public void addItem(BillItem item) {
        items.add(item);
        recalculate();
    }

    // Recalculate totals
    public void recalculate() {
        double total = 0.0;
        for (BillItem item : items) {
            total += item.getSubtotal(); // Unboxing
        }
        this.totalAmount = total; // Autoboxing
        this.netAmount = totalAmount - discount;
    }

    // Method overloading: apply discount by percentage
    public void applyDiscount(double percentage) {
        this.discount = totalAmount * (percentage / 100.0);
        this.netAmount = totalAmount - discount;
    }

    // Method overloading: apply discount by fixed amount with a flag
    public void applyDiscount(double amount, boolean isFixed) {
        if (isFixed) {
            this.discount = amount;
        } else {
            this.discount = totalAmount * (amount / 100.0);
        }
        this.netAmount = totalAmount - discount;
    }

    // Getters and Setters
    public String getBillId() { return billId; }
    public void setBillId(String billId) { this.billId = billId; }

    public String getCustomerId() { return customerId; }
    public void setCustomerId(String customerId) { this.customerId = customerId; }

    public String getCustomerName() { return customerName; }
    public void setCustomerName(String customerName) { this.customerName = customerName; }

    public String getDate() { return date; }
    public void setDate(String date) { this.date = date; }

    public ArrayList<BillItem> getItems() { return items; }
    public void setItems(ArrayList<BillItem> items) { this.items = items; }

    public Double getTotalAmount() { return totalAmount; }
    public void setTotalAmount(Double totalAmount) { this.totalAmount = totalAmount; }

    public Double getDiscount() { return discount; }
    public void setDiscount(Double discount) { this.discount = discount; }

    public Double getNetAmount() { return netAmount; }
    public void setNetAmount(Double netAmount) { this.netAmount = netAmount; }

    public String getBilledBy() { return billedBy; }
    public void setBilledBy(String billedBy) { this.billedBy = billedBy; }

    @Override
    public String toString() {
        return billId + " | " + customerName + " | Rs." + String.format("%.2f", netAmount)
               + " | " + date;
    }
}
