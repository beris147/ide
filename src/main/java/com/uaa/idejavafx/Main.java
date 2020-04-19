/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.uaa.idejavafx;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Scanner;
import javafx.stage.DirectoryChooser;

/**
 *
 * @author beris
 */
public class Main {
    
    private static final String OS = System.getProperty("os.name").toLowerCase();
    public static String compilerDir = null;
    public static Path confPath = null;
    public static String python = null;

    public static boolean isWindows() {
        return (OS.contains("win"));
    }

    public static void init() {
        python = (isWindows()) ? "python " : "python3 ";
        confPath = Paths.get("./resources/.conf").toAbsolutePath();
        try ( Scanner scanner = new Scanner(confPath).useDelimiter("\n")) {
            while (scanner.hasNext()) {
                String line = scanner.next();
                if (line.contains("compiler=")) {
                    compilerDir = line
                            .replace("compiler=", "")
                            .replace("\n", "")
                            .replace("\r", "");
                }
            }
        } catch (IOException ex) {
            ex.printStackTrace();
        }
    }
    
    public static void setCompilerDir() {
        DirectoryChooser chooser = new DirectoryChooser();
        chooser.setTitle("Selecciona la carpeta del compilador");
        File selectedDirectory = chooser.showDialog(null);
        try ( FileWriter fw = new FileWriter(Main.confPath.toString(), true);  
                BufferedWriter bw = new BufferedWriter(fw);  
                PrintWriter pw = new PrintWriter(bw);) {
            Main.compilerDir = selectedDirectory.getAbsolutePath();
            pw.println("compiler=" + Main.compilerDir);
        } catch (IOException i) {
            i.printStackTrace();
        }
    }

    public static void main(String[] args) {
        init();
        App.mymain(args);
    }
}
