package ru.spbau.farutin.youtrack_test.elements;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Wait;
import org.openqa.selenium.support.ui.WebDriverWait;

public class ErrorPopupPageElement {
    private TextPageElement errorText;

    public ErrorPopupPageElement(WebDriver webDriver) {
        Wait<WebDriver> wait = new WebDriverWait(webDriver, 10);
        wait.until(ExpectedConditions.presenceOfElementLocated(By.className("error")));

        errorText = new TextPageElement(webDriver, By.xpath("/html/body/div[5]/table/tbody/tr/td[2]/ul/li[2]"));
    }

    public String getError() {
        return errorText.read();
    }
}
