package com.uaa.idejavafx.controllers;

import com.uaa.classes.FileHelper;
import java.io.IOException;
import java.net.URL;
import java.util.Arrays;
import java.util.ResourceBundle;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Label;
import javafx.scene.control.Tab;
import org.fxmisc.richtext.*;
import org.fxmisc.richtext.model.TwoDimensional;

public class PrimaryController implements Initializable {
    @FXML
    private CodeArea codeText;
    @FXML
    private Tab tabTitle;
    @FXML
    private Label rowLabel;
    @FXML
    private Label colLabel;
    @FXML
    private Label totRows;
    @FXML
    private Label totCols;
    @FXML
    private Label infoLabel;
    
    private final FileHelper fileHelper = new FileHelper();
    
    @Override
    public void initialize(URL url, ResourceBundle rb) {
        this.codeText.setParagraphGraphicFactory(LineNumberFactory.get(this.codeText));
    }
    
    private void setTitle(){
        if(this.fileHelper.getFile() != null){
            this.tabTitle.setText(this.fileHelper.getFile().getName());
        } else{
            this.tabTitle.setText("*");
        }
    }
    
    private void showCoords() {
        TwoDimensional.Position pos = this.codeText.offsetToPosition(this.codeText.getCaretPosition(), TwoDimensional.Bias.Forward);

        this.rowLabel.setText("Ln: " + (pos.getMajor() + 1));
        this.colLabel.setText("Col: " + (pos.getMinor() + 1));
    }
    
    private void showTotal() {
        String [] rows = this.codeText.getText().split("\n");
        int cols = Arrays.asList(rows).stream().map(String::length).max(Integer::compareTo).get();

        this.totRows.setText("Lineas: " + rows.length);
        this.totCols.setText("Columnas: " + cols);
    }
    
    @FXML
    private void openNewFile() throws IOException {
        this.fileHelper.setFile(null);
        this.setTitle();
        this.codeText.replaceText("");
        this.saveFile();
        this.showCoords();
    }

    @FXML
    private void saveFile() throws IOException {
        this.fileHelper.saveContent(codeText);
        this.setTitle();
        if(this.fileHelper.getFile() != null){
            this.infoLabel.setText("\tArchivo guardado con éxito");
        }
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
        this.showCoords();
    }
    
    @FXML
    private void undo() throws IOException {
        this.codeText.undo();
        this.showCoords();
    }
    
    @FXML
    private void redo() throws IOException {
        this.codeText.redo();
        this.showCoords();
    }
    
    @FXML
    private void run() throws IOException {
        
    }
    
    @FXML
    private void getCaretPosition() {
        this.showCoords();
        this.showTotal();
    }
}