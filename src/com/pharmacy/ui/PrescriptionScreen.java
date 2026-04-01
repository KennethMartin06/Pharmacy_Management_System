package com.pharmacy.ui;

import com.pharmacy.model.*;
import com.pharmacy.service.*;
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

import java.text.SimpleDateFormat;
import java.util.Date;

/**
 * Prescription Handling Screen.
 * Demonstrates: JavaFX TableView, GridPane, VBox/HBox, ArrayList operations.
 */
public class PrescriptionScreen {

    private Scene scene;
    private PharmacyApp app;
    private PrescriptionService prescriptionService;
    private CustomerService customerService;
    private InventoryManager inventoryManager;
    private TableView<Prescription> tableView;
    private ObservableList<Prescription> tableData;

    public PrescriptionScreen(PharmacyApp app, PrescriptionService prescriptionService,
                               CustomerService customerService, InventoryManager inventoryManager) {
        this.app = app;
        this.prescriptionService = prescriptionService;
        this.customerService = customerService;
        this.inventoryManager = inventoryManager;
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

        Label titleLabel = new Label("Prescription Handling");
        titleLabel.setFont(Font.font("Arial", FontWeight.BOLD, 20));
        titleLabel.setStyle("-fx-text-fill: white;");

        topBar.getChildren().addAll(backBtn, titleLabel);
        root.setTop(topBar);

        // Left - Form
        VBox formBox = new VBox(10);
        formBox.setPadding(new Insets(15));
        formBox.setPrefWidth(330);
        formBox.setStyle("-fx-background-color: white; -fx-border-color: #bdc3c7; -fx-border-width: 0 1 0 0;");

        Label formTitle = new Label("New Prescription");
        formTitle.setFont(Font.font("Arial", FontWeight.BOLD, 15));

        GridPane grid = new GridPane();
        grid.setVgap(8);
        grid.setHgap(8);

        TextField custIdField = new TextField();
        custIdField.setPromptText("Customer ID");
        TextField custNameField = new TextField();
        custNameField.setPromptText("Patient name");
        TextField doctorField = new TextField();
        doctorField.setPromptText("Doctor name");
        TextField notesField = new TextField();
        notesField.setPromptText("Notes/Instructions");

        custIdField.textProperty().addListener((obs, o, n) -> {
            if (n != null && !n.isEmpty()) {
                Customer cust = customerService.getCustomerById(n.trim());
                if (cust != null) custNameField.setText(cust.getName());
            }
        });

        int r = 0;
        grid.add(new Label("Customer ID:"), 0, r); grid.add(custIdField, 1, r++);
        grid.add(new Label("Patient Name:"), 0, r); grid.add(custNameField, 1, r++);
        grid.add(new Label("Doctor:"), 0, r); grid.add(doctorField, 1, r++);
        grid.add(new Label("Notes:"), 0, r); grid.add(notesField, 1, r++);

        // Prescription items
        Label itemsTitle = new Label("Prescribed Medicines");
        itemsTitle.setFont(Font.font("Arial", FontWeight.BOLD, 13));

        TextField medIdField = new TextField();
        medIdField.setPromptText("Medicine ID");
        Label medNameLabel = new Label("-");
        TextField medQtyField = new TextField();
        medQtyField.setPromptText("Quantity");
        TextField dosageField = new TextField();
        dosageField.setPromptText("e.g., 1-0-1");

        medIdField.textProperty().addListener((obs, o, n) -> {
            if (n != null && !n.isEmpty()) {
                Medicine med = inventoryManager.getMedicineById(n.trim());
                if (med != null) medNameLabel.setText(med.getName());
            }
        });

        GridPane itemGrid = new GridPane();
        itemGrid.setVgap(6);
        itemGrid.setHgap(6);
        int ir = 0;
        itemGrid.add(new Label("Med ID:"), 0, ir); itemGrid.add(medIdField, 1, ir++);
        itemGrid.add(new Label("Name:"), 0, ir); itemGrid.add(medNameLabel, 1, ir++);
        itemGrid.add(new Label("Qty:"), 0, ir); itemGrid.add(medQtyField, 1, ir++);
        itemGrid.add(new Label("Dosage:"), 0, ir); itemGrid.add(dosageField, 1, ir++);

        // Items list display
        ListView<String> itemsList = new ListView<>();
        itemsList.setPrefHeight(120);
        java.util.ArrayList<PrescriptionItem> presItems = new java.util.ArrayList<>();

        Label statusLabel = new Label();

        Button addItemBtn = new Button("Add Medicine");
        addItemBtn.setStyle("-fx-background-color: #3498db; -fx-text-fill: white; -fx-cursor: hand; -fx-pref-width: 200;");
        addItemBtn.setOnAction(e -> {
            try {
                String medId = medIdField.getText().trim();
                Medicine med = inventoryManager.getMedicineById(medId);
                if (med == null) { statusLabel.setText("Medicine not found!"); return; }
                int qty = Integer.parseInt(medQtyField.getText().trim());
                PrescriptionItem item = new PrescriptionItem(medId, med.getName(), qty, dosageField.getText());
                presItems.add(item);
                itemsList.getItems().add(item.toString());
                medIdField.clear();
                medQtyField.clear();
                dosageField.clear();
                medNameLabel.setText("-");
            } catch (Exception ex) {
                statusLabel.setText("Error: " + ex.getMessage());
            }
        });

        Button saveBtn = new Button("Save Prescription");
        saveBtn.setStyle("-fx-background-color: #27ae60; -fx-text-fill: white; -fx-font-size: 13; " +
                        "-fx-pref-width: 280; -fx-cursor: hand;");
        saveBtn.setOnAction(e -> {
            if (custNameField.getText().trim().isEmpty() || doctorField.getText().trim().isEmpty()) {
                statusLabel.setText("Fill all fields!");
                statusLabel.setStyle("-fx-text-fill: #e74c3c;");
                return;
            }
            String presId = IDGenerator.generatePrescriptionId();
            String date = new SimpleDateFormat("yyyy-MM-dd").format(new Date());
            Prescription pres = new Prescription(presId, custIdField.getText().trim(),
                    custNameField.getText(), doctorField.getText(), date, notesField.getText());
            for (PrescriptionItem item : presItems) {
                pres.addItem(item);
            }
            prescriptionService.addPrescription(pres);
            refreshTable();
            presItems.clear();
            itemsList.getItems().clear();
            custIdField.clear(); custNameField.clear(); doctorField.clear(); notesField.clear();
            statusLabel.setText("Prescription saved: " + presId);
            statusLabel.setStyle("-fx-text-fill: #27ae60;");
        });

        formBox.getChildren().addAll(formTitle, grid, new Separator(),
                itemsTitle, itemGrid, addItemBtn, itemsList, new Separator(),
                saveBtn, statusLabel);
        root.setLeft(formBox);

        // Center - Table
        VBox tableBox = new VBox(10);
        tableBox.setPadding(new Insets(15));

        Label tableTitle = new Label("All Prescriptions");
        tableTitle.setFont(Font.font("Arial", FontWeight.BOLD, 15));

        tableView = new TableView<>();

        TableColumn<Prescription, String> idCol = new TableColumn<>("ID");
        idCol.setCellValueFactory(new PropertyValueFactory<>("prescriptionId"));

        TableColumn<Prescription, String> patCol = new TableColumn<>("Patient");
        patCol.setCellValueFactory(new PropertyValueFactory<>("customerName"));
        patCol.setPrefWidth(130);

        TableColumn<Prescription, String> docCol = new TableColumn<>("Doctor");
        docCol.setCellValueFactory(new PropertyValueFactory<>("doctorName"));
        docCol.setPrefWidth(130);

        TableColumn<Prescription, String> dateCol = new TableColumn<>("Date");
        dateCol.setCellValueFactory(new PropertyValueFactory<>("date"));

        TableColumn<Prescription, String> notesCol = new TableColumn<>("Notes");
        notesCol.setCellValueFactory(new PropertyValueFactory<>("notes"));
        notesCol.setPrefWidth(180);

        tableView.getColumns().addAll(idCol, patCol, docCol, dateCol, notesCol);
        refreshTable();

        // Details area
        TextArea detailsArea = new TextArea();
        detailsArea.setEditable(false);
        detailsArea.setPrefHeight(150);
        detailsArea.setPromptText("Select a prescription to view details...");

        tableView.getSelectionModel().selectedItemProperty().addListener((obs, o, n) -> {
            if (n != null) {
                StringBuilder sb = new StringBuilder();
                sb.append("Prescription: ").append(n.getPrescriptionId()).append("\n");
                sb.append("Patient: ").append(n.getCustomerName()).append("\n");
                sb.append("Doctor: Dr. ").append(n.getDoctorName()).append("\n");
                sb.append("Date: ").append(n.getDate()).append("\n");
                sb.append("Notes: ").append(n.getNotes()).append("\n\n");
                sb.append("Prescribed Medicines:\n");
                for (PrescriptionItem item : n.getItems()) {
                    sb.append("  - ").append(item.toString()).append("\n");
                }
                detailsArea.setText(sb.toString());
            }
        });

        Button deleteBtn = new Button("Delete Selected");
        deleteBtn.setStyle("-fx-background-color: #e74c3c; -fx-text-fill: white; -fx-cursor: hand;");
        deleteBtn.setOnAction(e -> {
            Prescription sel = tableView.getSelectionModel().getSelectedItem();
            if (sel != null) {
                prescriptionService.deletePrescription(sel.getPrescriptionId());
                refreshTable();
                detailsArea.clear();
            }
        });

        VBox.setVgrow(tableView, Priority.ALWAYS);
        tableBox.getChildren().addAll(tableTitle, tableView, new Label("Details:"), detailsArea, deleteBtn);
        root.setCenter(tableBox);

        scene = new Scene(root, 1100, 700);
    }

    private void refreshTable() {
        tableData = FXCollections.observableArrayList(prescriptionService.getAllPrescriptions());
        tableView.setItems(tableData);
    }

    public Scene getScene() { return scene; }
}
