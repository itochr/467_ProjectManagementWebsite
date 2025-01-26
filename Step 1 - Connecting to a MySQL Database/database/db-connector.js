// Get an instance of mysql we can use in the app
var mysql = require('mysql')

const fs = require("fs");

// Create a 'connection pool' using the provided credentials
var pool = mysql.createPool({
    user: "avnadmin",
    password: "AVNS_jJ5EndBYUZa_wWh4np5",
    host: "mysql-osu-capstone-capstone-project-management.l.aivencloud.com",
    port: "27713",
    database: "DATABASE",
    ssl: {
      rejectUnauthorized: true,
      ca: fs.readFileSync("./database/ca.pem").toString(),
    },
})

// Export it for use in our applicaiton
module.exports.pool = pool;
