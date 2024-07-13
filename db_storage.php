<?php
// db_storage.php

// Database configuration
$servername = "localhost";
$username = "DRSapp_MYSQL_USER";
$password = "DRSApp_MYSQL_PWD";
$dbname = "database_name";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// Retrieve form data
$reports = $_POST['reports'];
$staff_name = $_POST['staff_name'];
$staff_number = $_POST['staff_number'];

// Prepare and bind
$stmt = $conn->prepare("INSERT INTO staff (reports, staff_name, staff_number) VALUES (?, ?, ?)");
$stmt->bind_param("sss", $reports, $staff_name, $staff_number);

// Execute the statement
if ($stmt->execute()) {
    echo "New record created successfully";
} else {
    echo "Error: " . $stmt->error;
}

// Close connection
$stmt->close();
$conn->close();
?>
