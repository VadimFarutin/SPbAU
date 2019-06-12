package ru.spbau.farutin.youtrack_test.objects;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import ru.spbau.farutin.youtrack_test.elements.ButtonPageElement;

public class IssuesPageObject {
    private static final String ISSUES_URL = "http://localhost:8080/issues";

    private WebDriver webDriver;
    private ButtonPageElement createIssueButton;

    public IssuesPageObject(WebDriver webDriver) {
        this.webDriver = webDriver;
        this.webDriver.get(ISSUES_URL);
        createIssueButton = new ButtonPageElement(webDriver, By.xpath("/html/body/div[1]/div[1]/div/a[5]"));
    }

    public CreateIssuePageObject createIssue() {
        createIssueButton.click();
        return new CreateIssuePageObject(webDriver);
    }
}
