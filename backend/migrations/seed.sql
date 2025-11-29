INSERT INTO providers (name, slug, website)
VALUES
    ('TXU Energy', 'txu', 'https://www.txu.com'),
    ('Reliant Energy', 'reliant', 'https://www.reliant.com'),
    ('Gexa Energy', 'gexa', 'https://www.gexaenergy.com'),
    ('Direct Energy', 'direct_energy', 'https://www.directenergy.com')
ON CONFLICT (slug) DO UPDATE SET name = EXCLUDED.name, website = EXCLUDED.website;
