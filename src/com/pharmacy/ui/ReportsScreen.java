package com.pharmacy.ui;

import com.pharmacy.model.Bill;
import com.pharmacy.model.Medicine;
import com.pharmacy.service.*;

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
import java.util.ArrayList;
import java.util.Calendar;
import java.util.Date;

/**
 * Reports & Alerts Screen - Sales reports, stock alerts, expiry alerts, backups.
 * Demonstrates: JavaFX TableView, VBox/HBox, Multithreading integration, Backup service.
 */
public class ReportsScreen {

    private Scene scene;
    private PharmacyApp app;
    private InventoryManager inventoryManager;
    private BillingService billingService;
    private CustomerService customerService;
    private SupplierService supplierService;
    private ExpiryAlertThread expiryAlertThread;
    private StockAlertThread stockAlertRunnable;

    public ReportsScreen(PharmacyApp app, InventoryManager inventoryManager,
                         BillingService billingService, CustomerService customerService,
                         SupplierService supplierService,
                         ExpiryAlertThread expiryAlertThread, StockAlertThread stockAlertRunnable) {
        this.app = app;
        this.inventoryManager = inventoryManager;
        this.billingService = billingService;
        this.customerService = customerService;
        this.supplierService = supplierService;
        this.expiryAlertThread = expiryAlertThread;
        this.stockAlertRunnable = stockAlertRunnable;
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
        backBtn.setOnAction(e -> app.showDashboard(app.getUserService().getCurrentUser()));

        Label titleLabel = new Label("Reports & Alerts");
        titleLabel.setFont(Font.font("Arial", FontWeight.BOLD, 20));
        titleLabel.setStyle("-fx-text-fill: white;");

        topBar.getChildren().addAll(backBtn, titleLabel);
        root.setTop(topBar);

        // Left - Report categories
        VBox leftMenu = new VBox(8);
        leftMenu.setPadding(new Insets(15));
        leftMenu.setPrefWidth(200);
        leftMenu.setStyle("-fx-background-color: white; -fx-border-color: #bdc3c7; -fx-border-width: 0 1 0 0;");

        Label menuTitle = new Label("Report Types");
        menuTitle.setFont(Font.font("Arial", FontWeight.BOLD, 14));

        // Content area in center
        VBox contentArea = new VBox(10);
        contentArea.setPadding(new Insets(15));

        Button salesReportBtn = createMenuButton("Sales Report", "#27ae60");
        Button stockReportBtn = createMenuButton("Stock Report", "#3498db");
        Button expiryAlertBtn = createMenuButton("Expiry Alerts", "#e74c3c");
        Button lowStockBtn = createMenuButton("Low Stock Alert", "#e67e22");
        Button summaryBtn = createMenuButton("Summary", "#9b59b6");
        Button backupBtn = createMenuButton("Backup Data", "#34495e");

        // Sales Report
        salesReportBtn.setOnAction(e -> showSalesReport(contentArea));

        // Stock Report
        stockReportBtn.setOnAction(e -> showStockReport(contentArea));

        // Expiry Alerts (from alert thread)
        expiryAlertBtn.setOnAction(e -> showExpiryAlerts(contentArea));

        // Low Stock Alert (from stock thread)
        lowStockBtn.setOnAction(e -> showLowStockAlerts(contentArea));

        // Summary
        summaryBtn.setOnAction(e -> showSummary(contentArea));

        // Backup
        backupBtn.setOnAction(e -> runBackup(contentArea));

        leftMenu.getChildren().addAll(menuTitle, new Separator(),
                salesReportBtn, stockReportBtn, expiryAlertBtn,
                lowStockBtn, summaryBtn, new Separator(), backupBtn);
        root.setLeft(leftMenu);

        // Initial content
        showSummary(contentArea);
        root.setCenter(contentArea);

        scene = new Scene(root, 1100, 700);
    }

    private void showSalesReport(VBox contentArea) {
        contentArea.getChildren().clear();

        Label title = new Label("Sales Report");
        title.setFont(Font.font("Arial", FontWeight.BOLD, 18));

        String today = new SimpleDateFormat("yyyy-MM-dd").format(new Date());
        Label totalSales = new Label(String.format("Total Sales (All Time): Rs.%.2f", billingService.getTotalSales()));
        totalSales.setFont(Font.font("Arial", FontWeight.BOLD, 14));
        totalSales.setStyle("-fx-text-fill: #27ae60;");

        Label todaySales = new Label(String.format("Today's Sales: Rs.%.2f", billingService.getTotalSalesByDate(today)));
        todaySales.setFont(Font.font("Arial", FontWeight.BOLD, 14));

        Label billCount = new Label("Total Bills: " + billingService.getBillCount());

        // Bills table
        TableView<Bill> billTable = new TableView<>();
        ObservableList<Bill> bills = FXCollections.observableArrayList(billingService.getAllBills());
        billTable.setItems(bills);

        TableColumn<Bill, String> idCol = new TableColumn<>("Bill ID");
        idCol.setCellValueFactory(new PropertyValueFactory<>("billId"));
        TableColumn<Bill, String> custCol = new TableColumn<>("Customer");
        custCol.setCellValueFactory(new PropertyValueFactory<>("customerName"));
        custCol.setPrefWidth(150);
        TableColumn<Bill, String> dateCol = new TableColumn<>("Date");
        dateCol.setCellValueFactory(new PropertyValueFactory<>("date"));
        TableColumn<Bill, Double> totalCol = new TableColumn<>("Total");
        totalCol.setCellValueFactory(new PropertyValueFactory<>("totalAmount"));
        TableColumn<Bill, Double> discCol = new TableColumn<>("Discount");
        discCol.setCellValueFactory(new PropertyValueFactory<>("discount"));
        TableColumn<Bill, Double> netCol = new TableColumn<>("Net Amount");
        netCol.setCellValueFactory(new PropertyValueFactory<>("netAmount"));
        netCol.setPrefWidth(100);
        TableColumn<Bill, String> byCol = new TableColumn<>("Billed By");
        byCol.setCellValueFactory(new PropertyValueFactory<>("billedBy"));

        billTable.getColumns().addAll(idCol, custCol, dateCol, totalCol, discCol, netCol, byCol);
        VBox.setVgrow(billTable, Priority.ALWAYS);

        contentArea.getChildren().addAll(title, totalSales, todaySales, billCount, billTable);
    }

    @SuppressWarnings("unchecked")
    private void showStockReport(VBox contentArea) {
        contentArea.getChildren().clear();

        Label title = new Label("Stock Report");
        title.setFont(Font.font("Arial", FontWeight.BOLD, 18));

        Label countLabel = new Label("Total Medicines in Inventory: " + inventoryManager.getMedicineCount());
        countLabel.setFont(Font.font("Arial", FontWeight.BOLD, 14));

        TableView<Medicine> table = new TableView<>();
        ObservableList<Medicine> data = FXCollections.observableArrayList(inventoryManager.getSortedByName());
        table.setItems(data);

        TableColumn<Medicine, String> idCol = new TableColumn<>("ID");
        idCol.setCellValueFactory(new PropertyValueFactory<>("medicineId"));
        TableColumn<Medicine, String> nameCol = new TableColumn<>("Name");
        nameCol.setCellValueFactory(new PropertyValueFactory<>("name"));
        nameCol.setPrefWidth(170);
        TableColumn<Medicine, String> catCol = new TableColumn<>("Category");
        catCol.setCellValueFactory(new PropertyValueFactory<>("category"));
        TableColumn<Medicine, Integer> qtyCol = new TableColumn<>("Quantity");
        qtyCol.setCellValueFactory(new PropertyValueFactory<>("quantity"));
        TableColumn<Medicine, Double> priceCol = new TableColumn<>("Price");
        priceCol.setCellValueFactory(new PropertyValueFactory<>("price"));
        TableColumn<Medicine, String> expCol = new TableColumn<>("Expiry");
        expCol.setCellValueFactory(new PropertyValueFactory<>("expiryDate"));
        expCol.setPrefWidth(100);

        table.getColumns().addAll(idCol, nameCol, catCol, qtyCol, priceCol, expCol);
        VBox.setVgrow(table, Priority.ALWAYS);

        contentArea.getChildren().addAll(title, countLabel, table);
    }

    @SuppressWarnings("unchecked")
    private void showExpiryAlerts(VBox contentArea) {
        contentArea.getChildren().clear();

        Label title = new Label("Expiry Alerts");
        title.setFont(Font.font("Arial", FontWeight.BOLD, 18));
        title.setStyle("-fx-text-fill: #e74c3c;");

        SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
        String currentDate = sdf.format(new Date());
        Calendar cal = Calendar.getInstance();
        cal.add(Calendar.DAY_OF_MONTH, 30);
        String thresholdDate = sdf.format(cal.getTime());

        // Expired medicines
        ArrayList<Medicine> expired = inventoryManager.getExpiredMedicines(currentDate);
        Label expiredTitle = new Label("EXPIRED Medicines (" + expired.size() + ")");
        expiredTitle.setFont(Font.font("Arial", FontWeight.BOLD, 14));
        expiredTitle.setStyle("-fx-text-fill: #e74c3c;");

        TableView<Medicine> expiredTable = new TableView<>();
        expiredTable.setItems(FXCollections.observableArrayList(expired));
        addMedicineColumns(expiredTable);
        expiredTable.setPrefHeight(200);

        // Expiring soon
        ArrayList<Medicine> expiringSoon = inventoryManager.getExpiringSoon(currentDate, thresholdDate);
        Label expiringTitle = new Label("Expiring Within 30 Days (" + expiringSoon.size() + ")");
        expiringTitle.setFont(Font.font("Arial", FontWeight.BOLD, 14));
        expiringTitle.setStyle("-fx-text-fill: #e67e22;");

        TableView<Medicine> expiringTable = new TableView<>();
        expiringTable.setItems(FXCollections.observableArrayList(expiringSoon));
        addMedicineColumns(expiringTable);
        VBox.setVgrow(expiringTable, Priority.ALWAYS);

        contentArea.getChildren().addAll(title, expiredTitle, expiredTable, expiringTitle, expiringTable);
    }

    @SuppressWarnings("unchecked")
    private void showLowStockAlerts(VBox contentArea) {
        contentArea.getChildren().clear();

        Label title = new Label("Low Stock Alerts (< 10 units)");
        title.setFont(Font.font("Arial", FontWeight.BOLD, 18));
        title.setStyle("-fx-text-fill: #e67e22;");

        ArrayList<Medicine> lowStock = inventoryManager.getLowStockMedicines();
        Label countLabel = new Label("Low Stock Items: " + lowStock.size());
        countLabel.setFont(Font.font("Arial", FontWeight.BOLD, 14));

        TableView<Medicine> table = new TableView<>();
        table.setItems(FXCollections.observableArrayList(lowStock));
        addMedicineColumns(table);
        VBox.setVgrow(table, Priority.ALWAYS);

        contentArea.getChildren().addAll(title, countLabel, table);
    }

    private void showSummary(VBox contentArea) {
        contentArea.getChildren().clear();

        Label title = new Label("System Summary");
        title.setFont(Font.font("Arial", FontWeight.BOLD, 18));

        GridPane summaryGrid = new GridPane();
        summaryGrid.setVgap(15);
        summaryGrid.setHgap(20);
        summaryGrid.setPadding(new Insets(20));

        addSummaryCard(summaryGrid, 0, 0, "Total Medicines",
                       String.valueOf(inventoryManager.getMedicineCount()), "#3498db");
        addSummaryCard(summaryGrid, 1, 0, "Total Customers",
                       String.valueOf(customerService.getCustomerCount()), "#9b59b6");
        addSummaryCard(summaryGrid, 2, 0, "Total Suppliers",
                       String.valueOf(supplierService.getSupplierCount()), "#e67e22");
        addSummaryCard(summaryGrid, 0, 1, "Total Bills",
                       String.valueOf(billingService.getBillCount()), "#27ae60");
        addSummaryCard(summaryGrid, 1, 1, "Total Sales",
                       String.format("Rs.%.2f", billingService.getTotalSales()), "#2c3e50");

        String currentDate = new SimpleDateFormat("yyyy-MM-dd").format(new Date());
        addSummaryCard(summaryGrid, 2, 1, "Low Stock Items",
                       String.valueOf(inventoryManager.getLowStockMedicines().size()), "#e74c3c");

        // Thread status
        Label threadStatus = new Label("Background Threads:");
        threadStatus.setFont(Font.font("Arial", FontWeight.BOLD, 14));

        Label expiryThreadLabel = new Label("Expiry Alert Thread: " +
                (expiryAlertThread != null && expiryAlertThread.isAlive() ? "RUNNING" : "STOPPED"));
        expiryThreadLabel.setStyle(expiryAlertThread != null && expiryAlertThread.isAlive() ?
                "-fx-text-fill: #27ae60;" : "-fx-text-fill: #e74c3c;");

        Label stockThreadLabel = new Label("Stock Alert Thread: RUNNING (daemon)");
        stockThreadLabel.setStyle("-fx-text-fill: #27ae60;");

        contentArea.getChildren().addAll(title, summaryGrid, new Separator(),
                threadStatus, expiryThreadLabel, stockThreadLabel);
    }

    private void addSummaryCard(GridPane grid, int col, int row, String label, String value, String color) {
        VBox card = new VBox(5);
        card.setPadding(new Insets(15));
        card.setPrefSize(180, 80);
        card.setAlignment(Pos.CENTER);
        card.setStyle("-fx-background-color: " + color + "; -fx-background-radius: 8;");

        Label valLabel = new Label(value);
        valLabel.setFont(Font.font("Arial", FontWeight.BOLD, 20));
        valLabel.setStyle("-fx-text-fill: white;");

        Label nameLabel = new Label(label);
        nameLabel.setStyle("-fx-text-fill: #ecf0f1; -fx-font-size: 12;");

        card.getChildren().addAll(valLabel, nameLabel);
        grid.add(card, col, row);
    }

    private void runBackup(VBox contentArea) {
        contentArea.getChildren().clear();

        Label title = new Label("Data Backup");
        title.setFont(Font.font("Arial", FontWeight.BOLD, 18));

        Label statusLabel = new Label("Starting backup...");
        statusLabel.setStyle("-fx-text-fill: #3498db; -fx-font-size: 14;");

        ProgressIndicator progress = new ProgressIndicator();
        progress.setPrefSize(50, 50);

        contentArea.getChildren().addAll(title, progress, statusLabel);

        // Run backup in a separate thread (BackupService implements Runnable)
        BackupService backupService = new BackupService(
                inventoryManager, customerService, supplierService,
                billingService, app.getPrescriptionService());
        backupService.setCallback(message -> {
            Platform.runLater(() -> {
                statusLabel.setText(message);
                statusLabel.setStyle("-fx-text-fill: #27ae60; -fx-font-size: 14;");
                progress.setProgress(1.0);

                Label pathLabel = new Label("Backup files saved in: data/ directory");
                pathLabel.setStyle("-fx-font-size: 12;");

                Label filesLabel = new Label(
                    "Files created:\n" +
                    "  - backup_medicines.txt\n" +
                    "  - backup_customers.txt\n" +
                    "  - backup_suppliers.txt\n" +
                    "  - backup_bills.txt\n" +
                    "  - backup_prescriptions.txt");
                filesLabel.setStyle("-fx-font-size: 12;");

                contentArea.getChildren().addAll(pathLabel, filesLabel);
            });
        });

        Thread backupThread = new Thread(backupService, "BackupThread");
        backupThread.setDaemon(true);
        backupThread.start();
    }

    @SuppressWarnings("unchecked")
    private void addMedicineColumns(TableView<Medicine> table) {
        TableColumn<Medicine, String> idCol = new TableColumn<>("ID");
        idCol.setCellValueFactory(new PropertyValueFactory<>("medicineId"));
        TableColumn<Medicine, String> nameCol = new TableColumn<>("Name");
        nameCol.setCellValueFactory(new PropertyValueFactory<>("name"));
        nameCol.setPrefWidth(150);
        TableColumn<Medicine, String> catCol = new TableColumn<>("Category");
        catCol.setCellValueFactory(new PropertyValueFactory<>("category"));
        TableColumn<Medicine, Integer> qtyCol = new TableColumn<>("Qty");
        qtyCol.setCellValueFactory(new PropertyValueFactory<>("quantity"));
        TableColumn<Medicine, Double> priceCol = new TableColumn<>("Price");
        priceCol.setCellValueFactory(new PropertyValueFactory<>("price"));
        TableColumn<Medicine, String> expCol = new TableColumn<>("Expiry");
        expCol.setCellValueFactory(new PropertyValueFactory<>("expiryDate"));
        expCol.setPrefWidth(100);

        table.getColumns().addAll(idCol, nameCol, catCol, qtyCol, priceCol, expCol);
    }

    private Button createMenuButton(String text, String color) {
        Button btn = new Button(text);
        btn.setPrefWidth(170);
        btn.setStyle("-fx-background-color: " + color + "; -fx-text-fill: white; " +
                    "-fx-font-size: 12; -fx-cursor: hand; -fx-alignment: center-left;");
        return btn;
    }

    public Scene getScene() { return scene; }
}
