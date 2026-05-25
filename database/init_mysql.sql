CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    applicant_name VARCHAR(100) NOT NULL,
    organization_name VARCHAR(150) NOT NULL,
    contact_phone VARCHAR(30),
    email VARCHAR(100),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS applications (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    user_id BIGINT NOT NULL,
    title VARCHAR(200) NOT NULL,
    water_usage VARCHAR(255) NOT NULL,
    water_location VARCHAR(255) NOT NULL,
    application_period VARCHAR(100) NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'PENDING',
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_app_user FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS application_files (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    application_id BIGINT NOT NULL,
    original_name VARCHAR(255) NOT NULL,
    storage_path VARCHAR(255) NOT NULL,
    file_size BIGINT,
    content_type VARCHAR(100),
    uploaded_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_file_app FOREIGN KEY (application_id) REFERENCES applications(id)
);

CREATE TABLE IF NOT EXISTS review_results (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    application_id BIGINT NOT NULL,
    review_status VARCHAR(30) NOT NULL,
    summary VARCHAR(500) NOT NULL,
    risk_level VARCHAR(30) NOT NULL,
    suggestions TEXT,
    issues TEXT,
    knowledge_sources TEXT,
    completeness_rate DECIMAL(5,4),
    reviewed_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_review_app FOREIGN KEY (application_id) REFERENCES applications(id)
);
