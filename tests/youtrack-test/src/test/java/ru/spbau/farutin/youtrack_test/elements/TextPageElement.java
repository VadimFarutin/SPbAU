package ru.spbau.farutin.youtrack_test.elements;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class TextPageElement {
    private WebElement text;

    public TextPageElement(WebDriver webDriver, By by) {
        WebDriverWait wait = new WebDriverWait(webDriver, 10);
        wait.until(ExpectedConditions.visibilityOfElementLocated(by));
        text = webDriver.findElement(by);
    }

    public void write(String content) {
        text.sendKeys(content);
    }

    public String read() {
        return text.getText();
    }
}
