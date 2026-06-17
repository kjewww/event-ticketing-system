# API Documentation

Base URL:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## 1. Create Event

```http
POST /events
```

Request:

```json
{
  "organizer_id": "11111111-1111-1111-1111-111111111111",
  "name": "Tech Conference 2026",
  "description": "Annual technology conference.",
  "start_date": "2026-07-20",
  "end_date": "2026-07-20",
  "location": "Surabaya",
  "capacity": 100
}
```

Expected response includes:

```json
{
  "status": "Draft"
}
```

## 2. Create Ticket Category

```http
POST /events/{event_id}/ticket-categories
```

Request:

```json
{
  "organizer_id": "11111111-1111-1111-1111-111111111111",
  "name": "Regular",
  "price_amount": 50000,
  "currency": "IDR",
  "quota": 50,
  "sales_start_date": "2026-01-01",
  "sales_end_date": "2026-07-19"
}
```

Expected response includes:

```json
{
  "is_active": true
}
```

## 3. Publish Event

```http
POST /events/{event_id}/publish
```

Request:

```json
{
  "organizer_id": "11111111-1111-1111-1111-111111111111"
}
```

Expected response includes:

```json
{
  "status": "Published"
}
```

## 4. View Available Events

```http
GET /events/available
```

Optional query parameters:

```text
date_filter=2026-07-20
location=Surabaya
```

Expected response: list of published events.

## 5. View Event Details

```http
GET /events/{event_id}
```

Expected response includes event details and active ticket categories.

Ticket category purchase status may be:

```text
Available
Coming Soon
Sales Closed
Sold Out
```

## 6. Create Booking

```http
POST /bookings
```

Request:

```json
{
  "customer_id": "22222222-2222-2222-2222-222222222222",
  "customer_name": "Budi Santoso",
  "event_id": "PASTE_EVENT_ID",
  "ticket_category_id": "PASTE_TICKET_CATEGORY_ID",
  "quantity": 2,
  "service_fee_amount": 0,
  "currency": "IDR"
}
```

Expected response includes:

```json
{
  "status": "PendingPayment",
  "total_price_amount": 100000
}
```

## 7. Pay Booking

```http
POST /bookings/{booking_id}/pay
```

Request:

```json
{
  "customer_id": "22222222-2222-2222-2222-222222222222",
  "amount": 100000,
  "currency": "IDR"
}
```

Expected response includes:

```json
{
  "status": "Paid",
  "payment_reference": "PAY-..."
}
```

The response also returns issued ticket codes.

## 8. Expire Booking

```http
POST /bookings/{booking_id}/expire
```

Request:

```json
{
  "now": "2026-07-20T10:20:00"
}
```

Expected response includes:

```json
{
  "status": "Expired"
}
```

## 9. View Purchased Tickets

```http
GET /customers/{customer_id}/tickets
```

Expected response: list of tickets from paid bookings.

## 10. Check In Ticket

```http
POST /tickets/check-in
```

Request:

```json
{
  "event_id": "PASTE_EVENT_ID",
  "ticket_code": "PASTE_TICKET_CODE",
  "checked_in_at": "2026-07-20T10:00:00"
}
```

Expected response includes:

```json
{
  "status": "CheckedIn"
}
```

Invalid check-in cases return error responses:

- Ticket code not found
- Ticket already checked in
- Ticket belongs to different event
- Event is cancelled
- Check-in date is outside event date
- Ticket status is not active

## 11. Request Refund

```http
POST /bookings/{booking_id}/refunds
```

Request:

```json
{
  "customer_id": "22222222-2222-2222-2222-222222222222",
  "reason": "Cannot attend.",
  "refund_deadline": "2026-07-19T23:59:59"
}
```

Expected response includes:

```json
{
  "status": "Requested"
}
```

## 12. Approve Refund

```http
POST /refunds/{refund_id}/approve
```

Request:

```json
{
  "organizer_id": "11111111-1111-1111-1111-111111111111"
}
```

Expected response includes:

```json
{
  "status": "Approved"
}
```

## 13. Reject Refund

```http
POST /refunds/{refund_id}/reject
```

Request:

```json
{
  "organizer_id": "11111111-1111-1111-1111-111111111111",
  "rejection_reason": "Refund policy does not allow this request."
}
```

Expected response includes:

```json
{
  "status": "Rejected"
}
```

## 14. Mark Refund as Paid Out

```http
POST /refunds/{refund_id}/paid-out
```

Request:

```json
{
  "admin_id": "33333333-3333-3333-3333-333333333333"
}
```

Expected response includes:

```json
{
  "status": "PaidOut",
  "payment_reference": "REFUND-..."
}
```

## 15. View Event Sales Report

```http
GET /events/{event_id}/sales-report?organizer_id={organizer_id}
```

Expected response includes:

```json
{
  "tickets_sold_per_category": [],
  "booking_status_counts": [],
  "total_revenue_amount": 0,
  "currency": "IDR"
}
```

## 16. View Event Participants

```http
GET /events/{event_id}/participants?organizer_id={organizer_id}
```

Expected response: list of participants from paid bookings.

Each participant contains:

```json
{
  "customer_id": "UUID",
  "customer_name": "Customer Name",
  "ticket_category_name": "Regular",
  "ticket_code": "TCK-...",
  "check_in_status": "Active"
}
```

## Authorization Note

This project does not implement full authentication. For organizer-only actions, the API accepts `organizer_id` in the request body or query parameter and compares it with the event's `organizer_id`.