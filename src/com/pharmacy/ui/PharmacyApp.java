package com.pharmacy.ui;

import com.pharmacy.model.User;
import com.pharmacy.service.*;
import com.pharmacy.util.SampleDataLoader;

import javafx.application.Application;
import javafx.application.Platform;
import javafx.stage.Stage;

import java.io.File;

/**
 * Main JavaFX Application class - Entry point for the Pharmacy Management System.
 * Demonstrates: JavaFX Application, Stage management, Inheritance (extends Application).
 */
public class PharmacyApp extends Application {

    // Service instances (shared across all screens)
    private UserService userService;
    private InventoryManager inventoryManager;
    private CustomerService customerService;
    private SupplierService supplierService;
    private BillingService billingService;
    private PrescriptionService prescriptionService;

    // Alert threads
    private ExpiryAlertThread expiryAlertThread;
    private Thread stockAlertThreadHandle;
    private StockAlertThread stockAlertRunnable;

    private Stage primaryStage;

    @Override
    public void start(Stage primaryStage) {
        this.primaryStage = primaryStage;

        // Create data directory
        new File("data/invoices").mkdirs();

        // Initialize all services
        userService = new UserService();
        inventoryManager = new InventoryManager();
        customerService = new CustomerService();
        supplierService = new SupplierService();
        billingService = new BillingService(inventoryManager);
        prescriptionService = new PrescriptionService();

        // Load sample data if empty
        SampleDataLoader.loadSampleData(inventoryManager, customerService, supplierService);

        // Start background alert threads (Multithreading demonstration)
        startAlertThreads();

        // Show login screen
        showLoginScreen();

        primaryStage.setTitle("PharmaCare - Pharmacy Management System");
        primaryStage.setWidth(1100);
        primaryStage.setHeight(700);
        primaryStage.setOnCloseRequest(e -> {
            stopAlertThreads();
            Platform.exit();
            System.exit(0);
        });
        primaryStage.show();
    }

    /**
     * Start background threads for monitoring.
     * Demonstrates: Thread creation (both Thread subclass and Runnable), start(), daemon threads.
     */
    private void startAlertThreads() {
        // Thread extending Thread class
        expiryAlertThread = new ExpiryAlertThread(inventoryManager);
        expiryAlertThread.start();

        // Thread using Runnable interface
        stockAlertRunnable = new StockAlertThread(inventoryManager);
        stockAlertThreadHandle = new Thread(stockAlertRunnable, "StockAlertThread");
        stockAlertThreadHandle.setDaemon(true);
        stockAlertThreadHandle.start();
    }

    private void stopAlertThreads() {
        if (expiryAlertThread != null) {
            expiryAlertThread.stopChecking();
        }
        if (stockAlertRunnable != null) {
            stockAlertRunnable.stopChecking();
        }
    }

    // Show login screen
    public void showLoginScreen() {
        LoginScreen loginScreen = new LoginScreen(this, userService);
        primaryStage.setScene(loginScreen.getScene());
    }

    // Show dashboard after login
    public void showDashboard(User user) {
        DashboardScreen dashboard = new DashboardScreen(this, user);
        primaryStage.setScene(dashboard.getScene());
    }

    // Show inventory module
    public void showInventoryScreen() {
        InventoryScreen screen = new InventoryScreen(this, inventoryManager, supplierService);
        primaryStage.setScene(screen.getScene());
    }

    // Show billing module
    public void showBillingScreen() {
        BillingScreen screen = new BillingScreen(this, billingService, inventoryManager,
                                                  customerService, userService);
        primaryStage.setScene(screen.getScene());
    }

    // Show supplier module
    public void showSupplierScreen() {
        SupplierScreen screen = new SupplierScreen(this, supplierService);
        primaryStage.setScene(screen.getScene());
    }

    // Show customer module
    public void showCustomerScreen() {
        CustomerScreen screen = new CustomerScreen(this, customerService);
        primaryStage.setScene(screen.getScene());
    }

    // Show prescription module
    public void showPrescriptionScreen() {
        PrescriptionScreen screen = new PrescriptionScreen(this, prescriptionService,
                                                            customerService, inventoryManager);
        primaryStage.setScene(screen.getScene());
    }

    // Show reports module
    public void showReportsScreen() {
        ReportsScreen screen = new ReportsScreen(this, inventoryManager, billingService,
                                                  customerService, supplierService,
                                                  expiryAlertThread, stockAlertRunnable);
        primaryStage.setScene(screen.getScene());
    }

    // Getters for services
    public UserService getUserService() { return userService; }
    public InventoryManager getInventoryManager() { return inventoryManager; }
    public CustomerService getCustomerService() { return customerService; }
    public SupplierService getSupplierService() { return supplierService; }
    public BillingService getBillingService() { return billingService; }
    public PrescriptionService getPrescriptionService() { return prescriptionService; }
    public ExpiryAlertThread getExpiryAlertThread() { return expiryAlertThread; }
    public StockAlertThread getStockAlertRunnable() { return stockAlertRunnable; }
    public Stage getPrimaryStage() { return primaryStage; }

    /**
     * Main method - entry point.
     */
    public static void main(String[] args) {
        launch(args);
    }
}
