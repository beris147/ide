/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.uaa.classes;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

/**
 *
 * @author beris
 */
public class Functions {
    public static void saveFile(String content, File file){
        try {
            FileWriter fileWriter;
            fileWriter = new FileWriter(file);
            fileWriter.write(content);
            fileWriter.close();
        } catch (IOException ex) {
            
        }
    }
}
