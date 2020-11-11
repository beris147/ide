/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.uaa.classes;

import java.util.ArrayList;

/**
 *
 * @author root
 */
public class HashItem {
    String varName;
    String type;
    Integer register;
    ArrayList<Integer> lines;
    String val;

    public HashItem(String varName, String type, int register, ArrayList<Integer> lines, String val) {
        this.varName = varName;
        this.type = type;
        this.register = register;
        this.lines = lines;
        this.val = val;
    }

    public String getVarName() {
        return varName;
    }

    public void setVarName(String varName) {
        this.varName = varName;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public int getRegister() {
        return register;
    }

    public void setRegister(int register) {
        this.register = register;
    }

    public ArrayList<Integer> getLines() {
        return lines;
    }

    public void setLines(ArrayList<Integer> lines) {
        this.lines = lines;
    }

    public String getVal() {
        return val;
    }

    public void setVal(String val) {
        this.val = val;
    }
    
    
}
