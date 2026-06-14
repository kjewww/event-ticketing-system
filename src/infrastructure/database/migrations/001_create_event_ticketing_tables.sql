CREATE EXTENSION IF NOT EXISTS "pgcrypto";

CREATE TABLE IF NOT EXISTS events (
    id UUID PRIMARY KEY,
    organizer_id UUID NOT NULL,
    name VARCHAR(255) NOT NULL,
    description TEXT NOT NULL,
    location VARCHAR(255) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    capacity INTEGER NOT NULL,
    status VARCHAR(50) NOT NULL,

    CONSTRAINT ck_events_capacity_positive CHECK (capacity > 0),
    CONSTRAINT ck_events_date_range CHECK (end_date >= start_date)
);

CREATE INDEX IF NOT EXISTS ix_events_organizer_id ON events (organizer_id);
CREATE INDEX IF NOT EXISTS ix_events_status ON events (status);
CREATE INDEX IF NOT EXISTS ix_events_location ON events (location);
CREATE INDEX IF NOT EXISTS ix_events_start_date ON events (start_date);

CREATE TABLE IF NOT EXISTS ticket_categories (
    id UUID PRIMARY KEY,
    event_id UUID NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    name VARCHAR(100) NOT NULL,
    price_amount NUMERIC(12, 2) NOT NULL,
    price_currency VARCHAR(10) NOT NULL DEFAULT 'IDR',
    quota INTEGER NOT NULL,
    sales_start_date DATE NOT NULL,
    sales_end_date DATE NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,

    CONSTRAINT ck_ticket_categories_price_non_negative CHECK (price_amount >= 0),
    CONSTRAINT ck_ticket_categories_quota_positive CHECK (quota > 0),
    CONSTRAINT ck_ticket_categories_sales_range CHECK (sales_end_date >= sales_start_date)
);

CREATE INDEX IF NOT EXISTS ix_ticket_categories_event_id ON ticket_categories (event_id);
CREATE INDEX IF NOT EXISTS ix_ticket_categories_is_active ON ticket_categories (is_active);

CREATE TABLE IF NOT EXISTS bookings (
    id UUID PRIMARY KEY,
    customer_id UUID NOT NULL,
    customer_name VARCHAR(255) NOT NULL DEFAULT '',
    event_id UUID NOT NULL REFERENCES events(id) ON DELETE RESTRICT,
    ticket_category_id UUID NOT NULL REFERENCES ticket_categories(id) ON DELETE RESTRICT,
    quantity INTEGER NOT NULL,

    unit_price_amount NUMERIC(12, 2) NOT NULL,
    unit_price_currency VARCHAR(10) NOT NULL DEFAULT 'IDR',

    service_fee_amount NUMERIC(12, 2) NOT NULL DEFAULT 0,
    service_fee_currency VARCHAR(10) NOT NULL DEFAULT 'IDR',

    total_price_amount NUMERIC(12, 2) NOT NULL,
    total_price_currency VARCHAR(10) NOT NULL DEFAULT 'IDR',

    payment_deadline_at TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL,
    refund_required BOOLEAN NOT NULL DEFAULT FALSE,

    CONSTRAINT ck_bookings_quantity_positive CHECK (quantity > 0),
    CONSTRAINT ck_bookings_unit_price_non_negative CHECK (unit_price_amount >= 0),
    CONSTRAINT ck_bookings_service_fee_non_negative CHECK (service_fee_amount >= 0),
    CONSTRAINT ck_bookings_total_price_non_negative CHECK (total_price_amount >= 0)
);

CREATE INDEX IF NOT EXISTS ix_bookings_customer_id ON bookings (customer_id);
CREATE INDEX IF NOT EXISTS ix_bookings_event_id ON bookings (event_id);
CREATE INDEX IF NOT EXISTS ix_bookings_ticket_category_id ON bookings (ticket_category_id);
CREATE INDEX IF NOT EXISTS ix_bookings_status ON bookings (status);

CREATE TABLE IF NOT EXISTS tickets (
    id UUID PRIMARY KEY,
    booking_id UUID NOT NULL REFERENCES bookings(id) ON DELETE CASCADE,
    event_id UUID NOT NULL REFERENCES events(id) ON DELETE RESTRICT,
    ticket_category_id UUID NOT NULL REFERENCES ticket_categories(id) ON DELETE RESTRICT,
    ticket_code VARCHAR(100) NOT NULL UNIQUE,
    status VARCHAR(50) NOT NULL,
    checked_in_at TIMESTAMP NULL
);

CREATE INDEX IF NOT EXISTS ix_tickets_booking_id ON tickets (booking_id);
CREATE INDEX IF NOT EXISTS ix_tickets_event_id ON tickets (event_id);
CREATE INDEX IF NOT EXISTS ix_tickets_ticket_category_id ON tickets (ticket_category_id);
CREATE INDEX IF NOT EXISTS ix_tickets_ticket_code ON tickets (ticket_code);
CREATE INDEX IF NOT EXISTS ix_tickets_status ON tickets (status);

CREATE TABLE IF NOT EXISTS refunds (
    id UUID PRIMARY KEY,
    booking_id UUID NOT NULL UNIQUE REFERENCES bookings(id) ON DELETE RESTRICT,
    customer_id UUID NOT NULL,
    amount NUMERIC(12, 2) NOT NULL,
    currency VARCHAR(10) NOT NULL DEFAULT 'IDR',
    reason TEXT NULL,
    status VARCHAR(50) NOT NULL,
    rejection_reason TEXT NULL,
    payment_reference VARCHAR(255) NULL,

    CONSTRAINT ck_refunds_amount_non_negative CHECK (amount >= 0)
);

CREATE INDEX IF NOT EXISTS ix_refunds_booking_id ON refunds (booking_id);
CREATE INDEX IF NOT EXISTS ix_refunds_customer_id ON refunds (customer_id);
CREATE INDEX IF NOT EXISTS ix_refunds_status ON refunds (status);