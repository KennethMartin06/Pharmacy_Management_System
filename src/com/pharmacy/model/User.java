package com.pharmacy.model;

import java.io.Serializable;

/**
 * User model for login and role-based access.
 * Demonstrates: Encapsulation, Enum usage, Serialization.
 */
public class User implements Serializable {
    private static final long serialVersionUID = 1L;

    private String username;
    private String password;
    private String fullName;
    private UserRole role;

    // Default constructor
    public User() {
    }

    // Parameterized constructor
    public User(String username, String password, String fullName, UserRole role) {
        this.username = username;
        this.password = password;
        this.fullName = fullName;
        this.role = role;
    }

    // Validate login credentials
    public boolean authenticate(String inputPassword) {
        return this.password.equals(inputPassword);
    }

    // Getters and Setters
    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }

    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }

    public String getFullName() { return fullName; }
    public void setFullName(String fullName) { this.fullName = fullName; }

    public UserRole getRole() { return role; }
    public void setRole(UserRole role) { this.role = role; }

    @Override
    public String toString() {
        return username + " (" + role.getDisplayName() + ")";
    }
}
