# PharmaCare - Pharmacy Management System

A comprehensive pharmacy management system built with Django that helps pharmacies manage inventory, sales, and customer relationships efficiently.

## Features

### 1. Dashboard
- Real-time sales analytics
- Monthly sales overview
- Weekly sales chart
- Low stock alerts
- Expiry date tracking
- Quick access to key metrics

### 2. Inventory Management
- Add and manage medicines
- Track stock levels
- Batch management with expiry dates
- Low stock notifications
- Brand and category organization
- Stock adjustment history

### 3. Sales Management
- Quick sale processing
- Multiple items per sale
- Customer information tracking
- Prescription attachment
- Sales history
- Daily/Weekly/Monthly reports

### 4. Customer Management
- Customer database
- Purchase history tracking
- Search functionality
- Customer details management
- Prescription records

## Technical Stack

- **Backend**: Django 5.0.3
- **Database**: SQLite/PostgreSQL
- **Frontend**: Bootstrap 5
- **Additional Libraries**:
  - django-crispy-forms
  - django-environ
  - Pillow
  - django-widget-tweaks
  - whitenoise

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/DBMS-Mini-Project.git
cd DBMS-Mini-Project
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env file with your configuration
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Usage

### Initial Setup
1. Log in as admin
2. Add medicine brands and categories
3. Add initial inventory
4. Create staff accounts if needed

### Daily Operations
1. **Sales Processing**:
   - Create new sale
   - Select medicines
   - Add customer details
   - Process payment

2. **Inventory Management**:
   - Check low stock alerts
   - Add new stock
   - Adjust inventory
   - Track expiry dates

3. **Customer Management**:
   - Add new customers
   - View purchase history
   - Update customer information

## Security Features

- User authentication required
- Role-based access control
- Secure password storage
- CSRF protection
- XSS protection
- Environment variable configuration
- Secure cookie handling

## Best Practices

- Regular backups recommended
- Monitor stock levels
- Regular expiry date checks
- Update customer information
- Review sales analytics

## Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- Django community
- Bootstrap team
- All contributors

## Support

For support, please:
1. Check the documentation
2. Create an issue
3. Contact the development team
