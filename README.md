# Event Management System

Event Management System is a backend application for managing events, ticket categories, bookings, ticket payments, ticket check-in, refunds, sales reports, and participant lists.

This project is implemented using **Clean Architecture** and **Domain-Driven Design tactical patterns**. The system separates business logic from application use cases, infrastructure persistence, and REST API controllers.

## Main Features

- Event organizers can create, publish, and cancel events.
- Event organizers can create and disable ticket categories.
- Customers can browse published events and view event details.
- Customers can create bookings and pay for tickets.
- The system issues tickets with unique ticket codes after successful payment.
- Gate officers can validate and check in tickets.
- Customers can request refunds.
- Event organizers can approve or reject refund requests.
- System admins can mark approved refunds as paid out.
- Event organizers can view sales reports and participant lists.

## Architecture

This project follows four main layers:

```text
src/
├── domain/
├── application/
├── infrastructure/
└── presentation/
```

### Domain Layer

Contains core business rules and DDD tactical patterns:

- Aggregates
- Entities
- Value objects
- Domain services / policies
- Domain events
- Repository interfaces
- Domain exceptions

### Application Layer

Contains use case orchestration:

- Commands
- Command handlers
- Queries
- Query handlers
- DTOs
- Application service interfaces

### Infrastructure Layer

Contains technical implementations:

- PostgreSQL database connection
- SQLAlchemy models
- SQLAlchemy repository implementations
- Aggregate mappers
- Unit of Work implementation
- Simulated external service adapters
- SQL migration file

### Presentation Layer

Contains REST API implementation:

- FastAPI application
- API routers/controllers
- Request schemas
- Response schemas
- Dependency wiring

## Project Structure

```text
event-management-system/
├── docs/
│   ├── api_documentation.md
│   ├── aggregates_and_business_rules.md
│   ├── clean_architecture_diagram.svg
│   ├── domain_model_diagram.svg
│   └── ubiquitous_language_glossary.md
├── src/
│   ├── application/
│   │   ├── command_handlers/
│   │   ├── commands/
│   │   ├── dto/
│   │   ├── interfaces/
│   │   ├── queries/
│   │   └── query_handlers/
│   ├── domain/
│   │   ├── aggregates/
│   │   ├── entities/
│   │   ├── events/
│   │   ├── exceptions/
│   │   ├── repositories/
│   │   ├── services/
│   │   └── value_objects/
│   ├── infrastructure/
│   │   ├── database/
│   │   │   ├── migrations/
│   │   │   └── models/
│   │   ├── mappers/
│   │   ├── repositories/
│   │   ├── services/
│   │   └── unit_of_work/
│   └── presentation/
│       ├── api/
│       ├── schemas/
│       ├── dependencies.py
│       └── main.py
├── tests/
│   └── domain/
├── .env.example
├── .gitignore
├── pyproject.toml
├── uv.lock
└── README.md
```

The `src/` directory contains the application code, separated into Clean Architecture layers. The `tests/domain/` directory contains the required domain unit tests. The `docs/` directory contains supporting deliverables such as API documentation, architecture diagrams, domain model diagrams, aggregate explanations, and the ubiquitous language glossary.

## How to Run the Project

### Technology Stack

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pydantic
- pytest
- uv

### Prerequisites

Before running the project, make sure these are installed:

- Python
- uv
- PostgreSQL
- pgAdmin or another PostgreSQL database client

PostgreSQL must be running before the API server is started.

### Install Dependencies

From the project root, run:

```bash
uv sync
```

This installs the dependencies defined in the project configuration.

If dependencies are not installed yet, install them with:

```bash
uv add fastapi uvicorn sqlalchemy psycopg python-dotenv pydantic
uv add --dev pytest
```

### Start the API Server

After configuring PostgreSQL and preparing the database tables, run:

```bash
uv run python -m uvicorn src.presentation.main:app --reload
```

Open the interactive API documentation:

```text
http://127.0.0.1:8000/docs
```

Root endpoint:

```text
GET /
```

Expected response:

```json
{
  "message": "Event Ticketing System API",
  "status": "running"
}
```

## How to Configure PostgreSQL

Create a PostgreSQL database named:

```text
event_ticketing
```

Using pgAdmin:

```text
Servers → PostgreSQL → Databases → Right click → Create → Database
```

Set the database name to:

```text
event_ticketing
```

Alternatively, using SQL:

```sql
CREATE DATABASE event_ticketing;
```

Create a `.env` file in the project root. Use `.env.example` as the reference:

```env
DATABASE_URL=postgresql+psycopg://postgres:YOUR_PASSWORD@localhost:5432/event_ticketing
```

Example:

```env
DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/event_ticketing
```

Replace `YOUR_PASSWORD` with your local PostgreSQL password.

Do not commit `.env`.

## How to Run Database Migration

The SQL schema file is located at:

```text
src/infrastructure/database/migrations/001_create_event_ticketing_tables.sql
```

This migration creates the required PostgreSQL tables:

- `events`
- `ticket_categories`
- `bookings`
- `tickets`
- `refunds`

### Option 1: Manual Migration Using pgAdmin

Open pgAdmin Query Tool, select the `event_ticketing` database, paste the contents of this file, and execute it:

```text
src/infrastructure/database/migrations/001_create_event_ticketing_tables.sql
```

### Option 2: Manual Migration Using psql

If `psql` is available from the terminal, run:

```bash
psql -U postgres -d event_ticketing -f src/infrastructure/database/migrations/001_create_event_ticketing_tables.sql
```

On Windows, if `psql` is not available in PATH, use the full path. Example:

```powershell
& "C:\Program Files\PostgreSQL\17\bin\psql.exe" -U postgres -d event_ticketing -f "src\infrastructure\database\migrations\001_create_event_ticketing_tables.sql"
```

Change `17` to your installed PostgreSQL version.

### Option 3: Automatic Table Creation During Startup

The FastAPI application also calls `create_tables()` during startup, so the tables can be created automatically when the server starts:

```bash
uv run python -m uvicorn src.presentation.main:app --reload
```

The SQL migration file is still included as the formal database schema/migration deliverable.

## How to Run Tests

The required tests for this project are domain unit tests.

Run:

```bash
uv run python -m pytest tests/domain -q
```

Expected result:

```text
34 passed
```

The domain tests cover event rules, booking rules, ticket check-in rules, refund rules, and domain services/policies.

## List of Implemented User Stories

| ID | User Story | Status |
|---|---|---|
| US1 | Create Event | Implemented |
| US2 | Publish Event | Implemented |
| US3 | Cancel Event | Implemented |
| US4 | Create Ticket Category | Implemented |
| US5 | Disable Ticket Category | Implemented |
| US6 | View Available Events | Implemented |
| US7 | View Event Details | Implemented |
| US8 | Create Ticket Booking | Implemented |
| US9 | Calculate Booking Total Price | Implemented |
| US10 | Pay Booking | Implemented |
| US11 | Expire Booking | Implemented |
| US12 | View Purchased Tickets | Implemented |
| US13 | Check In Ticket | Implemented |
| US14 | Reject Invalid Ticket Check-in | Implemented |
| US15 | Request Refund | Implemented |
| US16 | Approve Refund | Implemented |
| US17 | Reject Refund | Implemented |
| US18 | Mark Refund as Paid Out | Implemented |
| US19 | View Event Sales Report | Implemented |
| US20 | View Event Participants | Implemented |

## List of Implemented Domain Events

| Domain Event | Raised When |
|---|---|
| `EventCreated` | Event is created |
| `EventPublished` | Event is published |
| `EventCancelled` | Event is cancelled |
| `TicketCategoryCreated` | Ticket category is created |
| `TicketCategoryDisabled` | Ticket category is disabled |
| `TicketReserved` | Booking is created |
| `BookingPaid` | Booking is paid |
| `BookingExpired` | Booking expires |
| `TicketCheckedIn` | Ticket is checked in |
| `RefundRequested` | Refund is requested |
| `RefundApproved` | Refund is approved |
| `RefundRejected` | Refund is rejected |
| `RefundPaidOut` | Refund is marked as paid out |

## List of Implemented Application Service Interfaces

| Interface | Purpose | Infrastructure Implementation |
|---|---|---|
| `PaymentGateway` | Process booking payment | `FakePaymentGateway` |
| `RefundPaymentService` | Process refund payout | `FakeRefundPaymentService` |
| `NotificationService` | Send notification | `FakeNotificationService` |
| `TicketCodeGenerator` | Generate unique ticket codes | `UUIDTicketCodeGenerator` |
| `UnitOfWork` | Commit/rollback transaction | `SqlAlchemyUnitOfWork` |
| `EventReadRepository` | Read available events and event details | `SqlAlchemyEventReadRepository` |
| `BookingReadRepository` | Read purchased tickets | `SqlAlchemyBookingReadRepository` |
| `ReportReadRepository` | Read sales reports and participants | `SqlAlchemyReportReadRepository` |

## Notes

- This project uses simulated external service adapters instead of real payment, bank, or notification integrations. The interfaces are defined in the application layer, while the implementations are placed in the infrastructure layer.
- Additional documentation may be found in the "docs" folder.
