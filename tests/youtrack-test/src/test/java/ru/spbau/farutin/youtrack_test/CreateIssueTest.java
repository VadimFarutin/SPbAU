package ru.spbau.farutin.youtrack_test;

import org.junit.After;
import org.junit.Before;
import org.junit.BeforeClass;
import org.junit.Test;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.firefox.FirefoxDriver;
import ru.spbau.farutin.youtrack_test.elements.IssueInfoPageElement;
import ru.spbau.farutin.youtrack_test.elements.LastIssuePageElement;
import ru.spbau.farutin.youtrack_test.objects.CreateIssuePageObject;
import ru.spbau.farutin.youtrack_test.objects.IssuesPageObject;
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
    public void test() {
        testCreateIssue("summary", "description");
    }

    private void login() {
        LoginPageObject loginPage = new LoginPageObject(webDriver);
        loginPage.writeLogin(LOGIN);
        loginPage.writePassword(PASSWORD);
        loginPage.clickLogin();
    }

    private void testCreateIssue(String summary, String description) {
        MainPageObject mainPage = new MainPageObject(webDriver);
        CreateIssuePageObject createIssuePage = mainPage.createIssue();
        createIssuePage.writeSummary(summary);
        createIssuePage.writeDescription(description);
        createIssuePage.clickCreateIssue();

        IssueInfoPageElement issueInfo = new IssueInfoPageElement(webDriver);
        assertEquals(summary, issueInfo.getSummary());
        assertEquals(description, issueInfo.getDesciption());
    }
}
