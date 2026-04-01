package com.pharmacy.model;

/**
 * Enum representing different categories of medicines.
 * Demonstrates: Enum usage as required by OSDL syllabus.
 */
public enum MedicineCategory {
    TABLET("Tablet"),
    CAPSULE("Capsule"),
    SYRUP("Syrup"),
    INJECTION("Injection"),
    OINTMENT("Ointment"),
    DROPS("Drops"),
    INHALER("Inhaler"),
    POWDER("Powder");

    private final String displayName;

    // Enum constructor
    MedicineCategory(String displayName) {
        this.displayName = displayName;
    }

    public String getDisplayName() {
        return displayName;
    }

    @Override
    public String toString() {
        return displayName;
    }
}
