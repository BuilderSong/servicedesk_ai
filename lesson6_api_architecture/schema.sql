CREATE TABLE organizations (
    id   BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE properties (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    organization_id BIGINT NOT NULL REFERENCES organizations(id),
    address         TEXT NOT NULL
);

-- No organization_id here: a request's org is reached through its property.
CREATE TABLE requests (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    property_id BIGINT NOT NULL REFERENCES properties(id),
    description TEXT NOT NULL
                CHECK (length(btrim(description)) BETWEEN 1 AND 1000),
    status      TEXT NOT NULL DEFAULT 'open'
                CHECK (status IN ('open', 'closed')),
    created_by  TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);