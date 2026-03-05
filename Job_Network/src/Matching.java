import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.LinkedList;
import java.util.List;

public class Matching {
    private List<JobPosting> jobs;
    private List<UserProfile> applicants;
    private HashMap<JobPosting, UserProfile> jobsToApps; // Potentially change to List<UserProfile> to allow options
    private HashMap<UserProfile, JobPosting> appsToJobs;

    public Matching(List<JobPosting> jobs, List<UserProfile> applicants) {
        this.jobs = jobs;
        this.applicants = applicants;
        match();
    }

    public HashMap<JobPosting, UserProfile> getMatches() {
        return jobsToApps;
    }

    private int preference(JobPosting job, UserProfile applicant) {
        int salDif = Math.abs(job.getSalary() - applicant.getSalary());
        salDif = salDif / (salDif + 1);
        int expDif = job.getExperience() - applicant.getExperience();

        int loc = 0;
        if (job.getLocation().equalsIgnoreCase(applicant.getLocation())) {
            loc = 1;
        }

        int skills = 0;

        for (String skill: job.getSkills()) {
            if (Arrays.stream(applicant.getSkills()).anyMatch(appSkill -> appSkill.equalsIgnoreCase(skill))) {
                skills += 1;
            } else {
                skills -= 1;
            }
        }

        int type = -1;
        if (job.getType().equalsIgnoreCase(applicant.getType())) {
            type = 1;
        }

        return 10 * skills + 20 * type + 20 * loc - expDif - salDif;
    }

    public void match() {
        int[][] preferences = new int[jobs.size()][applicants.size()];

        for (int i = 0; i < jobs.size(); i++) {
            for (int j = 0; j < applicants.size(); j++) {
                preferences[i][j] = preference(jobs.get(i), applicants.get(j));
            }
        }

        HashMap<Integer, Integer> indexMatches = new HashMap<>();

        ArrayList<Integer> unmatched = new ArrayList<>();

        for (int i = 0; i < jobs.size(); i++) {
            unmatched.add(i); 
        }

        int current = 0;

        while (indexMatches.size() < jobs.size() && indexMatches.size() < applicants.size()) {

            current = unmatched.remove(0);

            int maxPref = Integer.MIN_VALUE;
            int maxInd = -1;

            for (int j = 0; j < applicants.size(); j++) {
                if (preferences[current][j] > maxPref) {
                    maxPref = preferences[current][j];
                    maxInd = j;
                }
            }

            if (indexMatches.containsKey((maxInd))) {
                int currentPref = preferences[indexMatches.get(maxInd)][maxInd];
                        if (maxPref > currentPref) {
                            unmatched.add(indexMatches.get(maxInd));
                            preferences[indexMatches.get(maxInd)][maxInd] = Integer.MIN_VALUE;
                            indexMatches.replace(maxInd, current);
                        } else {
                            unmatched.add(current);
                            preferences[current][maxInd] = Integer.MIN_VALUE;
                        }
            } else {
                indexMatches.put(maxInd, current);
            }
        }

        jobsToApps = new HashMap<JobPosting, UserProfile>();
        appsToJobs = new HashMap<UserProfile, JobPosting>();

        for (int key: indexMatches.keySet()) {
            jobsToApps.put(jobs.get(key), applicants.get(indexMatches.get(key)));
            appsToJobs.put(applicants.get(indexMatches.get(key)), jobs.get(key));
        }
    }

    public JobPosting getJobMatch(UserProfile applicant) {
        for (UserProfile possibleApp: appsToJobs.keySet()) {
            if (possibleApp.equals(applicant)) {
                return appsToJobs.get(possibleApp);
            }
        }

        return null;
    }

    public UserProfile getApplicantMatch(JobPosting job) {
        for (JobPosting possibleJob: jobsToApps.keySet()) {
            if (possibleJob.equals(job)) {
                return jobsToApps.get(possibleJob);
            }
        }

        return null;
    }

    public void printMatches() {
        for (JobPosting key: jobsToApps.keySet()) {
            System.out.println("Match:");
            System.out.println(key.getTitle());
            System.out.println(jobsToApps.get(key).getName());
            System.out.println();
        }
    }

    public static void main(String[] args) {
        String[] jobSkillsOne = {"java", "python", "leadership", "communication"};
        String[] jobSkillsTwo = {"excel", "finance", "networking", "communication"};
        String[] jobSkillsThree = {"customer service", "time management", "research", "biology"};

        JobPosting jobOne = new JobPosting(
            "First Test Job",
             "This is the first test job",
            "The role of this job is to serve as a test for matching", 
            jobSkillsOne, 
            5, 
            40000, 
            "Cleveland", 
            "Technology"
        );

        JobPosting jobTwo = new JobPosting(
            "Second Test Job",
             "This is the second test job",
            "The role of this job is to serve as a test for matching", 
            jobSkillsTwo, 
            10, 
            50000, 
            "Chicago", 
            "Business"
        );

        JobPosting jobThree = new JobPosting(
            "Third Test Job",
             "This is the third test job",
            "The role of this job is to serve as a test for matching", 
            jobSkillsThree, 
            2, 
            30000, 
            "Boston", 
            "Medicine"
        );

        JobPosting jobFour = new JobPosting(
            "Third Test Job",
             "This is the third test job",
            "The role of this job is to serve as a test for matching", 
            jobSkillsThree, 
            0, 
            50000, 
            "Portland", 
            "Medicine"
        );

        String[] applicantSkillsOne = {"java", "python", "leadership", "communication"};
        String[] applicantSkillsTwo = {"excel", "finance", "networking", "communication"};
        String[] applicantSkillsThree = {"customer service", "time management", "research", "biology"};

        UserProfile applicantOne = new UserProfile(
            "First Test Applicant",
             25,
            "Male", 
            applicantSkillsOne, 
            5, 
            40000, 
            "Cleveland", 
            "Technology"
        );

        UserProfile applicantTwo = new UserProfile(
            "Second Test Applicant",
             32,
            "Female", 
            applicantSkillsTwo, 
            10, 
            50000, 
            "Chicago", 
            "Business"
        );

        UserProfile applicantThree = new UserProfile(
            "Third Test Applicant",
             22,
            "Male", 
            applicantSkillsThree, 
            2, 
            30000, 
            "Boston", 
            "Medicine"
        );

        List<JobPosting> jobs = new LinkedList<>();
        jobs.add(jobOne);
        jobs.add(jobTwo);
        jobs.add(jobThree);
        jobs.add(jobFour);

        List<UserProfile> applicants = new LinkedList<>();
        applicants.add(applicantOne);
        applicants.add(applicantTwo);
        applicants.add(applicantThree);

        Matching matcher = new Matching(jobs, applicants);
        matcher.match();
        matcher.printMatches();
    }
}

