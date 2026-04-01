package com.pharmacy.ui;

import com.pharmacy.model.User;

import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;

/**
 * Dashboard screen - main navigation hub after login.
 * Demonstrates: JavaFX (VBox, HBox, Button, Label, GridPane), Event handling.
 */
public class DashboardScreen {

    private Scene scene;
    private PharmacyApp app;
    private User currentUser;

    public DashboardScreen(PharmacyApp app, User currentUser) {
        this.app = app;
        this.currentUser = currentUser;
        createScene();
    }

    private void createScene() {
        BorderPane root = new BorderPane();
        root.setStyle("-fx-background-color: #ecf0f1;");

        // Top bar
        HBox topBar = new HBox(20);
        topBar.setPadding(new Insets(15, 25, 15, 25));
        topBar.setAlignment(Pos.CENTER_LEFT);
        topBar.setStyle("-fx-background-color: #2c3e50;");

        Label titleLabel = new Label("PharmaCare Dashboard");
        titleLabel.setFont(Font.font("Arial", FontWeight.BOLD, 22));
        titleLabel.setStyle("-fx-text-fill: white;");

        Region spacer = new Region();
        HBox.setHgrow(spacer, Priority.ALWAYS);

        Label userLabel = new Label("Welcome, " + currentUser.getFullName()
                                    + " (" + currentUser.getRole().getDisplayName() + ")");
        userLabel.setStyle("-fx-text-fill: #bdc3c7; -fx-font-size: 13;");

        Button logoutBtn = new Button("Logout");
        logoutBtn.setStyle("-fx-background-color: #e74c3c; -fx-text-fill: white; -fx-cursor: hand;");
        logoutBtn.setOnAction(e -> {
            app.getUserService().logout();
            app.showLoginScreen();
        });

        topBar.getChildren().addAll(titleLabel, spacer, userLabel, logoutBtn);
        root.setTop(topBar);

        // Center - Module buttons in a grid
        GridPane moduleGrid = new GridPane();
        moduleGrid.setAlignment(Pos.CENTER);
        moduleGrid.setHgap(25);
        moduleGrid.setVgap(25);
        moduleGrid.setPadding(new Insets(40));

        // Module buttons
        Button inventoryBtn = createModuleButton("Inventory\nManagement",
                "Manage medicines, stock,\nbatch & expiry tracking", "#3498db");
        inventoryBtn.setOnAction(e -> app.showInventoryScreen());

        Button billingBtn = createModuleButton("Sales &\nBilling",
                "Create bills, generate\ninvoices for customers", "#27ae60");
        billingBtn.setOnAction(e -> app.showBillingScreen());

        Button supplierBtn = createModuleButton("Supplier\nManagement",
                "Manage supplier records\nand contact details", "#e67e22");
        supplierBtn.setOnAction(e -> app.showSupplierScreen());

        Button customerBtn = createModuleButton("Customer\nRecords",
                "Manage patient/customer\ninformation", "#9b59b6");
        customerBtn.setOnAction(e -> app.showCustomerScreen());

        Button prescriptionBtn = createModuleButton("Prescription\nHandling",
                "Record and manage\nprescription details", "#1abc9c");
        prescriptionBtn.setOnAction(e -> app.showPrescriptionScreen());

        Button reportsBtn = createModuleButton("Reports &\nAlerts",
                "View sales reports, stock\n& expiry alerts", "#e74c3c");
        reportsBtn.setOnAction(e -> app.showReportsScreen());

        // Arrange in 3x2 grid
        moduleGrid.add(inventoryBtn, 0, 0);
        moduleGrid.add(billingBtn, 1, 0);
        moduleGrid.add(supplierBtn, 2, 0);
        moduleGrid.add(customerBtn, 0, 1);
        moduleGrid.add(prescriptionBtn, 1, 1);
        moduleGrid.add(reportsBtn, 2, 1);

        root.setCenter(moduleGrid);

        // Bottom status bar
        HBox statusBar = new HBox(20);
        statusBar.setPadding(new Insets(10, 25, 10, 25));
        statusBar.setStyle("-fx-background-color: #34495e;");

        Label statusLabel = new Label("Medicines: " + app.getInventoryManager().getMedicineCount()
                + " | Customers: " + app.getCustomerService().getCustomerCount()
                + " | Suppliers: " + app.getSupplierService().getSupplierCount()
                + " | Bills: " + app.getBillingService().getBillCount());
        statusLabel.setStyle("-fx-text-fill: #bdc3c7; -fx-font-size: 12;");

        statusBar.getChildren().add(statusLabel);
        root.setBottom(statusBar);

        scene = new Scene(root, 1100, 700);
    }

    // Helper to create styled module buttons
    private Button createModuleButton(String title, String description, String color) {
        VBox content = new VBox(8);
        content.setAlignment(Pos.CENTER);

        Label titleLbl = new Label(title);
        titleLbl.setFont(Font.font("Arial", FontWeight.BOLD, 16));
        titleLbl.setStyle("-fx-text-fill: white; -fx-text-alignment: center;");

        Label descLbl = new Label(description);
        descLbl.setStyle("-fx-text-fill: #ecf0f1; -fx-font-size: 11; -fx-text-alignment: center;");

        content.getChildren().addAll(titleLbl, descLbl);

        Button btn = new Button();
        btn.setGraphic(content);
        btn.setPrefSize(230, 130);
        btn.setStyle("-fx-background-color: " + color + "; -fx-background-radius: 10; -fx-cursor: hand;");
        return btn;
    }

    public Scene getScene() {
        return scene;
    }
}
