package com.uaa.idejavafx.controllers;

import com.google.gson.*;
import com.uaa.classes.*;
import com.uaa.idejavafx.Main;
import java.io.*;
import static java.lang.Character.isDigit;
import java.net.URL;
import java.nio.file.*;
import java.time.*;
import java.util.*;
import java.util.concurrent.*;
import java.util.function.*;
import java.util.regex.*;
import javafx.concurrent.*;
import javafx.fxml.*;
import javafx.geometry.*;
import javafx.scene.Node;
import javafx.scene.control.*;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.control.ScrollPane.ScrollBarPolicy;
import javafx.scene.layout.*;
import org.fxmisc.flowless.VirtualizedScrollPane;
import org.fxmisc.richtext.*;
import org.fxmisc.richtext.model.*;
import org.reactfx.Subscription;

public class PrimaryController implements Initializable {
    @FXML
    private CodeArea codeText, outputArea, errorArea, lexicalArea;
    @FXML
    private TreeView<String> syntacticTree, semanticTree;
    @FXML
    private Tab tabTitle, outputTab, errorTab, lexicalTab, syntacticTab, semanticTab;
    @FXML
    private Label currentLabel, totalLabel, infoLabel;
    @FXML
    private Button lexicalButton;
    @FXML
    private TabPane statusTabPane, compilerTabPane;
    @FXML
    private AnchorPane pane;
    @FXML
    private TableView symtab;
    
    private final FileHelper fileHelper = new FileHelper();
    
    private ExecutorService executor;
    
    private static final String[] KEYWORDS = new String[] {
            "main", "if", "then", "else", "end", "do", "while", "until", "cin", "cout", "real", "int", "boolean"
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
        this.initLineNumberFactory(new ArrayList<>());
        this.setScrollPane(this.lexicalArea, (AnchorPane) this.lexicalArea.getParent(), ScrollBarPolicy.AS_NEEDED, ScrollBarPolicy.NEVER);
        this.setScrollPane(this.codeText, (AnchorPane) this.codeText.getParent(), ScrollBarPolicy.ALWAYS, ScrollBarPolicy.ALWAYS);
        this.setScrollPane(this.outputArea, (AnchorPane) this.outputArea.getParent(), ScrollBarPolicy.AS_NEEDED, ScrollBarPolicy.NEVER);
        this.setScrollPane(this.errorArea, (AnchorPane) this.errorArea.getParent(), ScrollBarPolicy.AS_NEEDED, ScrollBarPolicy.NEVER);
        
        
        symtab.getColumns().clear();
        TableColumn<HashItem, String> varNameColumn = new TableColumn<>("Name");
        varNameColumn.setCellValueFactory(new PropertyValueFactory<>("varName"));

        TableColumn<HashItem, String> typeColumn = new TableColumn<>("Type");
        typeColumn.setCellValueFactory(new PropertyValueFactory<>("type"));
        
        TableColumn<HashItem, Integer> registerColumn = new TableColumn<>("# Register");
        registerColumn.setCellValueFactory(new PropertyValueFactory<>("register"));
        
        TableColumn<HashItem, ArrayList<String>> linesColumn = new TableColumn<>("Lines");
        linesColumn.setCellValueFactory(new PropertyValueFactory<>("lines"));
       
        varNameColumn.prefWidthProperty().bind(symtab.widthProperty().multiply(0.2));
        typeColumn.prefWidthProperty().bind(symtab.widthProperty().multiply(0.2));    
        registerColumn.prefWidthProperty().bind(symtab.widthProperty().multiply(0.2));
        linesColumn.prefWidthProperty().bind(symtab.widthProperty().multiply(0.4));   
        
        symtab.getColumns().add(varNameColumn);
        symtab.getColumns().add(typeColumn);
        symtab.getColumns().add(registerColumn);
        symtab.getColumns().add(linesColumn);
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
    
    private void initLineNumberFactory(List<Integer> errors) {
        IntFunction<Node> number = LineNumberFactory.get(this.codeText);
        IntFunction<Node> dot = new LineError(this.codeText.currentParagraphProperty(), errors);
        IntFunction<Node> lineNumberFactory = line -> {
            HBox hbox = new HBox(
                number.apply(line),
                dot.apply(line));
            hbox.setAlignment(Pos.CENTER);
            return hbox;
        };
        
        this.codeText.setParagraphGraphicFactory(lineNumberFactory);
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
    private void openNewFile() {
        this.fileHelper.setFile(null);
        this.setTitle();
        this.codeText.replaceText("");
        this.saveFile();
        this.showCoords();
    }

    @FXML
    private void saveFile() {
        this.fileHelper.saveContent(codeText);
        this.setTitle();
        if(this.fileHelper.getFile() != null){
            this.infoLabel.setText("\tArchivo guardado con éxito");
        }
        this.initLineNumberFactory(new ArrayList<>());
    }
    
    @FXML
    private void saveFileAs() {
        this.fileHelper.setFile(null);
        this.saveFile();
        this.initLineNumberFactory(new ArrayList<>());
    }
    
    @FXML
    private void openFile() {
        this.fileHelper.openFile();
        if(this.fileHelper.getFile() != null){
            this.fileHelper.writeContent(codeText);
        }
        this.setTitle();
        this.showCoords();
    }
    
    @FXML
    private void undo() {
        this.codeText.undo();
        this.showCoords();
    }
    
    @FXML
    private void redo() {
        this.codeText.redo();
        this.showCoords();
    }
    
    @FXML
    private void run() {
        
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
    
    private boolean compilationErrors() {
        return !errorArea.getText().equals("");
    }
    
    private void cannotCompile(String unable, String cause){
        this.errorArea.appendText("Cannot compile "+unable+", "+cause+ " errors\n"); 
    }
    
    private void lexOutput(){
        SingleSelectionModel<Tab> selectionModel = statusTabPane.getSelectionModel();
        selectionModel.select(outputTab);
        String s, output = "", errors = "", lastLine = "";
        List<Integer> lineErrors = new ArrayList<>();
        Path lexo = Paths.get(this.fileHelper.getFile().getParent() + "/compilador/lexical.o").toAbsolutePath();
        try (Scanner scanner = new Scanner(lexo).useDelimiter("\n")) {
            while (scanner.hasNext()) {
                s = scanner.next();
                if (s.contains("ERROR")) {
                    Integer l = Integer.parseInt(lastLine.split(" ")[0]);
                    Integer c = Integer.parseInt(lastLine.split(" ")[1]);
                    errors += s.replace(">", "\"").replace("<ERROR: ", ">>>Error with \"") + " line: " + l + " col: " + c + "\n";
                    lineErrors.add(l - 1);
                } else if (s.contains("<")) {
                    output += lastLine + "\n" + s + "\n";
                }
                lastLine = s;
            }
        } catch (IOException ex) { }

        if (!errors.isEmpty()) {
            selectionModel.select(errorTab);
        } else {
            selectionModel.select(outputTab);
            outputArea.appendText("\nbuild: ok");
        }
        errorArea.appendText(errors);
        lexicalArea.replaceText(output);        
        this.initLineNumberFactory(lineErrors);
    }
    
    private static boolean isInt(String strNum) {
        if (strNum == null) {
            return false;
        }
        try {
            int d = Integer.parseInt(strNum);
        } catch (NumberFormatException nfe) {
            return false;
        }
        return true;
    }
    
    private void getOutput(String ofile, TreeView<String> treeView, String tree){
        SingleSelectionModel<Tab> selectionModel = statusTabPane.getSelectionModel();
        selectionModel.select(outputTab);
        String s, errors = "";
        List<Integer> lineErrors = new ArrayList<>();
        Path syntaxo = Paths.get(this.fileHelper.getFile().getParent() + "/compilador/"+ofile).toAbsolutePath();
        try (Scanner scanner = new Scanner(syntaxo).useDelimiter("\n")) {
            while (scanner.hasNext()) {
                s = scanner.next();
                errors += s + "\n";
                String line = "";
                int i = 0;
                while(i < s.length() && !isDigit(s.charAt(i))) i++;
                while(i < s.length() && isDigit(s.charAt(i))){
                    line += s.charAt(i);
                    i++;
                }
                if(isInt(line)){
                    lineErrors.add(Integer.parseInt(line) - 1);
                }
                
            }
        } catch (IOException ex) { }
        if (!errors.isEmpty()) {
            selectionModel.select(errorTab);
        } else {
            selectionModel.select(outputTab);
            outputArea.appendText("\nbuild: ok");
        }
        if(tree != null){
            JsonParser parser = new JsonParser();
            try {
                JsonElement json = parser.parse(new FileReader(this.fileHelper.getFile().getParent() + "/compilador/"+tree));
                treeView.setRoot(createTree(json, null));
            } catch(FileNotFoundException ex) {}
        }
        errorArea.appendText(errors);
        this.initLineNumberFactory(lineErrors);
    }
    
    private void populateHashTable() {
        JsonParser parser = new JsonParser();
        try {
            JsonElement json = parser.parse(new FileReader(this.fileHelper.getFile().getParent() + "/compilador/symtab.json"));
            JsonObject table = json.getAsJsonObject().getAsJsonObject("vars");
            int i = 1;
            for(Map.Entry<String, JsonElement> entry : table.entrySet()){
                String varName = entry.getKey();
                JsonObject vals = entry.getValue().getAsJsonObject();
                String type = vals.get("type").getAsString();
                ArrayList<Integer> lines = new ArrayList<>();
                JsonArray arrLines = vals.get("lines").getAsJsonArray();
                for(int j=0;j<arrLines.size();j++) {
                    Integer l = arrLines.get(j).getAsInt();
                    lines.add(l);
                }
                this.symtab.getItems().add(new HashItem(varName, type, i++,lines ));
            }
        } catch(FileNotFoundException ex) {}
    }

    private TreeItem<String> createTree(JsonElement element, TreeItem<String> parent) {
        if (element.isJsonNull())
            // Empty
            return new TreeItem<String>("Null");
        
        else if (element.isJsonPrimitive()) {
            // Get property
            JsonPrimitive property = element.getAsJsonPrimitive();
            String value = property.getAsString();
            String parts [] = value.split("->");

            // Create item
            return new TreeItem<String>((parts.length > 1) ? parts[1] : value);
        }
        else if (element.isJsonArray()) {
            // Get json array
            JsonArray children = element.getAsJsonArray();

            // Iterate over object childs
            for (JsonElement child : children)
                // Add child to parent
                parent.getChildren().add(createTree(child, null));

            return null;
        }
        else {
            // Get json object
            JsonObject object = element.getAsJsonObject();
            TreeItem<String> item = null;

            // Map properties
            for (Map.Entry<String, JsonElement> property : object.entrySet()) {
                // Get property name and doc
                String key = property.getKey();
                JsonElement doc = property.getValue();

                if (doc.isJsonPrimitive())
                    item = createTree(doc, null);
                else {
                    // Get value from data object
                    if (key.equals("sdt") && doc.isJsonObject()) {
                        JsonObject data = doc.getAsJsonObject();
                        item = createTree(data.get("value"), null);
                    }
                    // Create childs
                    else createTree(doc, item);
                }
            }
            item.setExpanded(true);
            return item;
        }
    }
    
    private void python(String command, String params) throws IOException{
        SingleSelectionModel<Tab> selectionModel = statusTabPane.getSelectionModel();
        String errors = "", output = "";
        Process p = Runtime.getRuntime().exec(command + params);
        BufferedReader stdInput = new BufferedReader(new InputStreamReader(p.getInputStream()));
        BufferedReader stdError = new BufferedReader(new InputStreamReader(p.getErrorStream()));
        String s;
        while ((s = stdInput.readLine()) != null) { output = s + "\n"; }
        while ((s = stdError.readLine()) != null) { errors += s + "\n"; }
        if (!errors.isEmpty()) {
            selectionModel.select(errorTab);
        }
        errorArea.appendText(errors);
        outputArea.appendText(output);
        p.destroyForcibly(); stdInput.close(); stdError.close();
    }
    
    private void clean(){
        errorArea.replaceText(""); 
        outputArea.replaceText("");
    }
    
    @FXML
    private boolean runLexical(){
        this.clean();
        this.prepare("Compiling lexical...", "", this.lexicalTab);
        this.lexOutput();
        return true;
    }
    
    @FXML
    private boolean runSyntactic(){
        if(this.runLexical()){
            if(this.compilationErrors()) {
                this.cannotCompile("syntatic", "lexical");
                return false;
            }
            this.prepare("\nCompiling syntactic...", "-p", this.syntacticTab);
            this.getOutput("syntactic.o", this.syntacticTree, "tree.json");
            return true;
        }
        return false;
    }
    
    @FXML
    private boolean runSemantic(){
        if(this.runSyntactic()){
            if(this.compilationErrors()) {
                this.cannotCompile("semantic", "syntatic");
                return false;
            }
            this.prepare("\nCompiling semantic...", "-p -a", this.semanticTab);
            this.getOutput("semantic.o", this.semanticTree, null);
            this.populateHashTable();
            return true;
        }
        return false;
    }
    
    private void prepare(String message, String extraParams, Tab tab){
        SingleSelectionModel<Tab> compilerModel = compilerTabPane.getSelectionModel();
        compilerModel.select(tab);
        SingleSelectionModel<Tab> statusModel = statusTabPane.getSelectionModel();
        this.fileHelper.saveContent(codeText);
        if(this.fileHelper.getFile()== null){
            statusModel.select(errorTab);
            errorArea.replaceText("Archivo no seleccionado");
        } else {
            try {
                statusModel.select(outputTab);
                outputArea.appendText(message + "\n");
                String dir = this.fileHelper.getFile().getParent(), name = this.fileHelper.getFile().getName();
                if (Main.compilerDir == null) Main.setCompilerDir();
                String command = Main.python+Main.compilerDir+"/main.py", params = " -d"+dir+" -f"+name+ " " + extraParams;
                this.python(command, params);
            } catch (IOException ex) {
                errorArea.appendText("\n"+ex.getMessage());
            }
        }
    }
}