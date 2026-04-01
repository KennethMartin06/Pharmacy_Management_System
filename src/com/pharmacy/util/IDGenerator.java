package com.pharmacy.util;

/**
 * Utility class for generating unique IDs.
 * Demonstrates: Static methods, synchronized for thread safety.
 */
public class IDGenerator {
    private static int medicineCounter = 1000;
    private static int customerCounter = 2000;
    private static int supplierCounter = 3000;
    private static int billCounter = 4000;
    private static int prescriptionCounter = 5000;

    // Synchronized to ensure thread-safe ID generation
    public static synchronized String generateMedicineId() {
        return "MED" + (++medicineCounter);
    }

    public static synchronized String generateCustomerId() {
        return "CUS" + (++customerCounter);
    }

    public static synchronized String generateSupplierId() {
        return "SUP" + (++supplierCounter);
    }

    public static synchronized String generateBillId() {
        return "BIL" + (++billCounter);
    }

    public static synchronized String generatePrescriptionId() {
        return "PRE" + (++prescriptionCounter);
    }

    // Update counters based on existing data
    public static void updateCounters(int medCount, int cusCount, int supCount,
                                       int bilCount, int preCount) {
        if (medCount > medicineCounter) medicineCounter = medCount;
        if (cusCount > customerCounter) customerCounter = cusCount;
        if (supCount > supplierCounter) supplierCounter = supCount;
        if (bilCount > billCounter) billCounter = bilCount;
        if (preCount > prescriptionCounter) prescriptionCounter = preCount;
    }
}
