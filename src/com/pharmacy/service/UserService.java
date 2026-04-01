package com.pharmacy.service;

import com.pharmacy.model.User;
import com.pharmacy.model.UserRole;
import com.pharmacy.util.DataStore;

import java.util.ArrayList;

/**
 * Manages user authentication and accounts.
 * Demonstrates: ArrayList, Serialization, role-based access.
 */
public class UserService {

    private ArrayList<User> userList;
    private DataStore<User> dataStore;
    private User currentUser;

    private static final String DATA_FILE = "data/users.dat";

    public UserService() {
        this.dataStore = new DataStore<>(DATA_FILE);
        this.userList = dataStore.loadAll();

        // Create default admin if no users exist
        if (userList.isEmpty()) {
            createDefaultUsers();
        }
    }

    // Create default users for first run
    private void createDefaultUsers() {
        userList.add(new User("admin", "admin123", "System Administrator", UserRole.ADMIN));
        userList.add(new User("pharmacist", "pharma123", "Default Pharmacist", UserRole.PHARMACIST));
        dataStore.saveAll(userList);
    }

    // Authenticate user
    public User authenticate(String username, String password) {
        for (User user : userList) {
            if (user.getUsername().equals(username) && user.authenticate(password)) {
                this.currentUser = user;
                return user;
            }
        }
        return null;
    }

    public User getCurrentUser() {
        return currentUser;
    }

    public void setCurrentUser(User user) {
        this.currentUser = user;
    }

    public void addUser(User user) {
        userList.add(user);
        dataStore.saveAll(userList);
    }

    public ArrayList<User> getAllUsers() {
        return userList;
    }

    public void logout() {
        this.currentUser = null;
    }
}
