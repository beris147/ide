package com.uaa.idejavafx.controllers;

import com.uaa.classes.FileHelper;
import java.io.IOException;
import java.net.URL;
import java.util.ResourceBundle;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Tab;
import org.fxmisc.richtext.*;
import org.fxmisc.richtext.model.TwoDimensional;

public class PrimaryController implements Initializable {
    @FXML
    private CodeArea codeText;
    @FXML
    private Tab tabTitle;
    
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
    
    @FXML
    private void getCaretPosition() {
        TwoDimensional.Position pos = this.codeText.offsetToPosition(this.codeText.getCaretPosition(), TwoDimensional.Bias.Forward);
        //System.out.println((pos.getMajor() + 1)  + " - "  + (pos.getMinor() + 1));
    }
}