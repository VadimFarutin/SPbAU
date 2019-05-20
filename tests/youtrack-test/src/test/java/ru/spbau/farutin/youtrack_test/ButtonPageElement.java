package ru.spbau.farutin.youtrack_test;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.WebDriverWait;

public class ButtonPageElement {
    private WebElement button;

    public ButtonPageElement(WebDriver webDriver, By by) {
        WebDriverWait wait = new WebDriverWait(webDriver, 10);
        wait.until(ExpectedConditions.visibilityOfElementLocated(by));
        button = webDriver.findElement(by);
    }

    public void click() {
        button.click();
    }
}
