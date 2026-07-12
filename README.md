# Yaathra - Kerala Travel Planner

A complete full-stack web application for planning trips to Kerala, "God's Own Country". Built with Flask backend and responsive frontend featuring Kerala's beautiful green theme.

## Features

### Core Functionality
- **Destination Exploration**: Browse and discover 6+ Kerala destinations with detailed information
- **Trip Planning**: Intelligent trip planner with budget-based recommendations
- **User Authentication**: Secure login/signup system with password hashing
- **Wishlist System**: Save favorite destinations for future reference
- **User Dashboard**: Personal dashboard with saved trips and wishlist
- **Dynamic Content**: Fully responsive design with smooth animations

### Technical Features
- **Database**: SQLAlchemy ORM with SQLite database
- **Security**: Password hashing, form validation, CSRF protection
- **Responsive Design**: Mobile-first approach with Kerala green theme
- **Animations**: AOS (Animate On Scroll) library integration
- **Modern UI**: Custom CSS with gradients, shadows, and hover effects
- **SEO Optimized**: Semantic HTML5 structure

## Tech Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Database**: SQLite with SQLAlchemy ORM
- **Styling**: Custom CSS (Kerala green theme)
- **Animations**: AOS (Animate On Scroll)
- **Fonts**: Google Fonts (Playfair Display + Poppins)

## Project Structure

```
yaathra/
|
|-- app.py                 # Main Flask application
|-- models.py              # Database models
|-- requirements.txt       # Python dependencies
|-- database.db           # SQLite database (auto-generated)
|
|-- static/
|   |-- css/
|   |   |-- style.css     # Main stylesheet
|   |-- js/
|   |   |-- script.js     # JavaScript functionality
|   |-- images/           # Destination images
|
|-- templates/
|   |-- base.html         # Base template
|   |-- index.html        # Home page
|   |-- explore.html      # Destinations page
|   |-- place_detail.html # Place details
|   |-- plan.html         # Trip planner form
|   |-- plan_result.html  # Generated trip plan
|   |-- login.html        # Login page
|   |-- signup.html       # Registration page
|   |-- dashboard.html    # User dashboard
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Instructions

1. **Clone or Download the Project**
   ```bash
   cd yaathra
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Application**
   ```bash
   python app.py
   ```

5. **Access the Application**
   Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Available Destinations

The application comes pre-loaded with 6 Kerala destinations:

1. **Munnar** - Hill station with tea plantations
2. **Wayanad** - Nature and wildlife paradise  
3. **Kovalam** - Beautiful beach destination
4. **Alleppey** - Backwaters and houseboats
5. **Kumarakom** - Bird sanctuary and backwaters
6. **Thekkady** - Wildlife sanctuary

## Features Overview

### Home Page
- Hero section with Kerala background
- Featured destinations carousel
- Quick action buttons
- Kerala highlights section

### Explore Page
- Grid layout of all destinations
- Search functionality
- Category filters (Beach, Hill, Nature)
- Wishlist integration

### Place Detail Page
- Comprehensive destination information
- Activities, food, and culture sections
- Interactive Google Maps
- Budget and timing information
- Add to wishlist functionality

### Trip Planner
- Multi-step form with validation
- Budget-based recommendations
- Interest-based suggestions
- Dynamic itinerary generation
- Day-wise planning

### User Dashboard
- Trip statistics
- Saved trip plans
- Wishlist management
- Quick actions
- Personalized recommendations

### Authentication
- Secure user registration
- Password hashing
- Session management
- Protected routes

## Database Schema

### Users Table
- id, username, email, password_hash, created_at

### Places Table  
- id, name, title, description, image, category, activities, food, culture, best_time, avg_budget

### Trips Table
- id, user_id, destination, days, budget, interests, plan_text, created_at

### Wishlist Table
- id, user_id, place_id, created_at

## Customization

### Adding New Destinations
1. Add destination data to `DESTINATIONS` dictionary in `app.py`
2. Add corresponding image to `static/images/`
3. Restart the application

### Theme Customization
- Edit CSS variables in `static/css/style.css`
- Primary Kerala green: `#2e7d32`
- Adjust colors, fonts, and spacing as needed

### Adding New Features
- Add routes in `app.py`
- Create corresponding templates
- Update models if database changes needed
- Add JavaScript functionality in `script.js`

## API Endpoints

### Public Routes
- `GET /` - Home page
- `GET /explore` - Explore destinations
- `GET /place/<place_name>` - Place details
- `GET /plan` - Trip planner form
- `POST /plan` - Generate trip plan
- `GET /login` - Login page
- `POST /login` - User login
- `GET /signup` - Registration page
- `POST /signup` - User registration

### Protected Routes (Login Required)
- `GET /dashboard` - User dashboard
- `POST /add_to_wishlist/<place_name>` - Add to wishlist
- `POST /remove_from_wishlist/<place_name>` - Remove from wishlist
- `GET /logout` - User logout

## Security Features

- Password hashing with Werkzeug
- Session-based authentication
- Form validation and sanitization
- CSRF protection ready
- SQL injection prevention with SQLAlchemy
- XSS protection with Jinja2 auto-escaping

## Performance Optimizations

- Lazy loading for images
- Debounced search functionality
- Efficient database queries
- CSS animations instead of JavaScript where possible
- Responsive image handling

## Browser Support

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Development

### Running in Development Mode
```bash
export FLASK_ENV=development  # On macOS/Linux
set FLASK_ENV=development     # On Windows
python app.py
```

### Database Reset
```bash
rm database.db
python app.py
```

### Adding Dependencies
```bash
pip install package_name
pip freeze > requirements.txt
```

## Deployment

### Production Setup
1. Set environment variables:
   ```bash
   export FLASK_ENV=production
   export SECRET_KEY=your-secret-key
   ```

2. Use production WSGI server:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

3. Configure reverse proxy (Nginx/Apache)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Troubleshooting

### Common Issues

**Database Error**
- Delete `database.db` and restart the application

**Port Already in Use**
- Change port in `app.py` or kill existing process

**Static Files Not Loading**
- Check file paths in templates
- Ensure `static/` folder structure is correct

**Templates Not Found**
- Verify `templates/` folder exists
- Check template names in route definitions

## Future Enhancements

- [ ] Real hotel booking integration
- [ ] Payment gateway integration
- [ ] Mobile app development
- [ ] Social media sharing
- [ ] Advanced filtering options
- [ ] User reviews and ratings
- [ ] Multi-language support
- [ ] Email notifications
- [ ] Admin dashboard
- [ ] API documentation

## Support

For support and questions:
- Email: info@yaathra.com
- Phone: +91 98765 43210

## License

This project is for educational purposes. Feel free to use and modify according to your needs.

---

**Yaathra - Your Gateway to Kerala's Beauty**
