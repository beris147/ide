package com.uaa.idejavafx;

import java.io.IOException;
import javafx.fxml.FXML;

public class PrimaryController {
    @FXML
    private void openNewFile() throws IOException {
        System.out.println("New file");
    }
    
    @FXML
    private void saveFile() throws IOException {
        System.out.println("Save file");
    }
    
    @FXML
    private void saveFileAs() throws IOException {
        System.out.println("Save file as...");
    }
    
    @FXML
    private void openFile() throws IOException {
        System.out.println("Open file");
    }
    
    @FXML
    private void undo() throws IOException {
        System.out.println("undo");
    }
    
    @FXML
    private void redo() throws IOException {
        System.out.println("redo");
    }
    
    @FXML
    private void run() throws IOException {
        System.out.println("run");
    }
}
