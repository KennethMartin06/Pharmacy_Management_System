package com.pharmacy.model;

/**
 * Enum for role-based access control.
 * Demonstrates: Enum with methods.
 */
public enum UserRole {
    ADMIN("Administrator", true),
    PHARMACIST("Pharmacist", false);

    private final String displayName;
    private final boolean canManageUsers;

    UserRole(String displayName, boolean canManageUsers) {
        this.displayName = displayName;
        this.canManageUsers = canManageUsers;
    }

    public String getDisplayName() {
        return displayName;
    }

    public boolean canManageUsers() {
        return canManageUsers;
    }
}
