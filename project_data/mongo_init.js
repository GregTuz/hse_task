const readerUsername = process.env.MONGO_READER_USERNAME;
const readerPassword = process.env.MONGO_READER_PASSWORD;

const adminUsername = process.env.MONGO_INITDB_ROOT_USERNAME;
const adminPassword = process.env.MONGO_INITDB_ROOT_PASSWORD;

const dbName = process.env.MONGO_DB_NAME;

db = db.getSiblingDB(dbName);

db.createCollection("users"
//, {
//    validator: {
//        $jsonSchema: {
//            bsonType: "object",
//            required: ["results", "info"],
//            properties: {
//                results: {
//                    bsonType: "array",
//                    items: {
//                        bsonType: "object",
//                        properties: {
//                            gender: { bsonType: ["string", "null"] },
//                            name: {
//                                bsonType: "object",
//                                properties: {
//                                    title: { bsonType: ["string", "null"] },
//                                    first: { bsonType: ["string", "null"] },
//                                    last: { bsonType: ["string", "null"] }
//                                }
//                            },
//                            location: {
//                                bsonType: "object",
//                                properties: {
//                                    street: {
//                                        bsonType: "object",
//                                        properties: {
//                                            number: { bsonType: ["int", "null"] },
//                                            name: { bsonType: ["string", "null"] }
//                                        }
//                                    },
//                                    city: { bsonType: ["string", "null"] },
//                                    state: { bsonType: ["string", "null"] },
//                                    country: { bsonType: ["string", "null"] },
//                                    postcode: { bsonType: ["string", "int", "null"] },
//                                    coordinates: {
//                                        bsonType: "object",
//                                        properties: {
//                                            latitude: { bsonType: ["string", "null"] },
//                                            longitude: { bsonType: ["string", "null"] }
//                                        }
//                                    },
//                                    timezone: {
//                                        bsonType: "object",
//                                        properties: {
//                                            offset: { bsonType: ["string", "null"] },
//                                            description: { bsonType: ["string", "null"] }
//                                        }
//                                    }
//                                }
//                            },
//                            email: { bsonType: ["string", "null"] },
//                            login: {
//                                bsonType: "object",
//                                properties: {
//                                    uuid: { bsonType: ["string", "null"] },
//                                    username: { bsonType: ["string", "null"] },
//                                    password: { bsonType: ["string", "null"] },
//                                    salt: { bsonType: ["string", "null"] },
//                                    md5: { bsonType: ["string", "null"] },
//                                    sha1: { bsonType: ["string", "null"] },
//                                    sha256: { bsonType: ["string", "null"] }
//                                }
//                            },
//                            dob: {
//                                bsonType: "object",
//                                properties: {
//                                    date: { bsonType: ["string", "null"] },
//                                    age: { bsonType: ["int", "null"] }
//                                }
//                            },
//                            registered: {
//                                bsonType: "object",
//                                properties: {
//                                    date: { bsonType: ["string", "null"] },
//                                    age: { bsonType: ["int", "null"] }
//                                }
//                            },
//                            phone: { bsonType: ["string", "null"] },
//                            cell: { bsonType: ["string", "null"] },
//                            id: {
//                                bsonType: "object",
//                                properties: {
//                                    name: { bsonType: ["string", "null"] },
//                                    value: { bsonType: ["string", "null"] }
//                                }
//                            },
//                            picture: {
//                                bsonType: "object",
//                                properties: {
//                                    large: { bsonType: ["string", "null"] },
//                                    medium: { bsonType: ["string", "null"] },
//                                    thumbnail: { bsonType: ["string", "null"] }
//                                }
//                            },
//                            nat: { bsonType: ["string", "null"] }
//                        }
//                    }
//                },
//                info: {
//                    bsonType: "object",
//                    properties: {
//                        seed: { bsonType: ["string", "null"] },
//                        results: { bsonType: ["int", "null"] },
//                        page: { bsonType: ["int", "null"] },
//                        version: { bsonType: ["string", "null"] }
//                    }
//                }
//            }
//        }
//    }
//}
);

db.createUser({
    user: adminUsername,
    pwd: adminPassword,
    roles: [
        { role: "root", db: "admin"},
        { role: "dbAdmin", db: dbName }
    ]
});

db.createUser({
    user: readerUsername,
    pwd: readerPassword,
    roles: [
        { role: "read", db: dbName }
    ]
});