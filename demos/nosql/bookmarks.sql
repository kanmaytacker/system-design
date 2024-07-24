CREATE TABLE Users (
    UserID SERIAL PRIMARY KEY,
    Username VARCHAR(255) NOT NULL,
    Email VARCHAR(255) NOT NULL UNIQUE
);

CREATE TABLE Bookmarks (
    BookmarkID SERIAL PRIMARY KEY,
    UserID INT NOT NULL,
    URL VARCHAR(2048) NOT NULL,
    Title VARCHAR(255) NOT NULL,
    Description TEXT,
    CreatedOn TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (UserID) REFERENCES Users(UserID)
);

CREATE TABLE Tags (
    TagID SERIAL PRIMARY KEY,
    TagName VARCHAR(50) UNIQUE NOT NULL
);

CREATE TABLE BookmarkTags (
    BookmarkID INT,
    TagID INT,
    PRIMARY KEY (BookmarkID, TagID),
    FOREIGN KEY (BookmarkID) REFERENCES Bookmarks(BookmarkID),
    FOREIGN KEY (TagID) REFERENCES Tags(TagID)
);

INSERT INTO
    Users (Username, Email)
VALUES
    ('tantia.tope', 'tantia.top@example.com'),
    ('sherlock.holmes', 'sherlock.holmes@example.com'),
    ('bruce.wayne', 'bruce.wayne@example.com');

INSERT INTO
    Bookmarks (UserID, URL, Title, Description, CreatedOn)
VALUES
    (
        1,
        'https://www.example.com',
        'Example Website',
        'This is an example website.',
        '2024-07-24 12:00:00'
    ),
    (
        1,
        'https://www.news.com',
        'News Website',
        'This is a news website.',
        '2024-07-24 13:00:00'
    ),
    (
        2,
        'https://www.opensource.org',
        'Open Source',
        'This is an open source community website.',
        '2024-07-24 14:00:00'
    );

INSERT INTO
    Tags (TagName)
VALUES
    ('Education'),
    ('News'),
    ('Technology'),
    ('Open Source');

INSERT INTO
    BookmarkTags (BookmarkID, TagID)
VALUES
    (1, 1),
    -- Example Website tagged with Education
    (1, 3),
    -- Example Website also tagged with Technology
    (2, 2),
    -- News Website tagged with News
    (2, 3),
    -- News Website also tagged with Technology
    (3, 4);

-- Open Source website tagged with Open Source