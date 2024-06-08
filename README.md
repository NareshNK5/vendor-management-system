# Vendor Management System

## Overview

The Vendor Management System is a Django-based application that allows users to manage vendor profiles, track purchase orders, and evaluate vendor performance using various metrics. This project utilizes Django REST Framework to provide API endpoints for creating, retrieving, updating, and deleting vendor and purchase order data.

## Features

1. **Vendor Profile Management**
    - Create, list, retrieve, update, and delete vendor profiles.

2. **Purchase Order Tracking**
    - Create, list, retrieve, update, and delete purchase orders.
    - Track details such as PO number, vendor reference, order date, items, quantity, and status.

3. **Vendor Performance Evaluation**
    - Metrics include On-Time Delivery Rate, Quality Rating, Response Time, and Fulfillment Rate.
    - Historical performance tracking.

## Models

### Vendor Model
- `name`: CharField - Vendor's name.
- `contact_details`: TextField - Contact information of the vendor.
- `address`: TextField - Physical address of the vendor.
- `vendor_code`: CharField - A unique identifier for the vendor.
- `on_time_delivery_rate`: FloatField - Tracks the percentage of on-time deliveries.
- `quality_rating_avg`: FloatField - Average rating of quality based on purchase orders.
- `average_response_time`: FloatField - Average time taken to acknowledge purchase orders.
- `fulfillment_rate`: FloatField - Percentage of purchase orders fulfilled successfully.

### Purchase Order Model
- `po_number`: CharField - Unique number identifying the PO.
- `vendor`: ForeignKey - Link to the Vendor model.
- `order_date`: DateTimeField - Date when the order was placed.
- `delivery_date`: DateTimeField - Expected or actual delivery date of the order.
- `items`: JSONField - Details of items ordered.
- `quantity`: IntegerField - Total quantity of items in the PO.
- `status`: CharField - Current status of the PO (e.g., pending, completed, canceled).
- `quality_rating`: FloatField - Rating given to the vendor for this PO (nullable).
- `issue_date`: DateTimeField - Timestamp when the PO was issued to the vendor.
- `acknowledgment_date`: DateTimeField, nullable - Timestamp when the vendor acknowledged the PO.

### Historical Performance Model
- `vendor`: ForeignKey - Link to the Vendor model.
- `date`: DateTimeField - Date of the performance record.
- `on_time_delivery_rate`: FloatField - Historical record of the on-time delivery rate.
- `quality_rating_avg`: FloatField - Historical record of the quality rating average.
- `average_response_time`: FloatField - Historical record of the average response time.
- `fulfillment_rate`: FloatField - Historical record of the fulfilment rate.

## Setup Instructions

### Prerequisites

- Python 3.8+
- Django 3.2+
- Django REST Framework

### Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/yourusername/vendor-management-system.git
   cd vendor-management-system
