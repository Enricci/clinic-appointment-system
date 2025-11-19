# Database Seeder Documentation

## Overview

This seeder script populates the clinic appointment system database with sample data for testing and development purposes.

## Usage

To seed the database, run the following command from the `clinic_project` directory:

```bash
python manage.py seed_data
```

## What Gets Created

### Doctors (6 total)

The seeder creates 6 doctors with unique specializations:

1. **Dr. John Smith** - Cardiology

   - Username: `dr_smith`
   - Email: john.smith@clinic.com
   - Phone: +1-555-0101

2. **Dr. Emily Johnson** - Pediatrics

   - Username: `dr_johnson`
   - Email: emily.johnson@clinic.com
   - Phone: +1-555-0102

3. **Dr. Michael Williams** - Orthopedics

   - Username: `dr_williams`
   - Email: michael.williams@clinic.com
   - Phone: +1-555-0103

4. **Dr. Sarah Brown** - Dermatology

   - Username: `dr_brown`
   - Email: sarah.brown@clinic.com
   - Phone: +1-555-0104

5. **Dr. Robert Davis** - Neurology

   - Username: `dr_davis`
   - Email: robert.davis@clinic.com
   - Phone: +1-555-0105

6. **Dr. Maria Martinez** - Ophthalmology
   - Username: `dr_martinez`
   - Email: maria.martinez@clinic.com
   - Phone: +1-555-0106

### Patients (8 total)

- Alice Cooper (alice_cooper@email.com)
- Bob Taylor (bob.taylor@email.com)
- Charlie Wilson (charlie.wilson@email.com)
- Diana Moore (diana.moore@email.com)
- Edward Jackson (edward.jackson@email.com)
- Fiona White (fiona.white@email.com)
- George Harris (george.harris@email.com)
- Hannah Martin (hannah.martin@email.com)

### Appointments (15 total)

- Random appointments spread across the next 30 days
- Various appointment times between 9:00 AM and 4:45 PM
- Different statuses: Pending, Approved, and Completed
- Realistic appointment reasons

### Prescriptions

- Created for completed appointments
- Includes medication names and detailed instructions

## Login Credentials

All seeded users (doctors and patients) use the same password:

**Password:** `password123`

You can log in using any username from the list above with this password.

## Important Notes

⚠️ **Warning:** Running this command will:

- Delete all existing prescriptions
- Delete all existing appointments
- Delete all existing patients
- Delete all existing doctors
- Delete all non-superuser users

Make sure you're running this on a development database, not production!

## Examples

### Login as a Doctor

- Username: `dr_smith`
- Password: `password123`

### Login as a Patient

- Username: `alice_cooper`
- Password: `password123`

## Re-seeding

You can run the seeder multiple times. Each time it runs, it will clear the existing data and create fresh sample data.

## Customization

To modify the seeder, edit the file:

```
clinic_app/management/commands/seed_data.py
```