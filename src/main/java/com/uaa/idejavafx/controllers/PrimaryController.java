package com.uaa.idejavafx.controllers;

import com.uaa.classes.FileHelper;
import java.io.IOException;
import javafx.fxml.FXML;
import javafx.scene.control.Tab;
import org.fxmisc.richtext.*;

public class PrimaryController {
    @FXML
    private CodeArea codeText;
    @FXML
    private Tab tabTitle;
    
    private final FileHelper fileHelper = new FileHelper();
    
    private void setTitle(){
        if(this.fileHelper.getFile() != null){
            this.tabTitle.setText(this.fileHelper.getFile().getName());
        } else{
            this.tabTitle.setText("*");
        }
    }
    
    @FXML
    private void openNewFile() throws IOException {
        this.fileHelper.setFile(null);
        this.setTitle();
        this.codeText.replaceText("");
        this.saveFile();
    }

    @FXML
    private void saveFile() throws IOException {
        this.fileHelper.saveContent(codeText);
        this.setTitle();
    }
    
    @FXML
    private void saveFileAs() throws IOException {
        this.fileHelper.setFile(null);
        this.saveFile();
    }
    
    @FXML
    private void openFile() throws IOException {
        this.fileHelper.openFile();
        if(this.fileHelper.getFile() != null){
            this.fileHelper.writeContent(codeText);
        }
        this.setTitle();
    }
    
    @FXML
    private void undo() throws IOException {
        this.codeText.undo();
    }
    
    @FXML
    private void redo() throws IOException {
        this.codeText.redo();
    }
    
    @FXML
    private void run() throws IOException {
        
    }
}