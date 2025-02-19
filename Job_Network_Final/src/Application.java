import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

import org.bson.Document;

import com.mongodb.client.MongoCursor;
import com.mongodb.client.model.Filters;

public class Application {

    public void homePage() {
        Application app = new Application();
        System.out.println("Welcome to the Job Application Network\n");

        boolean flag = true;

        Scanner input = new Scanner(System.in);

        while (flag) {
            System.out.println("Please select one of the following options by entering the corresponding number and pressing enter");
            System.out.println("1: Create New Profile");
            System.out.println("2: Load Existing Profile");
            System.out.println("3: Exit");

            try {
                int option = input.nextInt();
                input.nextLine();

                if (option == 1) {
                    app.createProfile(input);
                } else if (option == 2) {
                    app.loadProfile(input);
                } else  if (option == 3) {
                    flag = false;
                } else {
                    System.out.println("Invalid option\n");
                }
            } catch (Exception e) {
                input.nextLine();
                System.out.println("Invalid input\n");
            }
        }

        input.close();
    }

    // Method to create a profile either job or applicant
    public void createProfile(Scanner input) {
        System.out.println("Please input what type of profile you would like to create");

        System.out.println("1: Create Applicant Profile");
        System.out.println("2: Create Job Profile");
        System.out.println("3: Return");

        try {
            int option = input.nextInt();
            input.nextLine();

            if (option == 1) {
                createApplicantProfile(input);
            } else if (option == 2) {
                createJobProfile(input);
            } else  if (option == 3) {
                return;
            } else {
                System.out.println("Invalid input");
                createProfile(input);
            }
        } catch (Exception e) {
            System.out.println("Invalid input");
            createProfile(input);
        }

        return;
    }

    public UserProfile createApplicantProfile(Scanner input) {
        System.out.println("Please input your name and press enter:");

        String name = input.nextLine();

        while (name.length() <= 0) {
            System.out.println("\nInvalid input. Please enter a name:");
            name = input.nextLine();
        }

        // System.out.println("Please input the associated password");
        // String password = input.nextLine();

        System.out.println("Now input your age:");
        int age = 0;
        while (true) {
            try {
                age = input.nextInt();
                input.nextLine();

                if (age < 0) {
                    System.out.println("\nInvalid input. Please enter a positive integer:");
                } else {
                    break;
                }
            } catch (Exception e){
                input.nextLine();
                System.out.println("\nInvalid input. Please enter a positive integer:");
            }
        }

        System.out.println("Now input your gender:");
        String gender = input.nextLine();

        while (gender.length() <= 0) {
            System.out.println("\nInvalid input. Please enter a gender:");
            gender = input.nextLine();
        }

        System.out.println("Now input the skills associated with the position separated by commas:");
        String skillString = input.nextLine();

        while (skillString.length() <= 0) {
            System.out.println("\nInvalid input. Please enter at least one skill:");
            skillString = input.nextLine();
        }

        String[] skills = skillString.replaceAll(" ", "").split(",");

        System.out.println("Now input your experience in years:");
        int experience = 0;
        while (true) {
            try {
                experience = input.nextInt();
                input.nextLine();

                if (experience < 0) {
                    System.out.println("\nInvalid input. Please enter a positive integer:");
                } else {
                    break;
                }
            } catch (Exception e){
                input.nextLine();
                System.out.println("\nInvalid input. Please enter a positive integer:");
            }
        }

        System.out.println("Now input your target job salary:");
        int salary = 0;
        
        while (true) {
            try {
                salary = input.nextInt();
                input.nextLine();

                if (salary < 0) {
                    System.out.println("\nInvalid input. Please enter a positive integer:");
                } else {
                    break;
                }
            } catch (Exception e){
                input.nextLine();
                System.out.println("\nInvalid input. Please enter a positive integer:");
            }
        }

        System.out.println("Now input your ideal job location:");
        String location = input.nextLine();

        while (location.length() <= 0) {
            System.out.println("\nInvalid input. Please enter a valid city:");
            location = input.nextLine();
        }

        System.out.println("Finally input the ideal job field:");
        String type = input.nextLine();

        while (type.length() <= 0) {
            System.out.println("\nInvalid input. Please enter a valid field:");
            type = input.nextLine();
        }

        UserProfile applicant = new UserProfile(name, age, gender, skills, experience, salary, location, type);

        applicant.save();

        return applicant;
    }

    public JobPosting createJobProfile(Scanner input) {
        System.out.println("Please input the job title and press enter:");

        String title = input.nextLine();

        while (title.length() <= 0) {
            System.out.println("\nInvalid input. Please enter a valid title:");
            title = input.nextLine();
        }

        // System.out.println("Please input the associated password");
        // String password = input.nextLine();

        System.out.println("Now input the job summary:");
        String summary = input.nextLine();

        while (summary.length() <= 0) {
            System.out.println("\nInvalid input. Please enter a valid summary:");
            summary = input.nextLine();
        }

        System.out.println("Now input the job responsibilities:");
        String responsibilities = input.nextLine();

        while (responsibilities.length() <= 0) {
            System.out.println("\nInvalid input. Please enter valid responsibilities:");
            responsibilities = input.nextLine();
        }

        System.out.println("Now input the skills associated with the position separated by commas:");
        String skillString = input.nextLine();

        while (skillString.length() <= 0) {
            System.out.println("\nInvalid input. Please enter at least one skill:");
            skillString = input.nextLine();
        }

        String[] skills = skillString.replaceAll(" ", "").split(",");

        System.out.println("Now input the experience expected:");
        int experience = 0;
        while (true) {
            try {
                experience = input.nextInt();
                input.nextLine();

                if (experience < 0) {
                    System.out.println("\nInvalid input. Please enter a positive integer:");
                } else {
                    break;
                }
            } catch (Exception e){
                input.nextLine();
                System.out.println("\nInvalid input. Please enter a positive integer:");
            }
        }

        System.out.println("Now input the job salary:");
        int salary = 0;
        while (true) {
            try {
                salary = input.nextInt();
                input.nextLine();

                if (salary < 0) {
                    System.out.println("\nInvalid input. Please enter a positive integer:");
                } else {
                    break;
                }
            } catch (Exception e){
                input.nextLine();
                System.out.println("\nInvalid input. Please enter a positive integer:");
            }
        }

        System.out.println("Now input the job location:");
        String location = input.nextLine();

        while (location.length() <= 0) {
            System.out.println("\nInvalid input. Please enter a valid city:");
            location = input.nextLine();
        }

        System.out.println("Finally input the job field:");
        String type = input.nextLine();

        while (type.length() <= 0) {
            System.out.println("\nInvalid input. Please enter a valid field:");
            type = input.nextLine();
        }

        JobPosting job = new JobPosting(title, summary, responsibilities, skills, experience, salary, location, type);

        job.save();

        return job;
    }

    // Method to load a profile to match, edit, or delete
    public void loadProfile(Scanner input) {
        System.out.println("What type of profile would you like to load:");

        while (true) {
            System.out.println("1: Load Applicant Profile");
            System.out.println("2: Load Job Posting");
            System.out.println("3: Return");

            try {
                int option = input.nextInt();
                input.nextLine();

                if (option == 1) {
                    loadApplicantProfile(input);
                    break;
                } else if (option == 2) {
                    loadJobProfile(input);
                    break;
                } else  if (option == 3) {
                    break;
                } else {
                    System.out.println("\nInvalid input. Please enter a valid selection:");
                }
            } catch (Exception e) {
                System.out.println("\nInvalid input. Please enter a valid selection:");
                input.nextLine();
            }
        }

        return;
    }

    public void loadJobProfile(Scanner input) {
        System.out.println("Please input the job title and press enter:");

        String title = input.nextLine();
        DatabaseHandler dbHandler = new DatabaseHandler("JobPostings");
        JobPosting job = new JobPosting();
        try {
            job = new JobPosting(dbHandler.getCollection().find(Filters.eq("title", title)).first());
        } catch (Exception e) {
            System.out.println("Job posting does not exist, please enter a different value\n");
            loadJobProfile(input);
            return;
        }

        System.out.println("Job posting loaded successfully:");

        System.out.println(job);

        System.out.println("Select one of the following profile options:");

        while (true) {
            System.out.println("1: Edit Profile");
            System.out.println("2: Delete Profile");
            System.out.println("3: Find Match");
            System.out.println("4: Return");

            try {
                int option = input.nextInt();
                input.nextLine();

                if (option == 1) {
                    editJobProfile(input, job);
                } else if (option == 2) {
                    System.out.println("Are you sure you want to permanently delete your account?");
                    while (true) {
                        System.out.println("1: Continue");
                        System.out.println("2: Cancel");
                        try {
                            int confirmation = input.nextInt();
                            input.nextLine();

                            if (confirmation == 1) {
                                job.delete(true);
                                break;
                            } else if (confirmation == 2) {
                                System.out.println("Account has not been deleted");
                                break;
                            }
                        } catch (Exception e) {
                            System.out.println("\nInvalid input. Please enter a valid selection:");
                        }
                    }
                    break;
                } else if (option == 3) {
                    UserProfile applicant = bestApplicant(job);
                    System.out.println("\nBest applicant for this job:\n");
                    System.out.println(applicant);
                } else  if (option == 4) {
                    break;
                } else {
                    System.out.println("Invalid input. Please enter a valid selection");
                }
            } catch (Exception e) {
                System.out.println("\nInvalid input. Please enter a valid selection:");
                input.nextLine();
            }
        }

        return;
    }

    public void editJobProfile(Scanner input, JobPosting job) {
        JobPosting oldJob = new JobPosting(job);
        while (true) {
            System.out.println("Which of the following features would you like to update:");
            System.out.println("Title, summary, responsibilities, skills, experience, salary, location, or type");
            System.out.println("\nTo update a specific feature enter the feature name and press enter");
            System.out.println("To save changes and exit input save then press enter");

            String attribute = input.nextLine();

            if (attribute.equalsIgnoreCase("save")) {
                oldJob.delete(false);
                job.save();
                return;
            }

            System.out.println("Please enter the new attribute value(s):");

            String value = input.nextLine();
            
            job.update(attribute, value);
            System.out.println(attribute);
            System.out.println(value);
        }
    }

    public void loadApplicantProfile(Scanner input) {
        System.out.println("Please input your name and press enter:");

        String name = input.nextLine();
        DatabaseHandler dbHandler = new DatabaseHandler("UserProfiles");
        Document data = dbHandler.getCollection().find(Filters.eq("name", name)).first();
        UserProfile user = new UserProfile();
        try {
            user = new UserProfile(data);
        } catch (Exception e) {
            System.out.println("Applicant profile does not exist, please enter a different value\n");
            loadApplicantProfile(input);
            return;
        }

        System.out.println("Applicant profile loaded successfully:");
        System.out.println(user);

        System.out.println("Select one of the following profile options:");

        while (true) {
            System.out.println("1: Edit Profile");
            System.out.println("2: Delete Profile");
            System.out.println("3: Find Match");
            System.out.println("4: Return");
            
            try {
                int option = input.nextInt();
                input.nextLine();

                if (option == 1) {
                    editApplicantProfile(input, user);
                } else if (option == 2) {
                    System.out.println("Are you sure you want to permanently delete your account?");
                    while (true) {
                        System.out.println("1: Continue");
                        System.out.println("2: Cancel");
                        try {
                            int confirmation = input.nextInt();
                            input.nextLine();

                            if (confirmation == 1) {
                                user.delete(true);
                                break;
                            } else if (confirmation == 2) {
                                System.out.println("Account has not been deleted");
                                break;
                            }
                        } catch (Exception e) {
                            System.out.println("\nInvalid input. Please enter a valid selection:");
                        }
                    }
                } else if (option == 3) {
                    JobPosting job = bestJob(user);
                    System.out.println("\nBest job for this applicant:\n");
                    System.out.println(job);
                } else  if (option == 4) {
                    break;
                } else {
                    System.out.println("\nInvalid input. Please enter a valid selection:");
                    input.nextLine();
                }
            } catch (Exception e) {
                System.out.println("\nInvalid input. Please enter a valid selection:");
                input.nextLine();
            }
        }

        return;
    }

    public void editApplicantProfile(Scanner input, UserProfile user) {
        UserProfile oldUser = new UserProfile(user);
        while (true) {
            System.out.println("Which of the following features would you like to update:");
            System.out.println("Name, age, gender, skills, experience, salary, location, or type");
            System.out.println("\nTo update a specific feature enter the feature name and press enter");
            System.out.println("To save changes and exit input save then press enter");

            String attribute = input.nextLine();

            if (attribute.equalsIgnoreCase("save")) {
                oldUser.delete(false);
                user.save();
                return;
            }

            System.out.println("Please enter the new attribute value(s):");

            String value = input.nextLine();
            
            user.update(attribute, value);
        }
    }

    // Method to provide a user with their best match
    public JobPosting bestJob(UserProfile user) {
        List<JobPosting> jobs = loadJobs();
        List<UserProfile> applicants = loadApplicants();

        Matching matches = new Matching(jobs, applicants);

        return matches.getJobMatch(user);
    }

    // Method to provide a user with their best match
    public UserProfile bestApplicant(JobPosting job) {
        List<JobPosting> jobs = loadJobs();
        List<UserProfile> applicants = loadApplicants();

        Matching matches = new Matching(jobs, applicants);

        return matches.getApplicantMatch(job);
    }

    // Method to load all of the existing job entries
    private List<JobPosting> loadJobs() {
        List<JobPosting> jobs = new ArrayList<>();
        DatabaseHandler dbHandler = new DatabaseHandler("JobPostings");

        try (MongoCursor<Document> cursor = dbHandler.getCollection().find().iterator()) {
            while (cursor.hasNext()) {
                jobs.add(new JobPosting(cursor.next()));
            }
        }

        return jobs;
    }

    // Method to load all of the existing applicant profiles
    private List<UserProfile> loadApplicants() {
        List<UserProfile> applicants = new ArrayList<>();
        DatabaseHandler dbHandler = new DatabaseHandler("UserProfiles");

        try (MongoCursor<Document> cursor = dbHandler.getCollection().find().iterator()) {
            while (cursor.hasNext()) {
                applicants.add(new UserProfile(cursor.next()));
            }
        }

        return applicants;
    }

    public static void main(String[] args) {
        Application app = new Application();
        app.homePage();
    }
}
