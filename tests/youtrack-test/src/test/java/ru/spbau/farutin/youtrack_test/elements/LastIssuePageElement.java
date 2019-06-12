package ru.spbau.farutin.youtrack_test.elements;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;

public class LastIssuePageElement {
    private TextPageElement summaryText;
    private TextPageElement descriptionText;

    public LastIssuePageElement(WebDriver webDriver) {
        TextPageElement issuesFound = new TextPageElement(webDriver, By.id("id_l.I.sp.sl.issuesFound"));
        String issuesFoundText = issuesFound.read();
        String[] tokens = issuesFoundText.split(" ");
        int n = Integer.parseInt(tokens[1]);

        ButtonPageElement expandButton = new ButtonPageElement(webDriver, By.xpath(String.format("//*[@id=\"id_l.I.c.il.i_74_%d.vi.collapse\"]", n)));
        expandButton.click();
        summaryText = new TextPageElement(webDriver, By.xpath("/html/body/div[2]/div[2]/div[2]/div/div[3]/div[1]/table/tbody/tr/td[2]/div[2]/a[2]"));
        descriptionText = new TextPageElement(webDriver, By.xpath("/html/body/div[2]/div[2]/div[2]/div/div[3]/div[1]/table/tbody/tr/td[2]/div[2]/div[3]/div"));
    }

    public String getSummary() {
        return summaryText.read();
    }

    public String getDesciption() {
        return descriptionText.read();
    }
}
