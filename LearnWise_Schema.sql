CREATE TABLE Courses (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    url TEXT UNIQUE,
    is_paid BOOLEAN,
    price NUMERIC CHECK (price >= 0),
    duration NUMERIC,
    published TIMESTAMP,
    level TEXT NOT NULL,
    subject TEXT NOT NULL,
    source TEXT NOT NULL
);

CREATE TABLE Ratings (
    rating_id SERIAL PRIMARY KEY,
    course_id INTEGER REFERENCES Courses(id) ON DELETE CASCADE,
    number_of_ratings INTEGER NOT NULL,
    rating NUMERIC CHECK (rating >= 0 AND rating <= 5)
);

CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);
