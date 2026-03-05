import com.mongodb.ConnectionString;
import com.mongodb.MongoClientSettings;
import com.mongodb.MongoException;
import com.mongodb.ServerApi;
import com.mongodb.ServerApiVersion;
import com.mongodb.client.MongoClient;
import com.mongodb.client.MongoClients;
import com.mongodb.client.MongoCollection;
import com.mongodb.client.MongoDatabase;
import com.mongodb.client.model.Filters;
import com.mongodb.client.model.Updates;

import org.bson.Document;
import org.bson.conversions.Bson;

public class DatabaseHandler {
    private MongoClient mongoClient;
    private MongoDatabase database;
    private MongoCollection<Document> collection;

    public DatabaseHandler(String collectionName) {

        String connectionString = "mongodb+srv://mathwizdavid:Burnie127@davidscluster.u4hxzhs.mongodb.net/?retryWrites=true&w=majority&appName=DavidsCluster";
        String dbName = "DavidsCluster";

        try {
            ServerApi serverApi = ServerApi.builder()
                    .version(ServerApiVersion.V1)
                    .build();

            MongoClientSettings settings = MongoClientSettings.builder()
                    .applyConnectionString(new ConnectionString(connectionString))
                    .serverApi(serverApi)
                    .build();

            mongoClient = MongoClients.create(settings);
            database = mongoClient.getDatabase(dbName);
            collection = database.getCollection(collectionName);

            System.out.println("Connected to MongoDB and using collection: " + collectionName);
        } catch (MongoException e) {
            e.printStackTrace();
            throw new RuntimeException("Failed to connect to MongoDB.");
        }
    }

    public void insertDocument(Document document) {
        try {
            collection.insertOne(document);
            System.out.println("Document inserted: " + document.toJson());
        } catch (MongoException e) {
            System.err.println("Insert failed: " + e.getMessage());
        }
    }

    public Document findDocument(String fieldName, Object value) {
        try {
            Bson filter = Filters.eq(fieldName, value);
            Document result = collection.find(filter).first();
            if (result != null) {
                System.out.println("Document found: " + result.toJson());
                return result;
            } else {
                System.out.println("No document found with " + fieldName + " = " + value);
                return null;
            }
        } catch (MongoException e) {
            System.err.println("Find failed: " + e.getMessage());
            return null;
        }
    }

    public void updateDocument(String fieldName, Object value, String updateField, Object updateValue) {
        try {
            Bson filter = Filters.eq(fieldName, value);
            Bson updateOperation = Updates.set(updateField, updateValue);
            collection.updateOne(filter, updateOperation);
            System.out.println("Document updated: " + fieldName + " = " + value);
        } catch (MongoException e) {
            System.err.println("Update failed: " + e.getMessage());
        }
    }

    public MongoCollection<Document> getCollection(){
        return collection;
    }

    public void closeConnection() {
        if (mongoClient != null) {
            mongoClient.close();
            System.out.println("MongoDB connection closed.");
        }
    }
}
