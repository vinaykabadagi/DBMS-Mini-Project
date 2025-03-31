# PharmaCare - Pharmacy Management System

A modern, web-based pharmacy management system built with Django and Bootstrap 5. PharmaCare helps pharmacies manage their inventory, sales, and customer relationships efficiently.

## Features

### Dashboard
- Real-time sales analytics
- Daily and monthly sales overview
- Low stock alerts
- Expiring inventory notifications
- Top selling medicines chart

### Inventory Management
- Medicine catalog with detailed information
- Batch-wise stock tracking
- Expiry date monitoring
- Stock adjustment functionality
- Low stock alerts

### Sales Management
- Quick and easy sale creation
- Customer search integration
- Multiple items per sale
- Automatic stock updates
- Payment method tracking
- Complete sale history

### Customer Management
- Customer database
- Purchase history tracking
- Total purchase statistics
- Easy customer search
- Customer details management

## Technical Stack

### Backend
- Django 4.x
- Python 3.x
- SQLite/PostgreSQL

### Frontend
- Bootstrap 5
- Select2 for enhanced dropdowns
- Font Awesome icons
- jQuery for DOM manipulation
- AJAX for dynamic data loading

## Installation

1. Clone the repository:
```bash
git clone https://github.com/vinaykabadagi/DBMS-Mini-Project.git
cd DBMS-Mini-Project
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Apply database migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Usage

### Setting Up Initial Data
- Log in as admin
- Add medicine categories and brands
- Add medicines with their details
- Create initial inventory batches
- Add customers

### Making a Sale
1. Click "New Sale" from the dashboard
2. Select or add a customer
3. Add medicines to the sale
4. Select payment method
5. Complete the sale

### Managing Inventory
- Monitor stock levels from dashboard
- Adjust stock quantities as needed
- Track expiring medicines
- Add new batches when stock arrives

### Customer Management
- Add new customers
- View customer purchase history
- Track customer statistics
- Search customers by name or phone

## Security Features
- User authentication required
- Login protection for all views
- CSRF protection
- Form validation
- Protected customer deletion

## Best Practices
- Optimized database queries
- Proper error handling
- User-friendly messages
- Responsive design
- Clean code structure

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request


## Acknowledgments

- Django framework
- Bootstrap team
- Select2 library
- Font Awesome
- All contributors

## Support

For support, please open an issue in the GitHub repository or contact the development team.
