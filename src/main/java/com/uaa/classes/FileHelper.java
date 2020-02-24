package com.uaa.classes;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.IOException;
import javafx.stage.FileChooser;
import org.fxmisc.richtext.CodeArea;

/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

/**
 *
 * @author beris
 */
public class FileHelper {
    private final FileChooser fileChooser;
    private File file;

    public FileHelper() {
        this.fileChooser = new FileChooser();
        this.fileChooser.getExtensionFilters().addAll(
            new FileChooser.ExtensionFilter("Text files", "*.txt")
        );
        this.file = null;
    }

    public FileChooser getFileChooser() {
        return fileChooser;
    }

    public File getFile() {
        return file;
    }

    public void setFile(File file) {
        this.file = file;
    }
    
    public void openFile(){
        this.file = this.fileChooser.showOpenDialog(null);
        this.setDirectory();
    }
    
    private void setDirectory(){
         if(this.file != null){
            this.fileChooser.setInitialDirectory(this.file.getParentFile());
        }
    }
    
    public void writeContent(CodeArea codeText){
        codeText.replaceText("");
        if(this.file != null){
            BufferedReader in = null;
            try {
                in = new BufferedReader(new FileReader(this.file));
                String str;
                while ((str = in.readLine()) != null) {
                    codeText.appendText(str);
                    codeText.appendText("\n");
                }
            } catch (IOException e) {
                codeText.replaceText("Archivo no válido");
            } finally {
                try { in.close(); } catch (IOException ex) { }
            }
        } else{
            codeText.replaceText("Archivo no válido");
        }
    }
    
    public void saveContent(CodeArea codeText){
        if(this.file == null){
            this.file = this.fileChooser.showSaveDialog(null);
        }
        if(file != null){   
            Functions.saveFile(codeText.getText(), this.file);
            this.setDirectory();
        }
    }

}
