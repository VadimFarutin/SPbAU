package ru.spbau.farutin.youtrack_test.elements;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class IssueInfoPageElement {
    private TextPageElement summaryText;
    private TextPageElement descriptionText;

    public IssueInfoPageElement(WebDriver webDriver) {
        summaryText = new TextPageElement(webDriver, By.id("id_l.I.ic.icr.it.issSum"));
        descriptionText = new TextPageElement(webDriver, By.id("id_l.I.ic.icr.d.description"));
    }

    public String getSummary() {
        return summaryText.read();
    }

    public String getDesciption() {
        return descriptionText.read();
    }
}
