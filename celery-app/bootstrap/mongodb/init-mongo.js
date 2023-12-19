// db.createUser({
//     user: 'accessuser',
//     pwd: 'accesspwd',
//     roles: [
//         {
//             role: 'readWrite',
//             db: 'image_records',
//         },
//         {
//             role: 'readWrite',
//             db: 'celery_results',
//         },

//     ],
// });

var adminUser = {
    user: 'accessuser',
    pwd: 'accesspwd',
    roles: [
        {
            role: 'readWrite',
            db: 'image_records',
        },
        {
            role: 'readWrite',
            db: 'celery',
        },

    ],
}

var adminDb = db.getSiblingDB('admin');

adminDb.createUser(adminUser);

db.getSiblingDB('admin').auth(adminUser.user, adminUser.pwd);

db = new Mongo().getDB("image_records");
db.createCollection('images', { capped: false });

// db = new Mongo().getDB("celery_results");
// db.createCollection('results', { capped: false });


// db.createUser({
//     user: 'accessuser',
//     pwd: 'accesspwd',
//     roles: [
//         {
//             role: 'readWrite',
//             db: 'celery_results',
//         },
//     ],
// });

// db = new Mongo().getDB("celery_results");