/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package com.uaa.classes;

import java.util.List;
import java.util.function.IntFunction;
import javafx.beans.value.ObservableValue;
import javafx.scene.Node;
import javafx.scene.paint.Color;
import javafx.scene.shape.Circle;
import org.reactfx.value.Val;

/**
 *
 * @author danielmnv
 */
public class LineError implements IntFunction<Node> {
    private final ObservableValue<Integer> line;
    private final List<Integer> errors;

    public LineError(ObservableValue<Integer> line, List<Integer> errors) {
        this.line = line;
        this.errors = errors;
    }

    @Override
    public Node apply(int lineNumber) {
        Circle circle = new Circle(5);
        circle.setFill(Color.RED);

        circle.visibleProperty().bind(Val.map(line, l -> this.errors.contains(lineNumber)).conditionOnShowing(circle));

        return circle;
    }
}
