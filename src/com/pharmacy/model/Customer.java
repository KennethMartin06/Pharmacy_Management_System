package com.pharmacy.model;

import java.io.Serializable;

/**
 * Customer/Patient model class.
 * Demonstrates: Encapsulation, Serialization.
 */
public class Customer implements Serializable {
    private static final long serialVersionUID = 1L;

    private String customerId;
    private String name;
    private String phone;
    private String email;
    private String address;

    // Default constructor
    public Customer() {
    }

    // Parameterized constructor
    public Customer(String customerId, String name, String phone, String email, String address) {
        this.customerId = customerId;
        this.name = name;
        this.phone = phone;
        this.email = email;
        this.address = address;
    }

    // Getters and Setters
    public String getCustomerId() { return customerId; }
    public void setCustomerId(String customerId) { this.customerId = customerId; }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getPhone() { return phone; }
    public void setPhone(String phone) { this.phone = phone; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }

    public String getAddress() { return address; }
    public void setAddress(String address) { this.address = address; }

    @Override
    public String toString() {
        return customerId + " | " + name + " | " + phone;
    }
}
