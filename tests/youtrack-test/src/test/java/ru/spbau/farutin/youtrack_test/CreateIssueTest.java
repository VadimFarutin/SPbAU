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
        testSuccess("summary", "description", "summary", "description");
    }

    @Test
    public void testSummaryWithSpaces() {
        testSuccess("summary   summary", "description", "summary summary", "description");
    }

    @Test
    public void testSummaryWithFirstSpace() {
        testSuccess(" summary", "description", "summary", "description");
    }

    @Test
    public void testSummaryWithLastSpace() {
        testSuccess("summary ", "description", "summary", "description");
    }

    @Test
    public void testDescriptionWithSpaces() {
        testSuccess("summary", "description   description", "summary", "description   description");
    }

    @Test
    public void testDescriptionWithFirstSpace() {
        testSuccess("summary", " description", "summary", " description");
    }

    @Test
    public void testDescriptionWithLastSpace() {
        testSuccess("summary", "description ", "summary", "description ");
    }

    @Test
    public void testSummaryWithCapitalLetters() {
        testSuccess("SumMarY", "description", "SumMarY", "description");
    }

    @Test
    public void testDescriptionWithCapitalLetters() {
        testSuccess("summary", "DeScriPtioN", "summary", "DeScriPtioN");
    }

    @Test
    public void testSummaryWithDigits() {
        testSuccess("123hello", "description", "123hello", "description");
    }

    @Test
    public void testDescriptionWithDigits() {
        testSuccess("summary", "123hello", "summary", "123hello");
    }

    @Test
    public void testSummaryWithSpecialCharacters() {
        testSuccess("`~!@#$%^&*()_+-=[]{}:;\'\"\\|,<.>/?", "description", "`~!@#$%^&*()_+-=[]{}:;\'\"\\|,<.>/?", "description");
    }

    @Test
    public void testDescriptionWithSpecialCharacters() {
        testSuccess("summary", "`~!@#$%^&*()_+-=[]{}:;\'\"\\|,<.>/?", "summary", "`~!@#$%^&*()_+-=[]{}:;\'\"\\|,<.>/?");
    }

    @Test
    public void testLongSummary() {
        String c = "a";
        String summary = new String(new char[100]).replace("\0", c);
        testSuccess(summary, "description", summary, "description");
    }

    @Test
    public void testLongDescription() {
        String c = "a";
        String description = new String(new char[100]).replace("\0", c);
        testSuccess("summary", description, "summary", description);
    }

    @Test
    public void testExistedSummary() {
        testSuccess("summary", "description", "summary", "description");
        testSuccess("summary", "description1", "summary", "description1");
    }

    @Test
    public void testExistedDescription() {
        testSuccess("summary", "description", "summary", "description");
        testSuccess("summary1", "description", "summary1", "description");
    }

    @Test
    public void testSummaryWithRussianLetters() {
        testSuccess("название", "description", "название", "description");
    }

    @Test
    public void testDescriptionWithRussianLetters() {
        testSuccess("summary", "описание", "summary", "описание");
    }

    @Test
    public void testSummaryWithUnicodeCharacters() {
        testSuccess("∞€£¥©®™αβӦ\u0558ڸ", "description", "∞€£¥©®™αβӦ\u0558ڸ", "description");
    }

    @Test
    public void testDescriptionWithUnicodeCharacters() {
        testSuccess("summary", "∞€£¥©®™αβӦ\u0558ڸ", "summary", "∞€£¥©®™αβӦ\u0558ڸ");
    }

    @Test
    public void testSummaryWithNewLine() {
        testSuccess("a\nb", "description", "ab", "description");
    }

    @Test
    public void testDescriptionWithNewLine() {
        testSuccess("summary", "a\nb", "summary", "a\nb");
    }

    @Test
    public void testEmptyDescription() {
        testSuccess("summary", "", "summary", "No description");
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

    private void testSuccess(String summary, String description, String expectedSummary, String expectedDescription) {
        createIssue(summary, description);

        IssueInfoPageElement issueInfo = new IssueInfoPageElement(webDriver);
        assertEquals(expectedSummary, issueInfo.getSummary());
        assertEquals(expectedDescription, issueInfo.getDesciption());
    }

    private void testFail(String summary, String description, String reason) {
        createIssue(summary, description);

        ErrorPopupPageElement errorPopup = new ErrorPopupPageElement(webDriver);
        assertEquals(reason, errorPopup.getError());
    }
}
