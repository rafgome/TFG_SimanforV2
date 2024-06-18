const { MongoClient } = require('mongodb');

const waitingQueries = [];
let db = null;

const serverURL = process.env.MONGO_HOST;
const serverDB = process.env.MONGO_DB || 'simanfor';

if (serverURL && serverDB) {
    MongoClient.connect(`${serverURL}`, {
        useUnifiedTopology: true,
    }, (err, client) => {
        if (err) {
            console.warn('MongoDB: Could not connect', err);
            return;
        }

        console.info('MongoDB: Connected');
        db = client.db(serverDB);

        // Fire all waiting queries.
        waitingQueries.forEach((cb) => {
            cb();
        });
    });
} else {
    console.warn('MongoDB connection can\'t be initiated. You need to define config parameters.');
}

const checkIfConnectedAndWait = (cb) => {
    if (!db) return waitingQueries.push(cb);
    return cb();
}

/*
* collectionName: String
* documents: Array
*/
const insert = async (collectionName, documents) => {
    const documentsArray = (Array.isArray(documents)) ? documents : [documents];

    return new Promise((resolve, reject) => {
        checkIfConnectedAndWait(() => {
            const collection = db.collection(collectionName);
            collection.insertMany(documentsArray, (err, result) => {
                if (err) {
                    console.error('Mongo insert ', err);
                    return reject(err);
                }

                return resolve(result);
            });
        });
    });
}

/*
* collectionName: String
* documents: Object
*/
const find = async (collectionName, query) => {
    return new Promise((resolve, reject) => {
        checkIfConnectedAndWait(() => {
            const collection = db.collection(collectionName);
            collection.find(query).toArray((err, docs) => {
                if (err) {
                    console.error('Mongo find ', err);
                    return reject(err);
                }

                return resolve(docs);
            });
        });
    });
}

/*
* collectionName: String
* query: Object
* data: Object
*/
const update = async (collectionName, query, data) => {
    return new Promise((resolve, reject) => {
        checkIfConnectedAndWait(() => {
            const collection = db.collection(collectionName);
            collection.updateOne(query, { $set: data }, (err, result) => {
                if (err) {
                    console.error('Mongo update ', err);
                    return reject(err);
                }

                return resolve(result);
            });
        });
    });
}

/*
* collectionName: String
* query: Object
*/
const remove = async (collectionName, query) => {
    return new Promise((resolve, reject) => {
        checkIfConnectedAndWait(() => {
            const collection = db.collection(collectionName);
            collection.deleteOne(query, (err, result) => {
                if (err) {
                    console.error('Mongo remove ', err);
                    return reject(err);
                }

                return resolve(result);
            });
        });
    });
};

module.exports = {
    insert,
    update,
    remove,
    find
};
