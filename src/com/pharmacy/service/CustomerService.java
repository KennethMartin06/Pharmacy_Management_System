package com.pharmacy.service;

import com.pharmacy.model.Customer;
import com.pharmacy.util.DataStore;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.Iterator;

/**
 * Manages customer/patient records.
 * Demonstrates: ArrayList, HashMap, Iterator, Generics.
 */
public class CustomerService {

    private ArrayList<Customer> customerList;
    private HashMap<String, Customer> customerMap;
    private DataStore<Customer> dataStore;

    private static final String DATA_FILE = "data/customers.dat";
    private static final String BACKUP_FILE = "data/backup_customers.txt";

    public CustomerService() {
        this.dataStore = new DataStore<>(DATA_FILE);
        this.customerList = dataStore.loadAll();
        this.customerMap = new HashMap<>();

        for (Customer cust : customerList) {
            customerMap.put(cust.getCustomerId(), cust);
        }
    }

    public synchronized void addCustomer(Customer customer) {
        customerList.add(customer);
        customerMap.put(customer.getCustomerId(), customer);
        saveData();
    }

    public synchronized void updateCustomer(Customer customer) {
        customerMap.put(customer.getCustomerId(), customer);
        for (int i = 0; i < customerList.size(); i++) {
            if (customerList.get(i).getCustomerId().equals(customer.getCustomerId())) {
                customerList.set(i, customer);
                break;
            }
        }
        saveData();
    }

    public synchronized void deleteCustomer(String customerId) {
        Iterator<Customer> iterator = customerList.iterator();
        while (iterator.hasNext()) {
            Customer cust = iterator.next();
            if (cust.getCustomerId().equals(customerId)) {
                iterator.remove();
                break;
            }
        }
        customerMap.remove(customerId);
        saveData();
    }

    public Customer getCustomerById(String customerId) {
        return customerMap.get(customerId);
    }

    public ArrayList<Customer> searchByName(String name) {
        ArrayList<Customer> results = new ArrayList<>();
        for (Customer cust : customerList) {
            if (cust.getName().toLowerCase().contains(name.toLowerCase())) {
                results.add(cust);
            }
        }
        return results;
    }

    public ArrayList<Customer> getAllCustomers() {
        return customerList;
    }

    private void saveData() {
        dataStore.saveAll(customerList);
    }

    public void createBackup() {
        dataStore.backupToText(customerList, BACKUP_FILE);
    }

    public int getCustomerCount() {
        return customerList.size();
    }
}
