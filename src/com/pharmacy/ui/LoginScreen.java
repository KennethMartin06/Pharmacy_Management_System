package com.pharmacy.ui;

import com.pharmacy.model.User;
import com.pharmacy.service.UserService;

import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;

/**
 * Login Screen with role-based authentication.
 * Demonstrates: JavaFX (GridPane, TextField, Button, Label), Event handling.
 */
public class LoginScreen {

    private Scene scene;
    private PharmacyApp app;
    private UserService userService;

    public LoginScreen(PharmacyApp app, UserService userService) {
        this.app = app;
        this.userService = userService;
        createScene();
    }

    private void createScene() {
        // Main layout
        VBox mainLayout = new VBox(20);
        mainLayout.setAlignment(Pos.CENTER);
        mainLayout.setPadding(new Insets(50));
        mainLayout.setStyle("-fx-background-color: #2c3e50;");

        // Title
        Label titleLabel = new Label("PharmaCare");
        titleLabel.setFont(Font.font("Arial", FontWeight.BOLD, 36));
        titleLabel.setStyle("-fx-text-fill: #ecf0f1;");

        Label subtitleLabel = new Label("Pharmacy Management System");
        subtitleLabel.setFont(Font.font("Arial", FontWeight.NORMAL, 16));
        subtitleLabel.setStyle("-fx-text-fill: #bdc3c7;");

        // Login form using GridPane
        GridPane grid = new GridPane();
        grid.setAlignment(Pos.CENTER);
        grid.setHgap(10);
        grid.setVgap(15);
        grid.setPadding(new Insets(30));
        grid.setMaxWidth(400);
        grid.setStyle("-fx-background-color: #34495e; -fx-background-radius: 10;");

        Label loginTitle = new Label("Login");
        loginTitle.setFont(Font.font("Arial", FontWeight.BOLD, 20));
        loginTitle.setStyle("-fx-text-fill: #ecf0f1;");
        grid.add(loginTitle, 0, 0, 2, 1);

        Label userLabel = new Label("Username:");
        userLabel.setStyle("-fx-text-fill: #ecf0f1;");
        TextField usernameField = new TextField();
        usernameField.setPromptText("Enter username");
        usernameField.setPrefWidth(250);
        grid.add(userLabel, 0, 1);
        grid.add(usernameField, 1, 1);

        Label passLabel = new Label("Password:");
        passLabel.setStyle("-fx-text-fill: #ecf0f1;");
        PasswordField passwordField = new PasswordField();
        passwordField.setPromptText("Enter password");
        grid.add(passLabel, 0, 2);
        grid.add(passwordField, 1, 2);

        Label messageLabel = new Label();
        messageLabel.setStyle("-fx-text-fill: #e74c3c;");

        Button loginBtn = new Button("Login");
        loginBtn.setStyle("-fx-background-color: #27ae60; -fx-text-fill: white; " +
                          "-fx-font-size: 14; -fx-pref-width: 250; -fx-cursor: hand;");
        loginBtn.setOnAction(e -> {
            String username = usernameField.getText().trim();
            String password = passwordField.getText().trim();

            if (username.isEmpty() || password.isEmpty()) {
                messageLabel.setText("Please enter both username and password.");
                return;
            }

            User user = userService.authenticate(username, password);
            if (user != null) {
                app.showDashboard(user);
            } else {
                messageLabel.setText("Invalid credentials! Please try again.");
                passwordField.clear();
            }
        });

        // Allow Enter key to login
        passwordField.setOnAction(e -> loginBtn.fire());
        usernameField.setOnAction(e -> loginBtn.fire());

        grid.add(loginBtn, 0, 3, 2, 1);
        grid.add(messageLabel, 0, 4, 2, 1);

        // Default credentials hint
        Label hintLabel = new Label("Default: admin/admin123 or pharmacist/pharma123");
        hintLabel.setStyle("-fx-text-fill: #7f8c8d; -fx-font-size: 11;");

        mainLayout.getChildren().addAll(titleLabel, subtitleLabel, grid, hintLabel);

        scene = new Scene(mainLayout, 1100, 700);
    }

    public Scene getScene() {
        return scene;
    }
}
