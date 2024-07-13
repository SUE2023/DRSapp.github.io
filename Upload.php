<?php
$servername = "DRSApp_MYSQL_HOST";
$username = "DRSapp_MYSQL_USER";
$password = "DRSApp_MYSQL_PWD";
$dbname = "test";

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    $caption = $_POST['caption'];
    $img = $_FILES['img']['tmp_name'];

    if ($img) {
        $imgContent = addslashes(file_get_contents($img));
        $sql = "INSERT INTO pic (caption, img) VALUES ('$caption', '$imgContent')";

        if ($conn->query($sql) === TRUE) {
            echo "New record created successfully";
        } else {
            echo "Error: " . $sql . "<br>" . $conn->error;
        }
    } else {
        echo "Please select an image to upload.";
    }
}

$conn->close();
?>
