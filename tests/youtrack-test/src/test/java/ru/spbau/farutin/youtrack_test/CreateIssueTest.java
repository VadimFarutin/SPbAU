package ru.spbau.farutin.youtrack_test;

import org.junit.After;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.openqa.selenium.By;
import org.openqa.selenium.StaleElementReferenceException;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import org.openqa.selenium.support.ui.ExpectedConditions;
import org.openqa.selenium.support.ui.Wait;
import org.openqa.selenium.support.ui.WebDriverWait;
import ru.spbau.farutin.youtrack_test.elements.ErrorPopupPageElement;
import ru.spbau.farutin.youtrack_test.elements.IssueInfoPageElement;
import ru.spbau.farutin.youtrack_test.objects.CreateIssuePageObject;
import ru.spbau.farutin.youtrack_test.objects.LoginPageObject;
import ru.spbau.farutin.youtrack_test.objects.MainPageObject;

import static org.junit.Assert.*;

public class CreateIssueTest {
    private static final String LOGIN = "root";
    private static final String PASSWORD = "password";
    private static final String DRIVER_NAME = "webdriver.firefox.driver";
    private static final String DRIVER_EXECUTABLE = "geckodriver.exe";

    private WebDriver webDriver;

    @BeforeClass
    public static void init() {
        System.setProperty(DRIVER_NAME, DRIVER_EXECUTABLE);
    }

    @Before
    public void setUp() {
        webDriver = new FirefoxDriver();
        login();
    }

    @After
    public void tearDown() {
        webDriver.quit();
    }

    @Test
    public void testSimple() {
        testSuccess("summary", "description");
    }

    @Test
    public void testEmptySummary() {
        testFail("", "description", "Summary is required");
    }

    @Test
    public void testEmptySummaryEmptyDescription() {
        testFail("", "", "Summary is required");
    }

    private void login() {
        LoginPageObject loginPage = new LoginPageObject(webDriver);
        loginPage.writeLogin(LOGIN);
        loginPage.writePassword(PASSWORD);
        loginPage.clickLogin();
    }

    private void createIssue(String summary, String description) {
        MainPageObject mainPage = new MainPageObject(webDriver);
        CreateIssuePageObject createIssuePage = mainPage.createIssue();
        createIssuePage.writeSummary(summary);
        createIssuePage.writeDescription(description);
        createIssuePage.clickCreateIssue();
    }

    private void testSuccess(String summary, String description) {
        createIssue(summary, description);

        IssueInfoPageElement issueInfo = new IssueInfoPageElement(webDriver);
        assertEquals(summary, issueInfo.getSummary());
        assertEquals(description, issueInfo.getDesciption());
    }

    private void testFail(String summary, String description, String reason) {
        createIssue(summary, description);

        ErrorPopupPageElement errorPopup = new ErrorPopupPageElement(webDriver);
        assertEquals(reason, errorPopup.getError());
    }
}
