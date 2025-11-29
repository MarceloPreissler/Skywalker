CREATE TABLE IF NOT EXISTS providers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    slug VARCHAR(100) NOT NULL UNIQUE,
    website VARCHAR(255),
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS plans (
    id SERIAL PRIMARY KEY,
    provider_id INTEGER NOT NULL REFERENCES providers(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    term_months INTEGER,
    rate_cents_kwh NUMERIC(8,2),
    base_fee NUMERIC(8,2),
    cancellation_fee NUMERIC(8,2),
    renewable_percentage INTEGER,
    features TEXT,
    url VARCHAR(255),
    last_scraped_at TIMESTAMP NOT NULL DEFAULT NOW()
);
CREATE INDEX IF NOT EXISTS idx_plans_provider_id ON plans(provider_id);
