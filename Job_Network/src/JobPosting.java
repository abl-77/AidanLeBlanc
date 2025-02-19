import java.util.Arrays;
import java.util.List;

import com.mongodb.client.model.Filters;

import org.bson.Document;
import org.bson.conversions.Bson;

public class JobPosting {
    // Overall details not used for matching
    private String title;
    private String summary;
    private String responsibilities;

    // Specific details for matching (Subject to change)
    private String[] skills; // May want to make it so skills are selected from preexisting ones
    private int experience; // How many years of experiece does someone have
    private int salary;
    private String location;
    private String type; // Not sure what a great word for this is, but the "type" of job such as tech or business

    public JobPosting() {
        title = "";
        summary = "";
        responsibilities = "";
        skills = null;
        experience = -1;
        salary = -1;
        location = "";
        type = "";
    }
    

    public JobPosting(String title, String summary, String responsibilities, String[] skills, int experience, int salary, String location, String type) {
        this.title = title;
        this.summary = summary;
        this.responsibilities = responsibilities;
        this.skills = skills;
        this.experience = experience;
        this.salary = salary;
        this.location = location;
        this.type = type;
    }

    public JobPosting(String title) {
        this.title = title;
        summary = "";
        responsibilities = "";
        skills = null;
        experience = -1;
        salary = -1;
        location = "";
        type = "";
    }

    public JobPosting(Document data) {
        this.title = (String) data.get("title");
        this.summary = (String) data.get("summary");
        this.responsibilities = (String) data.get("responsibilities");
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

    public JobPosting(JobPosting job) {
        this.title = job.title;
        this.summary = job.summary;
        this.responsibilities = job.responsibilities;
        this.skills = job.skills;
        this.experience = job.experience;
        this.salary = job.salary;
        this.location = job.location;
        this.type = job.type;
    }

    public boolean equals(Object o) {
        if (!(o instanceof JobPosting)) {
            return false;
        }
        JobPosting job = (JobPosting) o;

        for (int i = 0; i < skills.length; i++) {
            if (!(skills[i].equals(job.skills[i]))) {
                return false;
            }
        }

        return title.equals(job.title) && summary.equals(job.summary) && responsibilities.equals(job.responsibilities) && 
                experience == job.experience && salary == job.salary && location.equals(job.location) && type.equals(job.type);
    }

    // Get methods to preserve encapsulation
    public String getTitle() {
        return title;
    }

    public String getSummary() {
        return summary;
    }

    public String getResponsibilities() {
        return responsibilities;
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

    // Set methods to preserve encapsulation
    public void setTitle(String title) {
        this.title = title;
    }

    public void setSummary(String summary) {
        this.summary = summary;
    }

    public void setResponsibilities(String responsibilities) {
        this.responsibilities = responsibilities;
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

    // Method to save a new job posting
    // Currently allows for duplicate jobs to be posted
    public void save() {

        DatabaseHandler dbHandler = new DatabaseHandler("JobPostings");

        try {
            // Convert job posting to a MongoDB document
            Document jobDocument = new Document()
                    .append("summary", summary)
                    .append("skills", Arrays.asList(skills))
                    .append("responsibilities", responsibilities)
                    .append("location", location)
                    .append("title", title)
                    .append("experience", experience)
                    .append("salary", salary)
                    .append("type", type);

            // Insert the document into the database
            dbHandler.insertDocument(jobDocument);
            System.out.println("Job posting saved to database.");
        } catch (Exception e) {
            e.printStackTrace();
            System.err.println("Failed to save job posting to database.");
        }

        dbHandler.closeConnection();
    }
    

    // Method to delete a job posting from the database
    public void delete(Boolean print) {

        DatabaseHandler dbHandler = new DatabaseHandler("JobPostings");

        try {
            // Create a filter to find the job posting by title
            Bson filter = Filters.eq("title", title);

            // Attempt to delete the document
            dbHandler.getCollection().deleteOne(filter);
            if (print) System.out.println("Job posting with title '" + title + "' deleted from the database.");
        } catch (Exception e) {
            e.printStackTrace();
            if (print) System.err.println("Failed to delete job posting with title '" + title + "'.");
        }
        
        dbHandler.closeConnection();
    }

    public void update(String attribute, String value) {
        switch (attribute.toLowerCase()) {
            case "title":
                this.title = value;
                break;
            case "summary":
                this.summary = value;
                break;
            case "responsibilities":
                this.responsibilities = value;
                break;
            case "skills":
                String skillString = value;
                this.skills = skillString.replaceAll(" ", "").split(",");
                break;
            case "experience":
                try {
                    this.experience = Integer.parseInt(value);
                } catch (Exception e) {
                    System.out.println("\nInvalid value to update experience. Please enter a positive integer\n");
                }
                break;
            case "salary":
                try {
                    this.salary = Integer.parseInt(value);
                } catch (Exception e) {
                    System.out.println("\nInvalid value to update experience. Please enter a positive integer\n");
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
        String str = "\nJob Title: " + title + "\n\n";
        str += "Job Summary: " + summary + "\n\n";
        str += "Job Responsibilities: " + responsibilities + "\n\n";
        str += "Required Skills: ";
        for (String skill: skills) {
            str += skill + ", ";
        }
        str = str.substring(0, str.length() - 2);
        str += "\nYears of Experience: " + experience + "\n";
        str += "Expected Salary: " + salary + "\n";
        str += "Job Location: " + location + "\n";
        str += "Job Type: " + type + "\n";

        return str;
    }
}

