db.createUser({
    user: 'accessuser',
    pwd: 'accesspwd',
    roles: [
        {
            role: 'readWrite',
            db: 'image_records',
        },
    ],
});

db = new Mongo().getDB("image_records");

db.createCollection('images', { capped: false });