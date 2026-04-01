package com.pharmacy.ui;

import com.pharmacy.model.Medicine;
import com.pharmacy.model.MedicineCategory;
import com.pharmacy.service.InventoryManager;
import com.pharmacy.service.SupplierService;
import com.pharmacy.util.IDGenerator;

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

import java.util.ArrayList;

/**
 * Inventory Management Screen.
 * Demonstrates: JavaFX TableView, GridPane, VBox/HBox, Buttons, ComboBox.
 */
public class InventoryScreen {

    private Scene scene;
    private PharmacyApp app;
    private InventoryManager inventoryManager;
    private SupplierService supplierService;
    private TableView<Medicine> tableView;
    private ObservableList<Medicine> tableData;

    public InventoryScreen(PharmacyApp app, InventoryManager inventoryManager,
                           SupplierService supplierService) {
        this.app = app;
        this.inventoryManager = inventoryManager;
        this.supplierService = supplierService;
        createScene();
    }

    @SuppressWarnings("unchecked")
    private void createScene() {
        BorderPane root = new BorderPane();
        root.setStyle("-fx-background-color: #ecf0f1;");

        // Top bar
        HBox topBar = createTopBar("Inventory Management");
        root.setTop(topBar);

        // Left side - Form
        VBox formBox = createForm();
        root.setLeft(formBox);

        // Center - Table
        VBox tableBox = createTable();
        root.setCenter(tableBox);

        scene = new Scene(root, 1100, 700);
    }

    private HBox createTopBar(String title) {
        HBox topBar = new HBox(15);
        topBar.setPadding(new Insets(12, 20, 12, 20));
        topBar.setAlignment(Pos.CENTER_LEFT);
        topBar.setStyle("-fx-background-color: #2c3e50;");

        Button backBtn = new Button("< Back");
        backBtn.setStyle("-fx-background-color: #7f8c8d; -fx-text-fill: white; -fx-cursor: hand;");
        backBtn.setOnAction(e -> app.showDashboard(app.getUserService().getCurrentUser()));

        Label titleLabel = new Label(title);
        titleLabel.setFont(Font.font("Arial", FontWeight.BOLD, 20));
        titleLabel.setStyle("-fx-text-fill: white;");

        topBar.getChildren().addAll(backBtn, titleLabel);
        return topBar;
    }

    private VBox createForm() {
        VBox formBox = new VBox(10);
        formBox.setPadding(new Insets(15));
        formBox.setPrefWidth(320);
        formBox.setStyle("-fx-background-color: white; -fx-border-color: #bdc3c7; -fx-border-width: 0 1 0 0;");

        Label formTitle = new Label("Add / Edit Medicine");
        formTitle.setFont(Font.font("Arial", FontWeight.BOLD, 15));

        // Form fields using GridPane
        GridPane grid = new GridPane();
        grid.setVgap(8);
        grid.setHgap(8);

        TextField idField = new TextField();
        idField.setEditable(false);
        idField.setPromptText("Auto-generated");

        TextField nameField = new TextField();
        nameField.setPromptText("Medicine name");

        TextField mfgField = new TextField();
        mfgField.setPromptText("Manufacturer");

        ComboBox<MedicineCategory> categoryBox = new ComboBox<>();
        categoryBox.getItems().addAll(MedicineCategory.values());
        categoryBox.setPromptText("Select Category");
        categoryBox.setPrefWidth(180);

        TextField batchField = new TextField();
        batchField.setPromptText("Batch number");

        TextField expiryField = new TextField();
        expiryField.setPromptText("YYYY-MM-DD");

        TextField qtyField = new TextField();
        qtyField.setPromptText("Quantity");

        TextField priceField = new TextField();
        priceField.setPromptText("Price (Rs.)");

        TextField supplierField = new TextField();
        supplierField.setPromptText("Supplier ID");

        int row = 0;
        grid.add(new Label("ID:"), 0, row); grid.add(idField, 1, row++);
        grid.add(new Label("Name:"), 0, row); grid.add(nameField, 1, row++);
        grid.add(new Label("Manufacturer:"), 0, row); grid.add(mfgField, 1, row++);
        grid.add(new Label("Category:"), 0, row); grid.add(categoryBox, 1, row++);
        grid.add(new Label("Batch No:"), 0, row); grid.add(batchField, 1, row++);
        grid.add(new Label("Expiry Date:"), 0, row); grid.add(expiryField, 1, row++);
        grid.add(new Label("Quantity:"), 0, row); grid.add(qtyField, 1, row++);
        grid.add(new Label("Price:"), 0, row); grid.add(priceField, 1, row++);
        grid.add(new Label("Supplier ID:"), 0, row); grid.add(supplierField, 1, row++);

        Label statusLabel = new Label();
        statusLabel.setStyle("-fx-text-fill: #27ae60;");

        // Buttons
        HBox btnBox = new HBox(8);
        Button addBtn = new Button("Add");
        addBtn.setStyle("-fx-background-color: #27ae60; -fx-text-fill: white; -fx-cursor: hand;");
        Button updateBtn = new Button("Update");
        updateBtn.setStyle("-fx-background-color: #2980b9; -fx-text-fill: white; -fx-cursor: hand;");
        Button deleteBtn = new Button("Delete");
        deleteBtn.setStyle("-fx-background-color: #e74c3c; -fx-text-fill: white; -fx-cursor: hand;");
        Button clearBtn = new Button("Clear");
        clearBtn.setStyle("-fx-background-color: #7f8c8d; -fx-text-fill: white; -fx-cursor: hand;");
        btnBox.getChildren().addAll(addBtn, updateBtn, deleteBtn, clearBtn);

        // Add button action
        addBtn.setOnAction(e -> {
            try {
                String id = IDGenerator.generateMedicineId();
                Medicine med = new Medicine(id, nameField.getText(), mfgField.getText(),
                        categoryBox.getValue(), batchField.getText(), expiryField.getText(),
                        Integer.parseInt(qtyField.getText()), // Wrapper class parsing
                        Double.parseDouble(priceField.getText()), // Wrapper class parsing
                        supplierField.getText());
                inventoryManager.addMedicine(med);
                refreshTable();
                clearFields(idField, nameField, mfgField, categoryBox, batchField,
                           expiryField, qtyField, priceField, supplierField);
                statusLabel.setText("Medicine added: " + id);
                statusLabel.setStyle("-fx-text-fill: #27ae60;");
            } catch (Exception ex) {
                statusLabel.setText("Error: " + ex.getMessage());
                statusLabel.setStyle("-fx-text-fill: #e74c3c;");
            }
        });

        // Update button action
        updateBtn.setOnAction(e -> {
            try {
                String id = idField.getText();
                if (id.isEmpty()) {
                    statusLabel.setText("Select a medicine first!");
                    statusLabel.setStyle("-fx-text-fill: #e74c3c;");
                    return;
                }
                Medicine med = new Medicine(id, nameField.getText(), mfgField.getText(),
                        categoryBox.getValue(), batchField.getText(), expiryField.getText(),
                        Integer.parseInt(qtyField.getText()),
                        Double.parseDouble(priceField.getText()),
                        supplierField.getText());
                inventoryManager.updateMedicine(med);
                refreshTable();
                statusLabel.setText("Medicine updated: " + id);
                statusLabel.setStyle("-fx-text-fill: #27ae60;");
            } catch (Exception ex) {
                statusLabel.setText("Error: " + ex.getMessage());
                statusLabel.setStyle("-fx-text-fill: #e74c3c;");
            }
        });

        // Delete button action
        deleteBtn.setOnAction(e -> {
            String id = idField.getText();
            if (!id.isEmpty()) {
                inventoryManager.deleteMedicine(id);
                refreshTable();
                clearFields(idField, nameField, mfgField, categoryBox, batchField,
                           expiryField, qtyField, priceField, supplierField);
                statusLabel.setText("Medicine deleted: " + id);
            }
        });

        // Clear button
        clearBtn.setOnAction(e -> {
            clearFields(idField, nameField, mfgField, categoryBox, batchField,
                       expiryField, qtyField, priceField, supplierField);
            statusLabel.setText("");
        });

        // Table selection listener - populate form
        tableView = new TableView<>();
        tableView.getSelectionModel().selectedItemProperty().addListener((obs, oldVal, newVal) -> {
            if (newVal != null) {
                idField.setText(newVal.getMedicineId());
                nameField.setText(newVal.getName());
                mfgField.setText(newVal.getManufacturer());
                categoryBox.setValue(newVal.getCategory());
                batchField.setText(newVal.getBatchNumber());
                expiryField.setText(newVal.getExpiryDate());
                qtyField.setText(String.valueOf(newVal.getQuantity()));
                priceField.setText(String.valueOf(newVal.getPrice()));
                supplierField.setText(newVal.getSupplierId());
            }
        });

        formBox.getChildren().addAll(formTitle, grid, btnBox, statusLabel);
        return formBox;
    }

    @SuppressWarnings("unchecked")
    private VBox createTable() {
        VBox tableBox = new VBox(10);
        tableBox.setPadding(new Insets(15));

        // Search and sort controls
        HBox controlsBox = new HBox(10);
        controlsBox.setAlignment(Pos.CENTER_LEFT);

        TextField searchField = new TextField();
        searchField.setPromptText("Search by name...");
        searchField.setPrefWidth(200);

        Button searchBtn = new Button("Search");
        searchBtn.setStyle("-fx-background-color: #3498db; -fx-text-fill: white; -fx-cursor: hand;");
        searchBtn.setOnAction(e -> {
            String query = searchField.getText().trim();
            if (query.isEmpty()) {
                refreshTable();
            } else {
                ArrayList<Medicine> results = inventoryManager.searchByName(query);
                tableData = FXCollections.observableArrayList(results);
                tableView.setItems(tableData);
            }
        });

        ComboBox<String> sortBox = new ComboBox<>();
        sortBox.getItems().addAll("Sort by Name", "Sort by Price", "Sort by Expiry");
        sortBox.setPromptText("Sort by...");
        sortBox.setOnAction(e -> {
            String selected = sortBox.getValue();
            ArrayList<Medicine> sorted;
            if ("Sort by Name".equals(selected)) {
                sorted = inventoryManager.getSortedByName();
            } else if ("Sort by Price".equals(selected)) {
                sorted = inventoryManager.getSortedByPrice();
            } else {
                sorted = inventoryManager.getSortedByExpiry();
            }
            tableData = FXCollections.observableArrayList(sorted);
            tableView.setItems(tableData);
        });

        ComboBox<MedicineCategory> filterBox = new ComboBox<>();
        filterBox.getItems().addAll(MedicineCategory.values());
        filterBox.setPromptText("Filter by Category");
        filterBox.setOnAction(e -> {
            MedicineCategory cat = filterBox.getValue();
            if (cat != null) {
                ArrayList<Medicine> filtered = inventoryManager.filterByCategory(cat);
                tableData = FXCollections.observableArrayList(filtered);
                tableView.setItems(tableData);
            }
        });

        Button refreshBtn = new Button("Show All");
        refreshBtn.setStyle("-fx-background-color: #7f8c8d; -fx-text-fill: white; -fx-cursor: hand;");
        refreshBtn.setOnAction(e -> refreshTable());

        controlsBox.getChildren().addAll(searchField, searchBtn, sortBox, filterBox, refreshBtn);

        // Table columns
        TableColumn<Medicine, String> idCol = new TableColumn<>("ID");
        idCol.setCellValueFactory(new PropertyValueFactory<>("medicineId"));
        idCol.setPrefWidth(80);

        TableColumn<Medicine, String> nameCol = new TableColumn<>("Name");
        nameCol.setCellValueFactory(new PropertyValueFactory<>("name"));
        nameCol.setPrefWidth(150);

        TableColumn<Medicine, MedicineCategory> catCol = new TableColumn<>("Category");
        catCol.setCellValueFactory(new PropertyValueFactory<>("category"));
        catCol.setPrefWidth(80);

        TableColumn<Medicine, String> batchCol = new TableColumn<>("Batch");
        batchCol.setCellValueFactory(new PropertyValueFactory<>("batchNumber"));
        batchCol.setPrefWidth(70);

        TableColumn<Medicine, String> expiryCol = new TableColumn<>("Expiry");
        expiryCol.setCellValueFactory(new PropertyValueFactory<>("expiryDate"));
        expiryCol.setPrefWidth(90);

        TableColumn<Medicine, Integer> qtyCol = new TableColumn<>("Qty");
        qtyCol.setCellValueFactory(new PropertyValueFactory<>("quantity"));
        qtyCol.setPrefWidth(50);

        TableColumn<Medicine, Double> priceCol = new TableColumn<>("Price");
        priceCol.setCellValueFactory(new PropertyValueFactory<>("price"));
        priceCol.setPrefWidth(70);

        tableView.getColumns().addAll(idCol, nameCol, catCol, batchCol, expiryCol, qtyCol, priceCol);
        refreshTable();

        VBox.setVgrow(tableView, Priority.ALWAYS);
        tableBox.getChildren().addAll(controlsBox, tableView);
        return tableBox;
    }

    private void refreshTable() {
        tableData = FXCollections.observableArrayList(inventoryManager.getAllMedicines());
        tableView.setItems(tableData);
    }

    private void clearFields(TextField idField, TextField nameField, TextField mfgField,
                              ComboBox<MedicineCategory> categoryBox, TextField batchField,
                              TextField expiryField, TextField qtyField, TextField priceField,
                              TextField supplierField) {
        idField.clear();
        nameField.clear();
        mfgField.clear();
        categoryBox.setValue(null);
        batchField.clear();
        expiryField.clear();
        qtyField.clear();
        priceField.clear();
        supplierField.clear();
        tableView.getSelectionModel().clearSelection();
    }

    public Scene getScene() {
        return scene;
    }
}
