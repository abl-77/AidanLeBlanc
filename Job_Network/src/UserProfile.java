import java.util.Arrays;
import java.util.List;
import java.util.Scanner;
import com.mongodb.client.model.Filters;

import org.bson.Document;
import org.bson.conversions.Bson;

public class UserProfile {
    
    // Overall details not used for matching
    private String name;
    private int age;
    private String gender;

    // Specific details for matching (Subject to change)
    private String[] skills; // May want to make it so skills are selected from preexisting ones
    private int experience; // How many years of experiece does someone have
    private int salary;
    private String location;
    private String type; // Not sure what a great word for this is, but the "type" of job such as tech or business


    public UserProfile(String name, int age, String gender, String[] skills, int experience, int salary,
            String location, String type) {
        this.name = name;
        this.age = age;
        this.gender = gender;
        this.skills = skills;
        this.experience = experience;
        this.salary = salary;
        this.location = location;
        this.type = type;
    }

    public UserProfile(Document data) {
        this.name = (String) data.get("name");
        this.age = (int) data.get("age");
        this.gender = (String) data.get("gender");
        @SuppressWarnings("unchecked")
        List<String> skillList = (List<String>) data.get("skills");
        Object[] skillArray = skillList.toArray();
        this.skills = new String[skillArray.length];
        for (int i = 0; i < skillArray.length; i++) {
            this.skills[i] = (String) skillArray[i];
        }
        this.experience = (int) data.get("experience");
        this.salary = (int) data.get("salary");
        this.location = (String) data.get("location");
        this.type = (String) data.get("type");
    }


    public UserProfile() {
        name = "";
        age = -1;
        gender = "";
        skills = null;
        experience = -1;
        salary = -1;
        location = "";
        type = "";
    }

    public UserProfile(UserProfile user) {
        this.name = user.name;
        this.age = user.age;
        this.gender = user.gender;
        this.skills = user.skills;
        this.experience = user.experience;
        this.salary = user.salary;
        this.location = user.location;
        this.type = user.type;
    }

    public boolean equals(Object o) {
        if (!(o instanceof UserProfile)) {
            return false;
        }
        UserProfile user = (UserProfile) o;

        for (int i = 0; i < skills.length; i++) {
            if (!(skills[i].equals(user.skills[i]))) {
                return false;
            }
        }

        return name.equals(user.name) && age == user.age && experience == user.experience && 
                salary == user.salary && location.equals(user.location) && type.equals(user.type);
    }

    public String getName() {
        return name;
    }


    public int getAge() {
        return age;
    }


    public String getGender() {
        return gender;
    }


    public String[] getSkills() {
        return skills;
    }


    public int getExperience() {
        return experience;
    }


    public int getSalary() {
        return salary;
    }


    public String getLocation() {
        return location;
    }


    public String getType() {
        return type;
    }


    public void setName(String name) {
        this.name = name;
    }


    public void setAge(int age) {
        this.age = age;
    }


    public void setGender(String gender) {
        this.gender = gender;
    }


    public void setSkills(String[] skills) {
        this.skills = skills;
    }


    public void setExperience(int experience) {
        this.experience = experience;
    }


    public void setSalary(int salary) {
        this.salary = salary;
    }


    public void setLocation(String location) {
        this.location = location;
    }


    public void setType(String type) {
        this.type = type;
    }

    // Populate an existing job posting with new user given values (Overwrites current data)
    public UserProfile promptUser() {
        // Create a Scanner object to get the user's input
        Scanner input = new Scanner(System.in);
        System.out.println("Please input your name and press enter:");

        // Invalid argument checking is not implemented yet
        name = input.nextLine();

        System.out.println("Now input your age in years:");
        age = input.nextInt();
        input.nextLine();

        System.out.println("Now input your gender:");
        gender = input.nextLine();

        System.out.println("Now input the skills that you have separated by commas:");
        String skillString = input.nextLine();

        skills = skillString.replaceAll(" ", "").split(",");

        System.out.println("Now input the experience you have in years:");
        experience = input.nextInt();

        System.out.println("Now input your expected job salary:");
        salary = input.nextInt();
        input.nextLine();

        System.out.println("Now input your preferred job location:");
        location = input.nextLine();

        System.out.println("Finally input the job field of your interest:");
        type = input.nextLine();

        input.close();
        return this;
    }

    // Method to save a new user profile
    // Currently allows for duplicate profiles to be posted
    public void save() {

        DatabaseHandler dbHandler = new DatabaseHandler("UserProfiles");

        try {
            // Convert job posting to a MongoDB document
            Document jobDocument = new Document()
                    .append("location", location)
                    .append("age", age)
                    .append("gender", gender)
                    .append("skills", Arrays.asList(skills))
                    .append("type", type)
                    .append("name", name)
                    .append("experience", experience)
                    .append("salary", salary);

            // Insert the document into the database
            dbHandler.insertDocument(jobDocument);
            System.out.println("User profile saved to database.");
        } catch (Exception e) {
            e.printStackTrace();
            System.err.println("Failed to save user profile to database.");
        }

        dbHandler.closeConnection();
    }

    // Method to delete a user profile
    public void delete(Boolean print) {

        DatabaseHandler dbHandler = new DatabaseHandler("UserProfiles");

        try {
            // Create a filter to find the user profile by title
            Bson filter = Filters.eq("name", name);

            // Attempt to delete the document
            dbHandler.getCollection().deleteOne(filter);
            if (print) System.out.println("User profile with name '" + name + "' deleted from the database.");
        } catch (Exception e) {
            e.printStackTrace();
            if (print) System.err.println("Failed to delete user profile with name '" + name + "'.");
        }
        
        dbHandler.closeConnection();
    }

    public void update(String attribute, String value) {
        switch (attribute.toLowerCase()) {
            case "name":
                this.name = value;
                break;
            case "age":
                try {
                    this.age = Integer.parseInt(value);
                } catch (Exception e) {
                    System.out.println("\nInvalid value to update age. Please enter a positive integer\n");
                }
                break;
            case "gender":
                this.gender = value;
                break;
            case "skills":
                String skillString = value;
                this.skills = skillString.replaceAll(" ", "").split(",");
                break;
            case "experience":
                try {
                    this.experience = Integer.parseInt(value);
                } catch (Exception e) {
                    System.out.println("\nInvalid value to update experince. Please enter a positive integer\n");
                }
                break;
            case "salary":
                try {
                    this.salary = Integer.parseInt(value);
                } catch (Exception e) {
                    System.out.println("\nInvalid value to update salary. Please enter a positive integer\n");
                }
                break;
            case "location":
                this.location = value;
                break;
            case "type":
                this.type = value;
                break;
            default:
                System.out.println("\nInvalid feature selected. Please select one of the existing features to edit.\n");
        }
    }

    public String toString() {
        String str = "\nUser Name: " + name + "\n\n";
        str += "User Age: " + age + "\n\n";
        str += "User Gender: " + gender + "\n\n";
        str += "Skills: ";
        for (String skill: skills) {
            str += skill + ", ";
        }
        str = str.substring(0, str.length() - 2);
        str += "\nYears of Experience: " + experience + "\n";
        str += "Expected Salary: " + salary + "\n";
        str += "User Location: " + location + "\n";
        str += "Job Type: " + type + "\n";

        return str;
    }
}
