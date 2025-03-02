-- Create the users table if not exists
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Default user (password: "admin123")
INSERT INTO users (name, email, hashed_password) VALUES 
    ('Admin User', 'admin@mail.com', '$2b$12$2N.8Y5Bh9JZc5AKTqkXZ6Otpt6Nz5IoLpFkrb4x0FOUCBHby3RjXO')
ON CONFLICT (email) DO NOTHING;
