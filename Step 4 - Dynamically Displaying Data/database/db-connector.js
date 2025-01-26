// Get an instance of mysql we can use in the app
var mysql = require('mysql')

// Create a 'connection pool' using the provided credentials
var pool = mysql.createPool({
    connectionLimit : 10,
    host            : 'mysql-osu-capstone-capstone-project-management.l.aivencloud.com',
    user            : 'avnadmin',
    password        : 'AVNS_jJ5EndBYUZa_wWh4np5',
    database        : 'defaultdb'
})

// Export it for use in our applicaiton
module.exports.pool = pool;
