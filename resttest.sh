#!/bin/bash
set -Eeuo pipefail
set -x


# Base API URL
BASE_API_URL="http://localhost:8000/api"
BASE_API=$BASE_API_URL
ADMIN_EMAIL="admin@admin.com"
ADMIN_PASSWORD="admin"

staff_id=2  # This stands in for the staff_id to delete, adjust as needed
type_id=1   # Adjust this to match a real type_id in your system
subtype_id=1 # Adjust this to match a real subtype_id in your system
donor_id=1 # Adjust this to match a real donor_id in your system
# Log in and create a new session
echo "Logging in..."
http --session=./session.json --json POST "$BASE_API_URL/staff/login" staff_email='admin@admin.com' staff_password='admin'

# Test: Get all donation types
echo "Getting all types..."
http --session=./session.json GET "$BASE_API_URL/type"

# Test: Register a new donation type with missing field error case
echo "Registering a new type with missing field..."
http --session=./session.json --json POST "$BASE_API_URL/type"

# Test: Register a new donation type (adjust type_name accordingly)
echo "Registering a new type..."
http --session=./session.json --json POST "$BASE_API_URL/type" type_name="Books"

# Test: Get all donation subtypes by type id with wrong type_id
echo "Getting all subtypes with wrong type_id..."
http --session=./session.json GET "$BASE_API_URL/type/sub?type_id="

# Test: Get all donation subtypes by type id
echo "Getting all subtypes for type 1..."
http --session=./session.json GET "$BASE_API_URL/type/sub?type_id=1"

# Test: Register a new donation subtype with missing field error case
echo "Registering a new subtype with missing field..."
http --session=./session.json --json POST "$BASE_API_URL/type/sub"

# Test: Register a new donation subtype (adjust type_id and subtype_name accordingly)
echo "Registering a new subtype..."
http --session=./session.json --json POST "$BASE_API_URL/type/sub" type_id=1 subtype_name="Textbooks"

# Test: Get all staff members
echo "Getting all staff members..."
http --session=./session.json GET "$BASE_API_URL/staff"

# Attempt to access a protected endpoint without login (error case)
echo "Accessing protected endpoint without login..."
http --json GET "$BASE_API_URL/staff"

# Logout after tests
echo "Logging out..."
http --session=./session.json DELETE "$BASE_API_URL/staff/login"

# Attempt logout without an active session (error case)
echo "Logging out without active session..."
http DELETE "$BASE_API_URL/staff/logout"

# Login
echo "Login as admin..."
http --session=./session.json --json POST "${BASE_API}/staff/login" \
    staff_email=$ADMIN_EMAIL staff_password=$ADMIN_PASSWORD

# Register Staff
echo "Registering new staff..."
http --session=./session.json --json POST "${BASE_API}/staff" \
    staff_name="New Staff" staff_email="newstaff@example.com" staff_password="password123"

# Get All Staff
echo "Getting all staff..."
http --session=./session.json GET "${BASE_API}/staff"

# Delete Staff
echo "Deleting staff with id ${staff_id}..."
http --session=./session.json DELETE "${BASE_API}/staff/${staff_id}"

# Add New Donor
echo "Adding a new donor..."
http --session=./session.json --json POST "${BASE_API}/donor" \
    donor_name="John Doe" donor_email="john.doe@example.com"

# Show All Donors
echo "Getting all donors..."
http --session=./session.json GET "${BASE_API}/donor"

# Record Donation
echo "Recording donation..."
http --session=./session.json --json POST "${BASE_API}/donation" \
    donor_id=$donor_id donation_quantity=100 subtype_id=$subtype_id

# Record Distribution
echo "Recording distribution..."
http --session=./session.json --json POST "${BASE_API}/distribution" \
    subtype_id=$subtype_id distribution_amount=50

# Report by Type
echo "Reporting by type..."
http --session=./session.json GET "${BASE_API}/report/type/${type_id}"

# Report by Donor
echo "Reporting by donor..."
http --session=./session.json GET "${BASE_API}/report/donor/${donor_id}"

# Report by Subtype
echo "Reporting by subtype..."
http --session=./session.json GET "${BASE_API}/report/subtype/${subtype_id}"

# Logout
echo "Logging out..."
http --session=./session.json DELETE "${BASE_API}/staff/logout"