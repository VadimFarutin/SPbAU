package ru.spbau.farutin.youtrack_test.objects;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import ru.spbau.farutin.youtrack_test.elements.ButtonPageElement;
import ru.spbau.farutin.youtrack_test.elements.TextPageElement;

public class LoginPageObject {
    private static final String LOGIN_URL = "http://localhost:8080/login";

    private TextPageElement loginText;
    private TextPageElement passwordText;
    private ButtonPageElement loginButton;

    public LoginPageObject(WebDriver webDriver) {
        webDriver.get(LOGIN_URL);
        loginText = new TextPageElement(webDriver, By.id("id_l.L.login"));
        passwordText = new TextPageElement(webDriver, By.id("id_l.L.password"));
        loginButton = new ButtonPageElement(webDriver, By.id("id_l.L.loginButton"));
    }

    public void writeLogin(String login) {
        loginText.write(login);
    }

    public void writePassword(String password) {
        passwordText.write(password);
    }

    public void clickLogin() {
        loginButton.click();
    }
}
