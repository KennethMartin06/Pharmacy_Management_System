package com.pharmacy.util;

import java.io.*;
import java.util.ArrayList;

/**
 * Generic data store for serialization and deserialization.
 * Demonstrates: Generics, Serialization/Deserialization, File I/O.
 *
 * @param <T> The type of objects to store (must be Serializable)
 */
public class DataStore<T extends Serializable> {

    private String filePath;

    public DataStore(String filePath) {
        this.filePath = filePath;
    }

    /**
     * Save a list of objects using Serialization (ObjectOutputStream).
     * Demonstrates: FileOutputStream, ObjectOutputStream, Serialization.
     */
    public synchronized void saveAll(ArrayList<T> items) {
        try (FileOutputStream fos = new FileOutputStream(filePath);
             ObjectOutputStream oos = new ObjectOutputStream(fos)) {
            oos.writeObject(items);
        } catch (IOException e) {
            System.err.println("Error saving data to " + filePath + ": " + e.getMessage());
        }
    }

    /**
     * Load a list of objects using Deserialization (ObjectInputStream).
     * Demonstrates: FileInputStream, ObjectInputStream, Deserialization.
     */
    @SuppressWarnings("unchecked")
    public synchronized ArrayList<T> loadAll() {
        File file = new File(filePath);
        if (!file.exists()) {
            return new ArrayList<>();
        }
        try (FileInputStream fis = new FileInputStream(filePath);
             ObjectInputStream ois = new ObjectInputStream(fis)) {
            return (ArrayList<T>) ois.readObject();
        } catch (IOException | ClassNotFoundException e) {
            System.err.println("Error loading data from " + filePath + ": " + e.getMessage());
            return new ArrayList<>();
        }
    }

    /**
     * Backup data to a text file using FileWriter.
     * Demonstrates: FileWriter usage.
     */
    public void backupToText(ArrayList<T> items, String backupPath) {
        try (FileWriter writer = new FileWriter(backupPath)) {
            writer.write("=== DATA BACKUP ===\n");
            writer.write("Source: " + filePath + "\n");
            writer.write("Records: " + items.size() + "\n");
            writer.write("====================\n\n");
            for (T item : items) {
                writer.write(item.toString() + "\n");
            }
            writer.write("\n=== END OF BACKUP ===\n");
        } catch (IOException e) {
            System.err.println("Error creating backup: " + e.getMessage());
        }
    }

    /**
     * Read backup file content using FileReader.
     * Demonstrates: FileReader usage.
     */
    public String readBackup(String backupPath) {
        StringBuilder content = new StringBuilder();
        File file = new File(backupPath);
        if (!file.exists()) {
            return "No backup found.";
        }
        try (FileReader reader = new FileReader(backupPath)) {
            int ch;
            while ((ch = reader.read()) != -1) {
                content.append((char) ch);
            }
        } catch (IOException e) {
            System.err.println("Error reading backup: " + e.getMessage());
        }
        return content.toString();
    }

    public String getFilePath() {
        return filePath;
    }
}
