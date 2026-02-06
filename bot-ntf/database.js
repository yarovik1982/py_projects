const sqlite3 = require('sqlite3').verbose();
const path = require('path');

class Database {
   constructor() {
      this.db = new sqlite3.Database(path.join(__dirname, 'bot.db'), (err) => {
         if (err) {
            console.error('Error opening database:', err);
         } else {
            console.log('Connected to SQLite database');
            this.createTables();
         }
      });
   }

   createTables() {
      const queries = [
         `CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        balance INTEGER DEFAULT 1000,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
      )`,

         `CREATE TABLE IF NOT EXISTS inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        item_name TEXT,
        rarity TEXT,
        obtained_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
      )`,

         `CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        amount INTEGER,
        type TEXT,
        description TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES users (user_id)
      )`,

         `CREATE TABLE IF NOT EXISTS cooldowns (
        user_id INTEGER,
        action TEXT,
        last_used DATETIME,
        PRIMARY KEY (user_id, action)
      )`
      ];

      queries.forEach(query => {
         this.db.run(query, (err) => {
            if (err) {
               console.error('Error creating table:', err);
            }
         });
      });
   }

   getUser(userId) {
      return new Promise((resolve, reject) => {
         this.db.get('SELECT * FROM users WHERE user_id = ?', [userId], (err, row) => {
            if (err) reject(err);
            else resolve(row);
         });
      });
   }

   createUser(userId, username) {
      return new Promise((resolve, reject) => {
         this.db.run(
            'INSERT OR IGNORE INTO users (user_id, username, balance) VALUES (?, ?, 1000)',
            [userId, username],
            function (err) {
               if (err) reject(err);
               else resolve(this.lastID);
            }
         );
      });
   }

   updateBalance(userId, amount) {
      return new Promise((resolve, reject) => {
         this.db.run(
            'UPDATE users SET balance = balance + ? WHERE user_id = ?',
            [amount, userId],
            (err) => {
               if (err) reject(err);
               else resolve();
            }
         );
      });
   }

   addToInventory(userId, itemName, rarity) {
      return new Promise((resolve, reject) => {
         this.db.run(
            'INSERT INTO inventory (user_id, item_name, rarity) VALUES (?, ?, ?)',
            [userId, itemName, rarity],
            function (err) {
               if (err) reject(err);
               else resolve(this.lastID);
            }
         );
      });
   }

   getInventory(userId) {
      return new Promise((resolve, reject) => {
         this.db.all(
            'SELECT * FROM inventory WHERE user_id = ? ORDER BY obtained_at DESC',
            [userId],
            (err, rows) => {
               if (err) reject(err);
               else resolve(rows);
            }
         );
      });
   }

   addTransaction(userId, amount, type, description) {
      return new Promise((resolve, reject) => {
         this.db.run(
            'INSERT INTO transactions (user_id, amount, type, description) VALUES (?, ?, ?, ?)',
            [userId, amount, type, description],
            (err) => {
               if (err) reject(err);
               else resolve();
            }
         );
      });
   }

   setCooldown(userId, action) {
      return new Promise((resolve, reject) => {
         this.db.run(
            'INSERT OR REPLACE INTO cooldowns (user_id, action, last_used) VALUES (?, ?, CURRENT_TIMESTAMP)',
            [userId, action],
            (err) => {
               if (err) reject(err);
               else resolve();
            }
         );
      });
   }

   getCooldown(userId, action) {
      return new Promise((resolve, reject) => {
         this.db.get(
            'SELECT last_used FROM cooldowns WHERE user_id = ? AND action = ?',
            [userId, action],
            (err, row) => {
               if (err) reject(err);
               else resolve(row ? new Date(row.last_used) : null);
            }
         );
      });
   }
}

module.exports = new Database();