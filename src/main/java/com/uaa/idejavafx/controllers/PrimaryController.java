package com.uaa.idejavafx.controllers;

import com.uaa.classes.FileHelper;
import com.uaa.idejavafx.Main;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
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
import javafx.scene.control.Button;
import javafx.scene.control.Label;
import javafx.scene.control.ScrollPane;
import javafx.scene.control.ScrollPane.ScrollBarPolicy;
import javafx.scene.control.SingleSelectionModel;
import javafx.scene.control.Tab;
import javafx.scene.control.TabPane;
import javafx.scene.layout.AnchorPane;
import org.fxmisc.flowless.VirtualizedScrollPane;
import org.fxmisc.richtext.*;
import org.fxmisc.richtext.model.StyleSpans;
import org.fxmisc.richtext.model.StyleSpansBuilder;
import org.fxmisc.richtext.model.TwoDimensional;
import org.reactfx.Subscription;

public class PrimaryController implements Initializable {
    @FXML
    private CodeArea codeText, outputArea, errorArea, lexicalArea;
    @FXML
    private Tab tabTitle, outputTab, errorTab;
    @FXML
    private Label currentLabel, totalLabel, infoLabel;
    @FXML
    private Button lexicalButton;
    @FXML
    private TabPane statusTabPane;
    @FXML
    private AnchorPane pane;
    
    private final FileHelper fileHelper = new FileHelper();
    
    private ExecutorService executor;
    
    private static final String[] KEYWORDS = new String[] {
            "main", "if", "then", "else", "end", "do", "while", "cin", "cout", "real", "int", "boolean"
    };

    private static final String KEYWORD_PATTERN = "\\b(" + String.join("|", KEYWORDS) + ")\\b";
    private static final String NUMBER_PATTERN = "[0-9]+";
    private static final String IDENTIFIER_PATTERN = "([a-z]|[A-Z])([a-z]|[A-Z]|[0-9]|_)*";
    private static final String PAREN_PATTERN = "\\(|\\)";
    private static final String BRACE_PATTERN = "\\{|\\}";
    private static final String BRACKET_PATTERN = "\\[|\\]";
    private static final String SEMICOLON_PATTERN = "\\;";
    private static final String COMMENT_PATTERN = "//[^\n]*" + "|" + "/\\*(.|\\R)*?\\*/";
    private static final String OPERATOR_PATTERN = "(\\+|-|\\*|/|%|<=|<|>=|>|==|!=|:=|\\+\\+|--|\\,|\\;)";

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
        
        this.lexicalArea.setEditable(false);
        this.outputArea.setEditable(false); this.outputArea.setWrapText(true);
        this.errorArea.setEditable(false); this.errorArea.setWrapText(true);
        this.setScrollPane(this.lexicalArea, (AnchorPane) this.lexicalArea.getParent(), ScrollBarPolicy.AS_NEEDED, ScrollBarPolicy.NEVER);
        this.setScrollPane(this.codeText, (AnchorPane) this.codeText.getParent(), ScrollBarPolicy.ALWAYS, ScrollBarPolicy.ALWAYS);
        this.setScrollPane(this.outputArea, (AnchorPane) this.outputArea.getParent(), ScrollBarPolicy.AS_NEEDED, ScrollBarPolicy.NEVER);
        this.setScrollPane(this.errorArea, (AnchorPane) this.errorArea.getParent(), ScrollBarPolicy.AS_NEEDED, ScrollBarPolicy.NEVER);
    }
    
    private void setScrollPane(CodeArea area, AnchorPane pane, ScrollBarPolicy vBar, ScrollBarPolicy hBar){
        VirtualizedScrollPane sp = new VirtualizedScrollPane(area);
        sp.setVbarPolicy(vBar); sp.setHbarPolicy(hBar);
        pane.getChildren().add(sp);
        AnchorPane.setLeftAnchor(sp, 0.0);
        AnchorPane.setRightAnchor(sp, 0.0);
        AnchorPane.setBottomAnchor(sp, 0.0);
        AnchorPane.setTopAnchor(sp, 0.0);
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
        Optional<Integer> opMax = Arrays.asList(rows)
                .stream()
                .map(String::length)
                .max(Integer::compareTo);
        int cols = (opMax.isPresent()) ? opMax.get() : 0;
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
    
    @FXML
    private void selectCompiler() {
        Main.setCompilerDir();
    }
    
    @FXML
    private void runLexical(){
        SingleSelectionModel<Tab> selectionModel = statusTabPane.getSelectionModel();
        Process p = null;
        BufferedReader stdInput = null, stdError = null;
        this.fileHelper.saveContent(codeText);
        if(this.fileHelper.getFile()== null){
            selectionModel.select(errorTab);
            errorArea.replaceText("Archivo no seleccionado");
        } else {
            try {
                selectionModel.select(outputTab);
                outputArea.replaceText("Compilando léxico...\n");
                String dir = this.fileHelper.getFile().getParent(), name = this.fileHelper.getFile().getName();
                if (Main.compilerDir == null) {
                    Main.setCompilerDir();
                }
                String command = Main.python+Main.compilerDir+"\\lexic\\__init__.py", params = " -d"+dir+" -f"+name+" -t yes";
                p = Runtime.getRuntime().exec(command + params);
                stdInput = new BufferedReader(new InputStreamReader(p.getInputStream()));
                stdError = new BufferedReader(new InputStreamReader(p.getErrorStream()));
                String s, output = " ", errors = "";
                String lastLine = "";
                while ((s = stdInput.readLine()) != null) {
                    output += s + "\n";
                    if(s.contains("ERROR")){
                        errors += s + " line: " + lastLine + "\n";
                    }
                    lastLine = s;
                }
                while ((s = stdError.readLine()) != null) {
                    errors += s + "\n";
                }
                if(!errors.isEmpty()){
                    selectionModel.select(errorTab);
                } else {
                    selectionModel.select(outputTab);
                    outputArea.replaceText("build: ok");
                }
                errorArea.replaceText(errors);
                lexicalArea.replaceText(output);
            } catch (IOException ex) {
                errorArea.appendText("\n"+ex.getMessage());
            } finally{
                try {
                    if(p != null) p.destroyForcibly();
                    if(stdInput!=null) stdInput.close();
                    if(stdError != null) stdError.close();
                } catch (IOException ex) {
                    ex.printStackTrace();
                }
            }
        }
    }
}