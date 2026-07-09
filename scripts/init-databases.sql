-- Create all databases for microservices
CREATE DATABASE IF NOT EXISTS auth_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS company_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS seeker_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS chat_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE DATABASE IF NOT EXISTS ai_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Grant all privileges
GRANT ALL PRIVILEGES ON auth_db.* TO 'root'@'%';
GRANT ALL PRIVILEGES ON company_db.* TO 'root'@'%';
GRANT ALL PRIVILEGES ON seeker_db.* TO 'root'@'%';
GRANT ALL PRIVILEGES ON chat_db.* TO 'root'@'%';
GRANT ALL PRIVILEGES ON ai_db.* TO 'root'@'%';

FLUSH PRIVILEGES;
