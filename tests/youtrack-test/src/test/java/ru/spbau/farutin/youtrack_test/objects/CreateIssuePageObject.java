package ru.spbau.farutin.youtrack_test.objects;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import ru.spbau.farutin.youtrack_test.elements.ButtonPageElement;
import ru.spbau.farutin.youtrack_test.elements.TextPageElement;

public class CreateIssuePageObject {
    private TextPageElement summaryText;
    private TextPageElement descriptionText;
    private ButtonPageElement createIssueButton;

    public CreateIssuePageObject(WebDriver webDriver) {
        summaryText = new TextPageElement(webDriver, By.id("id_l.I.ni.ei.eit.summary"));
        descriptionText = new TextPageElement(webDriver, By.id("id_l.I.ni.ei.eit.description"));
        createIssueButton = new ButtonPageElement(webDriver, By.id("id_l.I.ni.ei.submitButton_74_0"));
    }

    public void writeSummary(String summary) {
        summaryText.write(summary);
    }

    public void writeDescription(String description) {
        descriptionText.write(description);
    }

    public void clickCreateIssue() {
        createIssueButton.click();
    }
}
