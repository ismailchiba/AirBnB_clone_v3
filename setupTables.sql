-- setup all tables
USE hbnb_dev_db;

CREATE TABLE IF NOT EXISTS states(
        id VARCHAR(60) PRIMARY KEY,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        name VARCHAR(128) NOT NULL
);

CREATE TABLE IF NOT EXISTS cities (
        id VARCHAR(60) PRIMARY KEY,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        name VARCHAR(128) NOT NULL,
        state_id VARCHAR(60) NOT NULL,
        FOREIGN KEY (state_id) REFERENCES states(id)
);

CREATE TABLE IF NOT EXISTS users (
        id VARCHAR(60) PRIMARY KEY,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        email VARCHAR(128) NOT NULL,
        password VARCHAR(128) NOT NULL,
        first_name VARCHAR(128) NULL,
        last_name VARCHAR(128) NULL
);

CREATE TABLE IF NOT EXISTS places (
        id VARCHAR(60) PRIMARY KEY,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        name VARCHAR(128) NOT NULL,
        description VARCHAR(1024) NULL,
        number_rooms INTEGER DEFAULT 0 NOT NULL,
        number_bathrooms INTEGER DEFAULT 0 NOT NULL,
        max_guest INTEGER DEFAULT 0 NOT NULL,
        price_by_night INTEGER DEFAULT 0 NOT NULL,
        latitude DECIMAL NULL,
        longitude DECIMAL NULL,
        city_id VARCHAR(60) NOT NULL,
        user_id VARCHAR(60) NOT NULL,
        FOREIGN KEY (city_id) REFERENCES cities(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS reviews (
        id VARCHAR(60) PRIMARY KEY,
        created_at DATETIME NOT NULL,
        updated_at DATETIME NOT NULL,
        text VARCHAR(1024) NOT NULL,
        place_id VARCHAR(60) NOT NULL,
        user_id VARCHAR(60) NOT NULL,
        FOREIGN KEY (place_id) REFERENCES places(id),
        FOREIGN KEY (user_id) REFERENCES users(id)
);
