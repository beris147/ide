package com.uaa.idejavafx.controllers;

import com.uaa.classes.FileHelper;
import java.io.IOException;
import java.net.URL;
import java.time.Duration;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.Optional;
import java.util.ResourceBundle;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import javafx.concurrent.Task;
import javafx.fxml.FXML;
import javafx.fxml.Initializable;
import javafx.scene.control.Label;
import javafx.scene.control.Tab;
import org.fxmisc.richtext.*;
import org.fxmisc.richtext.model.StyleSpans;
import org.fxmisc.richtext.model.StyleSpansBuilder;
import org.fxmisc.richtext.model.TwoDimensional;
import org.reactfx.Subscription;

public class PrimaryController implements Initializable {
    @FXML
    private CodeArea codeText;
    @FXML
    private Tab tabTitle;
    @FXML
    private Label currentLabel;
    @FXML
    private Label totalLabel;
    @FXML
    private Label infoLabel;
    
    private final FileHelper fileHelper = new FileHelper();
    
    private ExecutorService executor;
    
    private static final String[] KEYWORDS = new String[] {
            "main", "if", "then", "else", "end",
            "do", "while", "cin", "cout", "real",
            "int", "boolean"
    };

    private static final String KEYWORD_PATTERN = "\\b(" + String.join("|", KEYWORDS) + ")\\b";
    private static final String NUMBER_PATTERN = "[0-9]+";
    private static final String IDENTIFIER_PATTERN = "([a-z]|[A-Z])([a-z]|[A-Z]|[0-9]|_)*";
    private static final String PAREN_PATTERN = "\\(|\\)";
    private static final String BRACE_PATTERN = "\\{|\\}";
    private static final String BRACKET_PATTERN = "\\[|\\]";
    private static final String SEMICOLON_PATTERN = "\\;";
    private static final String COMMENT_PATTERN = "//[^\n]*" + "|" + "/\\*(.|\\R)*?\\*/";
    private static final String OPERATOR_PATTERN = "(\\+|-|\\*|/|%|<=|<|>=|>|==|!=|:=|\\+\\+|--)";

    private static final Pattern PATTERN = Pattern.compile(
            "(?<KEYWORD>" + KEYWORD_PATTERN + ")"
            + "|(?<NUMBER>" + NUMBER_PATTERN + ")"
            + "|(?<IDENTIFIER>" + IDENTIFIER_PATTERN + ")"
            + "|(?<PAREN>" + PAREN_PATTERN + ")"
            + "|(?<BRACE>" + BRACE_PATTERN + ")"
            + "|(?<BRACKET>" + BRACKET_PATTERN + ")"
            + "|(?<SEMICOLON>" + SEMICOLON_PATTERN + ")"
            + "|(?<COMMENT>" + COMMENT_PATTERN + ")"
            + "|(?<OPERATOR>" + OPERATOR_PATTERN + ")"
    );
    
    @Override
    public void initialize(URL url, ResourceBundle rb) {
        this.executor = Executors.newSingleThreadExecutor();
        
        this.codeText.setParagraphGraphicFactory(LineNumberFactory.get(this.codeText));
        
        Subscription subscription = this.codeText.multiPlainChanges()
            .successionEnds(Duration.ofMillis(1))
            .supplyTask(this::buildHighlight)
            .awaitLatest(this.codeText.multiPlainChanges())
            .filterMap(t -> {
                if(t.isSuccess()) {
                    return Optional.of(t.get());
                } else {
                    return Optional.empty();
                }
            })
            .subscribe(this::applyHighlight);
    }
    
    private Task<StyleSpans<Collection<String>>> buildHighlight() {
        Task<StyleSpans<Collection<String>>> task = new Task<StyleSpans<Collection<String>>>() {
            @Override
            protected StyleSpans<Collection<String>> call() throws Exception {
                return runHighlight(codeText.getText());
            }
        };
        this.executor.execute(task);
        return task;
    }

    private void applyHighlight(StyleSpans<Collection<String>> highlighting) {
        this.codeText.setStyleSpans(0, highlighting);
    }

    private static StyleSpans<Collection<String>> runHighlight(String text) {
        Matcher matcher = PATTERN.matcher(text);
        int lastKey = 0;
        StyleSpansBuilder<Collection<String>> builder = new StyleSpansBuilder<>();
        
        while(matcher.find()) {
            String styleClass =
                    matcher.group("KEYWORD") != null ? "keyword" :
                    matcher.group("NUMBER") != null ? "number" :
                    matcher.group("IDENTIFIER") != null ? "identifier" :
                    matcher.group("PAREN") != null ? "paren" :
                    matcher.group("BRACE") != null ? "brace" :
                    matcher.group("BRACKET") != null ? "bracket" :
                    matcher.group("SEMICOLON") != null ? "semicolon" :
                    matcher.group("COMMENT") != null ? "comment" :
                    matcher.group("OPERATOR") != null ? "operator" :
                    null;
                    assert styleClass != null;
            builder.add(Collections.emptyList(), matcher.start() - lastKey);
            builder.add(Collections.singleton(styleClass), matcher.end() - matcher.start());
            lastKey = matcher.end();
        }
        
        builder.add(Collections.emptyList(), text.length() - lastKey);
        return builder.create();
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

        this.currentLabel.setText("Ln: " + (pos.getMajor() + 1) + ", Col: " + (pos.getMinor() + 1));
    }
    
    private void showTotal() {
        String [] rows = this.codeText.getText().split("\n");
        int cols = Arrays.asList(rows).stream().map(String::length).max(Integer::compareTo).get();

        this.totalLabel.setText("Lineas: " + rows.length + ", Columnas: " + cols);
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