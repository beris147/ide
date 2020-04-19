package com.uaa.idejavafx;

import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.IOException;
import javafx.application.Platform;
import javafx.event.EventHandler;
import javafx.stage.WindowEvent;

/**
 * JavaFX App
 */
public class App extends Application {

    private static Scene scene;

    @Override
    public void start(Stage stage) throws IOException {
        Platform.setImplicitExit(true);
        scene = new Scene(loadFXML("primary"), 640, 480);
        stage.setOnCloseRequest((WindowEvent event) -> {
            Platform.exit();
            Thread start = new Thread(() -> {
                System.exit(0);
            });
            start.start();
        });
        stage.setMaximized(true);
        stage.setScene(scene);
        stage.show();
    }

    static void setRoot(String fxml) throws IOException {
        scene.setRoot(loadFXML(fxml));
    }

    private static Parent loadFXML(String fxml) throws IOException {
        FXMLLoader fxmlLoader = new FXMLLoader(App.class.getResource(fxml + ".fxml"));
        return fxmlLoader.load();
    }

    public static void mymain(String[] args) {
        launch(args);
    }

}