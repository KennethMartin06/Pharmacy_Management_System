package com.pharmacy.ui;

import com.pharmacy.model.Customer;
import com.pharmacy.service.CustomerService;
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

/**
 * Customer/Patient Records Screen.
 * Demonstrates: JavaFX TableView, GridPane, VBox/HBox, Event handling.
 */
public class CustomerScreen {

    private Scene scene;
    private PharmacyApp app;
    private CustomerService customerService;
    private TableView<Customer> tableView;
    private ObservableList<Customer> tableData;

    public CustomerScreen(PharmacyApp app, CustomerService customerService) {
        this.app = app;
        this.customerService = customerService;
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

        Label titleLabel = new Label("Customer / Patient Records");
        titleLabel.setFont(Font.font("Arial", FontWeight.BOLD, 20));
        titleLabel.setStyle("-fx-text-fill: white;");

        topBar.getChildren().addAll(backBtn, titleLabel);
        root.setTop(topBar);

        // Left - Form
        VBox formBox = new VBox(10);
        formBox.setPadding(new Insets(15));
        formBox.setPrefWidth(320);
        formBox.setStyle("-fx-background-color: white; -fx-border-color: #bdc3c7; -fx-border-width: 0 1 0 0;");

        Label formTitle = new Label("Add / Edit Customer");
        formTitle.setFont(Font.font("Arial", FontWeight.BOLD, 15));

        GridPane grid = new GridPane();
        grid.setVgap(8);
        grid.setHgap(8);

        TextField idField = new TextField();
        idField.setEditable(false);
        idField.setPromptText("Auto-generated");
        TextField nameField = new TextField();
        nameField.setPromptText("Full name");
        TextField phoneField = new TextField();
        phoneField.setPromptText("Phone number");
        TextField emailField = new TextField();
        emailField.setPromptText("Email");
        TextField addressField = new TextField();
        addressField.setPromptText("Address");

        int row = 0;
        grid.add(new Label("ID:"), 0, row); grid.add(idField, 1, row++);
        grid.add(new Label("Name:"), 0, row); grid.add(nameField, 1, row++);
        grid.add(new Label("Phone:"), 0, row); grid.add(phoneField, 1, row++);
        grid.add(new Label("Email:"), 0, row); grid.add(emailField, 1, row++);
        grid.add(new Label("Address:"), 0, row); grid.add(addressField, 1, row++);

        Label statusLabel = new Label();

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

        addBtn.setOnAction(e -> {
            String id = IDGenerator.generateCustomerId();
            Customer cust = new Customer(id, nameField.getText(), phoneField.getText(),
                    emailField.getText(), addressField.getText());
            customerService.addCustomer(cust);
            refreshTable();
            clearFields(idField, nameField, phoneField, emailField, addressField);
            statusLabel.setText("Customer added: " + id);
            statusLabel.setStyle("-fx-text-fill: #27ae60;");
        });

        updateBtn.setOnAction(e -> {
            String id = idField.getText();
            if (id.isEmpty()) { statusLabel.setText("Select a customer!"); return; }
            Customer cust = new Customer(id, nameField.getText(), phoneField.getText(),
                    emailField.getText(), addressField.getText());
            customerService.updateCustomer(cust);
            refreshTable();
            statusLabel.setText("Customer updated: " + id);
            statusLabel.setStyle("-fx-text-fill: #27ae60;");
        });

        deleteBtn.setOnAction(e -> {
            String id = idField.getText();
            if (!id.isEmpty()) {
                customerService.deleteCustomer(id);
                refreshTable();
                clearFields(idField, nameField, phoneField, emailField, addressField);
                statusLabel.setText("Customer deleted.");
            }
        });

        clearBtn.setOnAction(e -> {
            clearFields(idField, nameField, phoneField, emailField, addressField);
            statusLabel.setText("");
        });

        formBox.getChildren().addAll(formTitle, grid, btnBox, statusLabel);
        root.setLeft(formBox);

        // Center - Table
        VBox tableBox = new VBox(10);
        tableBox.setPadding(new Insets(15));

        HBox searchBox = new HBox(10);
        TextField searchField = new TextField();
        searchField.setPromptText("Search by name...");
        Button searchBtn = new Button("Search");
        searchBtn.setStyle("-fx-background-color: #3498db; -fx-text-fill: white; -fx-cursor: hand;");
        searchBtn.setOnAction(e -> {
            String q = searchField.getText().trim();
            if (q.isEmpty()) refreshTable();
            else {
                tableData = FXCollections.observableArrayList(customerService.searchByName(q));
                tableView.setItems(tableData);
            }
        });
        Button showAllBtn = new Button("Show All");
        showAllBtn.setStyle("-fx-background-color: #7f8c8d; -fx-text-fill: white; -fx-cursor: hand;");
        showAllBtn.setOnAction(e -> refreshTable());
        searchBox.getChildren().addAll(searchField, searchBtn, showAllBtn);

        tableView = new TableView<>();

        TableColumn<Customer, String> idCol = new TableColumn<>("ID");
        idCol.setCellValueFactory(new PropertyValueFactory<>("customerId"));

        TableColumn<Customer, String> nameCol = new TableColumn<>("Name");
        nameCol.setCellValueFactory(new PropertyValueFactory<>("name"));
        nameCol.setPrefWidth(150);

        TableColumn<Customer, String> phoneCol = new TableColumn<>("Phone");
        phoneCol.setCellValueFactory(new PropertyValueFactory<>("phone"));
        phoneCol.setPrefWidth(120);

        TableColumn<Customer, String> emailCol = new TableColumn<>("Email");
        emailCol.setCellValueFactory(new PropertyValueFactory<>("email"));
        emailCol.setPrefWidth(170);

        TableColumn<Customer, String> addrCol = new TableColumn<>("Address");
        addrCol.setCellValueFactory(new PropertyValueFactory<>("address"));
        addrCol.setPrefWidth(180);

        tableView.getColumns().addAll(idCol, nameCol, phoneCol, emailCol, addrCol);
        refreshTable();

        tableView.getSelectionModel().selectedItemProperty().addListener((obs, o, n) -> {
            if (n != null) {
                idField.setText(n.getCustomerId());
                nameField.setText(n.getName());
                phoneField.setText(n.getPhone());
                emailField.setText(n.getEmail());
                addressField.setText(n.getAddress());
            }
        });

        VBox.setVgrow(tableView, Priority.ALWAYS);
        tableBox.getChildren().addAll(searchBox, tableView);
        root.setCenter(tableBox);

        scene = new Scene(root, 1100, 700);
    }

    private void refreshTable() {
        tableData = FXCollections.observableArrayList(customerService.getAllCustomers());
        tableView.setItems(tableData);
    }

    private void clearFields(TextField... fields) {
        for (TextField f : fields) f.clear();
        tableView.getSelectionModel().clearSelection();
    }

    public Scene getScene() { return scene; }
}
