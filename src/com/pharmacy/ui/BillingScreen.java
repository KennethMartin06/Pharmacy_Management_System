package com.pharmacy.ui;

import com.pharmacy.model.*;
import com.pharmacy.service.*;
import com.pharmacy.util.IDGenerator;

import javafx.application.Platform;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.layout.*;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;

import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * Sales and Billing Screen with multi-threaded billing simulation.
 * Demonstrates: JavaFX TableView, GridPane, VBox/HBox, Multithreaded billing.
 */
public class BillingScreen {

    private Scene scene;
    private PharmacyApp app;
    private BillingService billingService;
    private InventoryManager inventoryManager;
    private CustomerService customerService;
    private UserService userService;

    private TableView<BillItem> billItemsTable;
    private ObservableList<BillItem> billItems;
    private Label totalLabel;
    private Label netLabel;
    private Bill currentBill;

    public BillingScreen(PharmacyApp app, BillingService billingService,
                         InventoryManager inventoryManager, CustomerService customerService,
                         UserService userService) {
        this.app = app;
        this.billingService = billingService;
        this.inventoryManager = inventoryManager;
        this.customerService = customerService;
        this.userService = userService;
        this.billItems = FXCollections.observableArrayList();
        createScene();
    }

    @SuppressWarnings("unchecked")
    private void createScene() {
        BorderPane root = new BorderPane();
        root.setStyle("-fx-background-color: #ecf0f1;");

        // Top bar
        HBox topBar = new HBox(15);
        topBar.setPadding(new Insets(12, 20, 12, 20));
        topBar.setAlignment(Pos.CENTER_LEFT);
        topBar.setStyle("-fx-background-color: #2c3e50;");

        Button backBtn = new Button("< Back");
        backBtn.setStyle("-fx-background-color: #7f8c8d; -fx-text-fill: white; -fx-cursor: hand;");
        backBtn.setOnAction(e -> app.showDashboard(userService.getCurrentUser()));

        Label titleLabel = new Label("Sales & Billing");
        titleLabel.setFont(Font.font("Arial", FontWeight.BOLD, 20));
        titleLabel.setStyle("-fx-text-fill: white;");

        topBar.getChildren().addAll(backBtn, titleLabel);
        root.setTop(topBar);

        // Left - Bill form
        VBox formBox = new VBox(12);
        formBox.setPadding(new Insets(15));
        formBox.setPrefWidth(320);
        formBox.setStyle("-fx-background-color: white; -fx-border-color: #bdc3c7; -fx-border-width: 0 1 0 0;");

        Label formTitle = new Label("New Bill");
        formTitle.setFont(Font.font("Arial", FontWeight.BOLD, 15));

        GridPane custGrid = new GridPane();
        custGrid.setVgap(8);
        custGrid.setHgap(8);

        TextField custIdField = new TextField();
        custIdField.setPromptText("Customer ID");
        TextField custNameField = new TextField();
        custNameField.setPromptText("Customer Name");

        // Auto-fill customer name when ID is entered
        custIdField.textProperty().addListener((obs, oldVal, newVal) -> {
            if (newVal != null && !newVal.isEmpty()) {
                Customer cust = customerService.getCustomerById(newVal.trim());
                if (cust != null) {
                    custNameField.setText(cust.getName());
                }
            }
        });

        custGrid.add(new Label("Customer ID:"), 0, 0);
        custGrid.add(custIdField, 1, 0);
        custGrid.add(new Label("Customer Name:"), 0, 1);
        custGrid.add(custNameField, 1, 1);

        // Add medicine to bill
        Label addItemTitle = new Label("Add Medicine to Bill");
        addItemTitle.setFont(Font.font("Arial", FontWeight.BOLD, 13));

        GridPane itemGrid = new GridPane();
        itemGrid.setVgap(8);
        itemGrid.setHgap(8);

        TextField medIdField = new TextField();
        medIdField.setPromptText("Medicine ID");
        Label medNameLabel = new Label("-");
        Label medPriceLabel = new Label("-");
        Label medStockLabel = new Label("-");
        TextField medQtyField = new TextField();
        medQtyField.setPromptText("Quantity");

        // Auto-fill medicine details
        medIdField.textProperty().addListener((obs, oldVal, newVal) -> {
            if (newVal != null && !newVal.isEmpty()) {
                Medicine med = inventoryManager.getMedicineById(newVal.trim());
                if (med != null) {
                    medNameLabel.setText(med.getName());
                    medPriceLabel.setText("Rs." + String.format("%.2f", med.getPrice()));
                    medStockLabel.setText("Stock: " + med.getQuantity());
                }
            }
        });

        int r = 0;
        itemGrid.add(new Label("Medicine ID:"), 0, r); itemGrid.add(medIdField, 1, r++);
        itemGrid.add(new Label("Name:"), 0, r); itemGrid.add(medNameLabel, 1, r++);
        itemGrid.add(new Label("Price:"), 0, r); itemGrid.add(medPriceLabel, 1, r++);
        itemGrid.add(new Label("Available:"), 0, r); itemGrid.add(medStockLabel, 1, r++);
        itemGrid.add(new Label("Quantity:"), 0, r); itemGrid.add(medQtyField, 1, r++);

        Label statusLabel = new Label();

        Button addItemBtn = new Button("Add to Bill");
        addItemBtn.setStyle("-fx-background-color: #3498db; -fx-text-fill: white; -fx-cursor: hand; -fx-pref-width: 200;");
        addItemBtn.setOnAction(e -> {
            try {
                String medId = medIdField.getText().trim();
                Medicine med = inventoryManager.getMedicineById(medId);
                if (med == null) {
                    statusLabel.setText("Medicine not found!");
                    statusLabel.setStyle("-fx-text-fill: #e74c3c;");
                    return;
                }
                int qty = Integer.parseInt(medQtyField.getText().trim());
                if (qty > med.getQuantity()) {
                    statusLabel.setText("Insufficient stock!");
                    statusLabel.setStyle("-fx-text-fill: #e74c3c;");
                    return;
                }

                BillItem item = new BillItem(medId, med.getName(), qty, med.getPrice());
                billItems.add(item);
                updateTotals();
                medIdField.clear();
                medQtyField.clear();
                medNameLabel.setText("-");
                medPriceLabel.setText("-");
                medStockLabel.setText("-");
                statusLabel.setText("Item added!");
                statusLabel.setStyle("-fx-text-fill: #27ae60;");
            } catch (NumberFormatException ex) {
                statusLabel.setText("Invalid quantity!");
                statusLabel.setStyle("-fx-text-fill: #e74c3c;");
            }
        });

        // Totals
        totalLabel = new Label("Total: Rs.0.00");
        totalLabel.setFont(Font.font("Arial", FontWeight.BOLD, 14));

        TextField discountField = new TextField("0");
        discountField.setPromptText("Discount %");
        discountField.setPrefWidth(80);

        netLabel = new Label("Net: Rs.0.00");
        netLabel.setFont(Font.font("Arial", FontWeight.BOLD, 16));
        netLabel.setStyle("-fx-text-fill: #27ae60;");

        HBox totalsBox = new HBox(10);
        totalsBox.setAlignment(Pos.CENTER_LEFT);
        totalsBox.getChildren().addAll(new Label("Discount %:"), discountField);

        // Generate Bill button - uses multithreaded billing
        Button generateBtn = new Button("Generate Bill (Threaded)");
        generateBtn.setStyle("-fx-background-color: #27ae60; -fx-text-fill: white; " +
                            "-fx-font-size: 14; -fx-pref-width: 280; -fx-cursor: hand;");
        generateBtn.setOnAction(e -> {
            if (billItems.isEmpty()) {
                statusLabel.setText("Add items first!");
                statusLabel.setStyle("-fx-text-fill: #e74c3c;");
                return;
            }
            if (custNameField.getText().trim().isEmpty()) {
                statusLabel.setText("Enter customer name!");
                statusLabel.setStyle("-fx-text-fill: #e74c3c;");
                return;
            }

            String billId = IDGenerator.generateBillId();
            String date = new SimpleDateFormat("yyyy-MM-dd").format(new Date());
            currentBill = new Bill(billId, custIdField.getText().trim(),
                                    custNameField.getText().trim(), date,
                                    userService.getCurrentUser().getUsername());

            for (BillItem item : billItems) {
                currentBill.addItem(item);
            }

            try {
                double discPct = Double.parseDouble(discountField.getText().trim());
                currentBill.applyDiscount(discPct); // Method overloading demo
            } catch (NumberFormatException ex) {
                // No discount
            }

            // Multi-threaded billing using BillingThread
            statusLabel.setText("Processing bill...");
            statusLabel.setStyle("-fx-text-fill: #3498db;");
            generateBtn.setDisable(true);

            BillingThread billingThread = new BillingThread(billingService, currentBill,
                (success, message, bill) -> {
                    // Use Platform.runLater to update UI from thread
                    Platform.runLater(() -> {
                        if (success) {
                            statusLabel.setText(message + " Invoice generated!");
                            statusLabel.setStyle("-fx-text-fill: #27ae60;");
                            billItems.clear();
                            updateTotals();
                            custIdField.clear();
                            custNameField.clear();
                        } else {
                            statusLabel.setText(message);
                            statusLabel.setStyle("-fx-text-fill: #e74c3c;");
                        }
                        generateBtn.setDisable(false);
                    });
                });
            billingThread.start();

            // Demonstrate join() - wait for billing thread in another thread
            Thread waitThread = new Thread(() -> {
                try {
                    billingThread.join(); // Wait for billing to complete
                    System.out.println("Billing thread completed via join()");
                } catch (InterruptedException ex) {
                    Thread.currentThread().interrupt();
                }
            });
            waitThread.setDaemon(true);
            waitThread.start();
        });

        Button clearBillBtn = new Button("Clear Bill");
        clearBillBtn.setStyle("-fx-background-color: #e74c3c; -fx-text-fill: white; -fx-cursor: hand;");
        clearBillBtn.setOnAction(e -> {
            billItems.clear();
            updateTotals();
            statusLabel.setText("");
        });

        formBox.getChildren().addAll(formTitle, custGrid,
                new Separator(), addItemTitle, itemGrid, addItemBtn, statusLabel,
                new Separator(), totalLabel, totalsBox, netLabel,
                generateBtn, clearBillBtn);
        root.setLeft(formBox);

        // Center - Bill items table
        VBox tableBox = new VBox(10);
        tableBox.setPadding(new Insets(15));

        Label tableTitle = new Label("Current Bill Items");
        tableTitle.setFont(Font.font("Arial", FontWeight.BOLD, 15));

        billItemsTable = new TableView<>();
        billItemsTable.setItems(billItems);

        TableColumn<BillItem, String> nameCol = new TableColumn<>("Medicine");
        nameCol.setCellValueFactory(new PropertyValueFactory<>("medicineName"));
        nameCol.setPrefWidth(200);

        TableColumn<BillItem, Integer> qtyCol = new TableColumn<>("Qty");
        qtyCol.setCellValueFactory(new PropertyValueFactory<>("quantity"));
        qtyCol.setPrefWidth(60);

        TableColumn<BillItem, Double> priceCol = new TableColumn<>("Unit Price");
        priceCol.setCellValueFactory(new PropertyValueFactory<>("unitPrice"));
        priceCol.setPrefWidth(100);

        TableColumn<BillItem, Double> subCol = new TableColumn<>("Subtotal");
        subCol.setCellValueFactory(new PropertyValueFactory<>("subtotal"));
        subCol.setPrefWidth(100);

        billItemsTable.getColumns().addAll(nameCol, qtyCol, priceCol, subCol);

        // Past bills table
        Label pastTitle = new Label("Past Bills");
        pastTitle.setFont(Font.font("Arial", FontWeight.BOLD, 13));

        TableView<Bill> pastBillsTable = new TableView<>();
        ObservableList<Bill> pastBills = FXCollections.observableArrayList(billingService.getAllBills());
        pastBillsTable.setItems(pastBills);

        TableColumn<Bill, String> billIdCol = new TableColumn<>("Bill ID");
        billIdCol.setCellValueFactory(new PropertyValueFactory<>("billId"));

        TableColumn<Bill, String> billCustCol = new TableColumn<>("Customer");
        billCustCol.setCellValueFactory(new PropertyValueFactory<>("customerName"));

        TableColumn<Bill, String> billDateCol = new TableColumn<>("Date");
        billDateCol.setCellValueFactory(new PropertyValueFactory<>("date"));

        TableColumn<Bill, Double> billAmtCol = new TableColumn<>("Amount");
        billAmtCol.setCellValueFactory(new PropertyValueFactory<>("netAmount"));

        pastBillsTable.getColumns().addAll(billIdCol, billCustCol, billDateCol, billAmtCol);
        pastBillsTable.setPrefHeight(200);

        VBox.setVgrow(billItemsTable, Priority.ALWAYS);
        tableBox.getChildren().addAll(tableTitle, billItemsTable, pastTitle, pastBillsTable);
        root.setCenter(tableBox);

        scene = new Scene(root, 1100, 700);
    }

    private void updateTotals() {
        double total = 0;
        for (BillItem item : billItems) {
            total += item.getSubtotal();
        }
        totalLabel.setText(String.format("Total: Rs.%.2f", total));
        netLabel.setText(String.format("Net: Rs.%.2f", total));
    }

    public Scene getScene() {
        return scene;
    }
}
