module com.uaa.idejavafx {
    requires javafx.controls;
    requires javafx.fxml;

    opens com.uaa.idejavafx to javafx.fxml;
    exports com.uaa.idejavafx;
    requires org.fxmisc.richtext;
    requires reactfx;
}