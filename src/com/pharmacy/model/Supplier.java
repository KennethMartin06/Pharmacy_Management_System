package com.pharmacy.model;

import java.io.Serializable;

/**
 * Supplier model class.
 * Demonstrates: Encapsulation, Serialization.
 */
public class Supplier implements Serializable {
    private static final long serialVersionUID = 1L;

    private String supplierId;
    private String companyName;
    private String contactPerson;
    private String phone;
    private String email;
    private String address;

    // Default constructor
    public Supplier() {
    }

    // Parameterized constructor
    public Supplier(String supplierId, String companyName, String contactPerson,
                    String phone, String email, String address) {
        this.supplierId = supplierId;
        this.companyName = companyName;
        this.contactPerson = contactPerson;
        this.phone = phone;
        this.email = email;
        this.address = address;
    }

    // Getters and Setters
    public String getSupplierId() { return supplierId; }
    public void setSupplierId(String supplierId) { this.supplierId = supplierId; }

    public String getCompanyName() { return companyName; }
    public void setCompanyName(String companyName) { this.companyName = companyName; }

    public String getContactPerson() { return contactPerson; }
    public void setContactPerson(String contactPerson) { this.contactPerson = contactPerson; }

    public String getPhone() { return phone; }
    public void setPhone(String phone) { this.phone = phone; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public String getAddress() { return address; }
    public void setAddress(String address) { this.address = address; }

    @Override
    public String toString() {
        return supplierId + " | " + companyName + " | " + contactPerson;
    }
}
