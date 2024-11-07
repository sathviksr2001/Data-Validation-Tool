import java.awt.*;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.regex.Matcher;
import java.util.regex.Pattern;
import javax.swing.*;

public class DataValidator {
    private final HashMap<String, Pattern> validationRules;
    private final ArrayList<String> validationErrors;

    public DataValidator() {
        validationRules = new HashMap<>();
        validationErrors = new ArrayList<>();
        initializeDefaultRules();
    }

    private void initializeDefaultRules() {
        validationRules.put("email", Pattern.compile("^[A-Za-z0-9+_.-]+@(.+)$"));
        validationRules.put("phone", Pattern.compile("^\\d{10}$"));
        validationRules.put("date", Pattern.compile("^\\d{4}-\\d{2}-\\d{2}$"));
        validationRules.put("creditCard", Pattern.compile("^\\d{16}$"));
    }

    public void addValidationRule(String ruleName, String pattern) {
        validationRules.put(ruleName, Pattern.compile(pattern));
    }

    public boolean validate(String data, String ruleType) {
        Pattern pattern = validationRules.get(ruleType);
        if (pattern == null) {
            validationErrors.add("Validation rule not found: " + ruleType);
            return false;
        }

        Matcher matcher = pattern.matcher(data);
        if (!matcher.matches()) {
            validationErrors.add("Data validation failed for rule: " + ruleType);
            return false;
        }
        return true;
    }

    public boolean validateNumericRange(double value, double min, double max) {
        if (value < min || value > max) {
            validationErrors.add("Value " + value + " is outside range [" + min + ", " + max + "]");
            return false;
        }
        return true;
    }

    public void clearErrors() {
        validationErrors.clear();
    }

    public ArrayList<String> getValidationErrors() {
        return new ArrayList<>(validationErrors);
    }

    public boolean checkDataConsistency(String value1, String value2, String consistencyType) {
        boolean result = switch (consistencyType) {
            case "equality" -> value1.equals(value2);
            case "numeric" -> {
                try {
                    double num1 = Double.parseDouble(value1);
                    double num2 = Double.parseDouble(value2);
                    yield num1 == num2;
                } catch (NumberFormatException e) {
                    validationErrors.add("Invalid numeric values for consistency check");
                    yield false;
                }
            }
            default -> {
                validationErrors.add("Unknown consistency check type: " + consistencyType);
                yield false;
            }
        };
        return result;
    }

    public static void createAndShowGUI() {
        JFrame frame = new JFrame("Data Validator");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(500, 400);
        frame.setLayout(new BorderLayout());

        // Create tabs for different validation types
        JTabbedPane tabbedPane = new JTabbedPane();
        
        // Email Validation Panel
        JPanel emailPanel = createEmailPanel();
        tabbedPane.addTab("Email Validation", emailPanel);
        
        // Phone Validation Panel
        JPanel phonePanel = createPhonePanel();
        tabbedPane.addTab("Phone Validation", phonePanel);
        
        // Numeric Range Panel
        JPanel rangePanel = createRangePanel();
        tabbedPane.addTab("Numeric Range", rangePanel);
        
        // Data Consistency Panel
        JPanel consistencyPanel = createConsistencyPanel();
        tabbedPane.addTab("Data Consistency", consistencyPanel);

        // Error Display Panel
        JPanel errorPanel = createErrorPanel();
        tabbedPane.addTab("Validation Errors", errorPanel);

        frame.add(tabbedPane, BorderLayout.CENTER);
        frame.setVisible(true);
    }
}
