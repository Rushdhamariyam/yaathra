# Yaathra - Kerala Travel Planner
# Complete Flask Application - All Python files combined

# ===== IMPORTS =====
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json
from datetime import datetime
from functools import wraps

# ===== APP CONFIGURATION =====
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yaathra_kerala_travel_planner_secret_key_2024'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db = SQLAlchemy(app)

# ===== CUSTOM FILTERS =====
@app.template_filter('from_json')
def from_json(value):
    return json.loads(value) if value else []

# ===== DATASET - ALL 14 KERALA DISTRICTS =====
all_places_dict = {}

# Part 1: First 3 districts
all_places_dict.update({
    "thiruvananthapuram": {
        "title": "Thiruvananthapuram",
        "image": "kovalam.jpg",
        "category": "city",
        "description": "Thiruvananthapuram, the capital of Kerala, is rich in culture and history. It is famous for the Padmanabhaswamy Temple and scenic beaches like Kovalam and Shanghumugham. The city offers vibrant local markets and delicious Kerala cuisine, including Sadya and seafood dishes. Visitors can explore museums, cultural landmarks, and nearby hill stations. October to March is the best time to visit for pleasant weather and festivals. Thiruvananthapuram beautifully blends spiritual heritage, natural beauty, and modern city life.",
        "activities": ["Kovalam Beach", "Temple visit", "Napier Museum", "Zoo visit"],
        "food": ["Seafood", "Kerala Sadya", "Appam & stew"],
        "culture": ["Classical dance", "Temple traditions", "Festivals"],
        "best_time": "October to March",
        "weather": "28°C - 35°C",
        "budget": "Medium",
        "hotels": [
            {"name": "Hilton Garden Inn", "price": 7000, "rating": 4.5},
            {"name": "Vivanta Trivandrum", "price": 8500, "rating": 4.6},
            {"name": "Uday Suites", "price": 5000, "rating": 4.3}
        ]
    },
    "kollam": {
        "title": "Kollam",
        "image": "beaches.jpg",
        "category": "water",
        "description": "Kollam is a historic coastal city known as the gateway to Kerala's backwaters. It features the beautiful Ashtamudi Lake, perfect for houseboat experiences and scenic views. The city is famous for its cashew industry and traditional coir products. Visitors can explore Thangassery Beach with its historic lighthouse and Portuguese fort ruins. The local cuisine offers delicious seafood and traditional Kerala Sadya. September to March is ideal for pleasant weather and cultural festivals.",
        "activities": ["Houseboat ride", "Beach visit", "Lake cruise"],
        "food": ["Seafood", "Fish curry", "Kerala meals"],
        "culture": ["Fishing traditions", "Cashew industry"],
        "best_time": "September to March",
        "weather": "26°C - 32°C",
        "budget": "Low",
        "hotels": [
            {"name": "The Raviz Kollam", "price": 6000, "rating": 4.5},
            {"name": "All Season Hotel", "price": 2500, "rating": 4.0},
            {"name": "Fragrant Nature", "price": 4500, "rating": 4.2}
        ]
    },
    "pathanamthitta": {
        "title": "Pathanamthitta",
        "image": "nature.jpg",
        "category": "nature",
        "description": "Pathanamthitta is known as the Pilgrim Capital of Kerala, famous for the sacred Sabarimala Temple. The district features the holy Pamba River and lush green forests of the Western Ghats. Visitors can explore ancient temples like Aranmula Parthasarathy with its beautiful murals. The region offers authentic Kerala cuisine, especially traditional vegetarian Sadya. November to February provides the best weather for pilgrimage and sightseeing. Pathanamthitta combines spiritual tranquility with natural beauty.",
        "activities": ["Forest trekking", "Pilgrimage", "Nature walks"],
        "food": ["Traditional Kerala meals", "Vegetarian cuisine"],
        "culture": ["Religious traditions", "Temple festivals"],
        "best_time": "November to April",
        "weather": "22°C - 30°C",
        "budget": "Low",
        "hotels": [
            {"name": "Hotel Hills Park", "price": 2000, "rating": 3.9},
            {"name": "Green Valley Resort", "price": 3000, "rating": 4.1},
            {"name": "Sabarimala Residency", "price": 2500, "rating": 4.0}
        ]
    },
})

# Part 2: Next 3 districts
all_places_dict.update({
    "alappuzha": {
        "title": "Alappuzha",
        "image": "alleppey.jpg",
        "category": "water",
        "description": "Alappuzha, known as the Venice of the East, is famous for its beautiful backwaters and houseboats. The district offers enchanting cruises through serene waters surrounded by lush paddy fields. Visitors can enjoy the famous Nehru Trophy Boat Race and explore historic Krishnapuram Palace. The local cuisine features delicious seafood and traditional Kerala dishes. October to February provides ideal weather for backwater experiences. Alappuzha perfectly combines natural beauty with traditional Kerala lifestyle.",
        "activities": ["Houseboat stay", "Backwater cruise", "Village tour"],
        "food": ["Karimeen fry", "Prawn curry", "Toddy"],
        "culture": ["Snake boat race", "Coir industry"],
        "best_time": "November to February",
        "weather": "27°C - 33°C",
        "budget": "Medium",
        "hotels": [
            {"name": "Houseboat Deluxe", "price": 5000, "rating": 4.6},
            {"name": "Ramada Alleppey", "price": 4500, "rating": 4.3},
            {"name": "Punnamada Resort", "price": 4000, "rating": 4.2}
        ]
    },
    "kottayam": {
        "title": "Kottayam",
        "image": "kumarakom.jpg",
        "category": "nature",
        "description": "Kottayam, known as the Land of Letters, Lakes, and Latex, is celebrated for its educational excellence and natural beauty. The district features the beautiful Kumarakom backwaters and the vast Vembanad Lake. Visitors can explore ancient churches like St. Mary's Church and traditional rubber plantations. The local cuisine blends Kerala flavors with Syrian Christian influences. September to March offers pleasant weather for exploration. Kottayam perfectly combines education, nature, and cultural heritage.",
        "activities": ["Backwater tours", "Village visits", "Rubber plantations"],
        "food": ["Traditional meals", "Fish curry"],
        "culture": ["Literary culture", "Festivals"],
        "best_time": "September to March",
        "weather": "26°C - 32°C",
        "budget": "Medium",
        "hotels": [
            {"name": "Hotel Arcadia", "price": 3000, "rating": 4.1},
            {"name": "Backwater Breeze", "price": 3500, "rating": 4.2},
            {"name": "Coconut Lagoon Resort", "price": 6000, "rating": 4.5}
        ]
    },
    "idukki": {
        "title": "Idukki",
        "image": "munnar.jpg",
        "category": "hill",
        "description": "Idukki is a picturesque hill district renowned for its stunning landscapes and wildlife sanctuaries. The district features the magnificent Idukki Arch Dam and the beautiful Munnar tea gardens. Visitors can explore the Periyar Tiger Reserve and enjoy spice plantation tours. The local cuisine includes traditional Kerala dishes with hill station flavors. September to March provides ideal weather for sightseeing. Idukki offers a perfect blend of natural beauty and cultural richness.",
        "activities": ["Trekking", "Idukki dam visit", "Wildlife safari"],
        "food": ["Local tribal cuisine", "Kerala meals"],
        "culture": ["Tribal traditions", "Eco-tourism"],
        "best_time": "September to March",
        "weather": "15°C - 25°C",
        "budget": "Medium",
        "hotels": [
            {"name": "Spice Village", "price": 7000, "rating": 4.6},
            {"name": "Mountain Resort", "price": 4000, "rating": 4.3},
            {"name": "Green Hill Stay", "price": 2800, "rating": 4.0}
        ]
    },
})

# Part 3: Next 3 districts
all_places_dict.update({
    "ernakulam": {
        "title": "Ernakulam",
        "image": "kochi.jpg",
        "category": "city",
        "description": "Ernakulam, the commercial capital of Kerala, blends modern urban life with rich cultural heritage. The district features historic Fort Kochi with Portuguese architecture and iconic Chinese fishing nets. Visitors can explore the ancient Jewish Synagogue and enjoy sunset views at Marine Drive. The local cuisine is famous for Malabar Biryani and seafood delicacies. October to March offers ideal weather for exploration. Ernakulam perfectly combines historical significance with modern amenities.",
        "activities": ["Shopping", "Fort Kochi", "Marine Drive"],
        "food": ["Seafood", "Street food", "Fusion cuisine"],
        "culture": ["Colonial heritage", "Art cafes"],
        "best_time": "October to March",
        "weather": "27°C - 33°C",
        "budget": "High",
        "hotels": [
            {"name": "Grand Hyatt Kochi", "price": 9000, "rating": 4.7},
            {"name": "Ibis Kochi", "price": 4000, "rating": 4.2},
            {"name": "Le Meridien", "price": 7000, "rating": 4.5}
        ]
    },
    "thrissur": {
        "title": "Thrissur",
        "image": "nature.jpg",
        "category": "city",
        "description": "Thrissur, the cultural capital of Kerala, is renowned for its vibrant festivals and rich artistic heritage. The district features the famous Vadakkunnathan Temple and the prestigious Kerala Kalamandalam. Visitors can experience the spectacular Thrissur Pooram festival and explore the sacred Guruvayur Temple. The local cuisine offers traditional Kerala Sadya and temple prasadam. October to March provides ideal weather for cultural experiences. Thrissur stands as the beating heart of Kerala's cultural traditions.",
        "activities": ["Temple visits", "Zoo", "Museum"],
        "food": ["Kerala Sadya", "Snacks"],
        "culture": ["Pooram festival", "Classical arts"],
        "best_time": "September to March",
        "weather": "26°C - 32°C",
        "budget": "Medium",
        "hotels": [
            {"name": "Joys Palace", "price": 4500, "rating": 4.3},
            {"name": "Hotel Luciya", "price": 2500, "rating": 4.0},
            {"name": "Casino Hotel", "price": 3500, "rating": 4.2}
        ]
    },
    "palakkad": {
        "title": "Palakkad",
        "image": "nature.jpg",
        "category": "nature",
        "description": "Palakkad, known as the Gateway of Kerala, is blessed with natural beauty and historical significance. The district features the majestic Palakkad Fort and the pristine Silent Valley National Park. Visitors can explore the beautiful Malampuzha Gardens and scenic Nelliyampathy hills. The local cuisine offers authentic Kerala dishes with regional specialties. September to March provides ideal weather for exploration. Palakkad perfectly blends historical heritage with natural splendor.",
        "activities": ["Fort visit", "Malampuzha dam", "Nature walks"],
        "food": ["Rice dishes", "Vegetarian meals"],
        "culture": ["Agricultural traditions"],
        "best_time": "October to March",
        "weather": "28°C - 36°C",
        "budget": "Medium",
        "hotels": [
            {"name": "KPM Regency", "price": 3000, "rating": 4.1},
            {"name": "Hotel Indraprastha", "price": 2500, "rating": 4.0},
            {"name": "Au Revoir Wellness Resort", "price": 5000, "rating": 4.4}
        ]
    }
})

# Part 4: Next 3 districts
all_places_dict.update({
    "malappuram": {
        "title": "Malappuram",
        "image": "beaches.jpg",
        "category": "nature",
        "description": "Malappuram, a district of hills and rivers, is renowned for its rich cultural heritage. The district features the ancient Nilambur Teak Plantations and the beautiful Kadalundi Bird Sanctuary. Visitors can explore historic mosques and enjoy the scenic beauty of rolling hills. The local cuisine offers authentic Malabar dishes with distinctive flavors. October to March provides ideal weather for cultural exploration. Malappuram perfectly blends cultural richness with natural splendor.",
        "activities": ["Hill visits", "River tourism"],
        "food": ["Malabar biryani", "Pathiri"],
        "culture": ["Mappila culture", "Festivals"],
        "best_time": "September to March",
        "weather": "25°C - 34°C",
        "budget": "Medium",
        "hotels": [
            {"name": "Hotel Rydges", "price": 3000, "rating": 4.1},
            {"name": "Malabar Residency", "price": 2500, "rating": 4.0},
            {"name": "Emarald Resort", "price": 4000, "rating": 4.2}
        ]
    },
    "kozhikode": {
        "title": "Kozhikode",
        "image": "beaches.jpg",
        "category": "beach",
        "description": "Kozhikode, historically known as Calicut, is a vibrant coastal city celebrated for its rich heritage. The city features beautiful beaches like Kozhikode and Beypore, perfect for sunset viewing. Visitors can explore the historic Mananchira Square and the ancient Tali Shiva Temple. The local cuisine is renowned for Malabar Biryani and seafood delicacies. October to March provides ideal weather for exploration. Kozhikode perfectly blends historical significance with culinary excellence.",
        "activities": ["Beach visit", "Shopping", "Food tours"],
        "food": ["Kozhikode biryani", "Halwa", "Seafood"],
        "culture": ["Trade history", "Food culture"],
        "best_time": "September to March",
        "weather": "28°C - 34°C",
        "budget": "Medium",
        "hotels": [
            {"name": "The Raviz Calicut", "price": 6000, "rating": 4.5},
            {"name": "Hotel Malabar Palace", "price": 3500, "rating": 4.2},
            {"name": "Westway Hotel", "price": 3000, "rating": 4.1}
        ]
    },
    "wayanad": {
        "title": "Wayanad",
        "image": "wayanad.jpg",
        "category": "nature",
        "description": "Wayanad is a picturesque hill district renowned for its stunning landscapes and ancient caves. The district features the prehistoric Edakkal Caves and the beautiful Chembra Peak with its heart-shaped lake. Visitors can explore the Wayanad Wildlife Sanctuary and enjoy spice plantation tours. The local cuisine includes traditional Kerala dishes with tribal influences. October to March provides ideal weather for exploration. Wayanad offers a perfect blend of natural beauty and archaeological significance.",
        "activities": ["Edakkal caves", "Waterfalls", "Trekking"],
        "food": ["Local cuisine", "Spice dishes"],
        "culture": ["Tribal heritage", "Eco tourism"],
        "best_time": "October to May",
        "weather": "20°C - 28°C",
        "budget": "Medium",
        "hotels": [
            {"name": "Wayanad Wild", "price": 4500, "rating": 4.6},
            {"name": "Green Gates", "price": 2800, "rating": 4.1},
            {"name": "Vythiri Village", "price": 6500, "rating": 4.5}
        ]
    }
})

# Part 5: Final 2 districts
all_places_dict.update({
    "kannur": {
        "title": "Kannur",
        "image": "beaches.jpg",
        "category": "beach",
        "description": "Kannur is a historic coastal district renowned for its pristine beaches and cultural traditions. The district features the majestic St. Angelo's Fort and the beautiful Payyambalam Beach. Visitors can experience traditional Theyyam performances and explore the world-famous handloom industry. The local cuisine offers fresh seafood and traditional Kerala dishes. October to March provides ideal weather for cultural experiences. Kannur perfectly blends historical significance with coastal beauty.",
        "activities": ["Beach", "Theyyam festival", "Fort visit"],
        "food": ["Seafood", "Kerala meals"],
        "culture": ["Theyyam ritual", "Handloom"],
        "best_time": "September to March",
        "weather": "27°C - 33°C",
        "budget": "Medium",
        "hotels": [
            {"name": "Mascot Beach Resort", "price": 4000, "rating": 4.2},
            {"name": "Hotel Blue Nile", "price": 2500, "rating": 4.0},
            {"name": "Seashell Haris Beach Home", "price": 3500, "rating": 4.3}
        ]
    },
    "kasaragod": {
        "title": "Kasaragod",
        "image": "beaches.jpg",
        "category": "beach",
        "description": "Kasaragod, the northernmost district of Kerala, is renowned for its ancient forts and cultural heritage. The district features the magnificent Bekal Fort and the beautiful Bekal and Chandragiri beaches. Visitors can experience traditional Theyyam performances and explore the ancient Madhur Temple. The local cuisine offers delicious Malabar dishes with distinctive flavors. October to March provides ideal weather for exploration. Kasaragod perfectly blends historical significance with coastal beauty.",
        "activities": ["Bekal Fort", "Beach walk"],
        "food": ["Malabar cuisine", "Seafood"],
        "culture": ["Multilingual traditions"],
        "best_time": "September to March",
        "weather": "28°C - 35°C",
        "budget": "Low",
        "hotels": [
            {"name": "Taj Bekal Resort", "price": 10000, "rating": 4.8},
            {"name": "Bekal Palace", "price": 5000, "rating": 4.3},
            {"name": "Neeleshwar Hermitage", "price": 8000, "rating": 4.6}
        ]
    }
})

# Use imported dataset
ALL_PLACES = all_places_dict

# Validation - Print length of dictionary
print(f"Dataset created with {len(ALL_PLACES)} districts")

# ===== DATABASE MODELS =====
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    image = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    activities = db.Column(db.Text)  # JSON string
    food = db.Column(db.Text)  # JSON string
    culture = db.Column(db.Text)  # JSON string
    best_time = db.Column(db.String(100))
    weather = db.Column(db.String(100))
    avg_budget = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship with hotels
    hotels = db.relationship('Hotel', backref='place', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'title': self.title,
            'description': self.description,
            'image': self.image,
            'category': self.category,
            'activities': json.loads(self.activities) if self.activities else [],
            'food': json.loads(self.food) if self.food else [],
            'culture': json.loads(self.culture) if self.culture else [],
            'best_time': self.best_time,
            'weather': self.weather,
            'avg_budget': self.avg_budget
        }

class Hotel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(200))  # Hotel image field
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    reviews = db.relationship('Review', back_populates='hotel', cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'rating': self.rating,
            'image': self.image,
            'place_id': self.place_id
        }

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    hotel_id = db.Column(db.Integer, db.ForeignKey('hotel.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    hotel = db.relationship('Hotel', back_populates='reviews')
    user = db.relationship('User', backref='user_reviews')
    
    def to_dict(self):
        return {
            'id': self.id,
            'rating': self.rating,
            'comment': self.comment,
            'hotel_id': self.hotel_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat()
        }

class Trip(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(100), nullable=False)
    days = db.Column(db.Integer, nullable=False)
    budget = db.Column(db.String(50), nullable=False)
    interests = db.Column(db.Text)  # JSON string
    plan_text = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'destination': self.destination,
            'days': self.days,
            'budget': self.budget,
            'interests': json.loads(self.interests) if self.interests else [],
            'plan_text': self.plan_text,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat()
        }

class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'created_at': self.created_at.isoformat()
        }

# ===== HELPER FUNCTIONS =====

def validate_place_images(places):
    """
    Helper to ensure list of places or a single place has a verified image attribute.
    If place.image is not set, or the file doesn't exist on disk, fall back to 'nature.jpg'.
    """
    import os
    if not places:
        return
    
    # Handle single object
    if not isinstance(places, list):
        places_list = [places]
    else:
        places_list = places
        
    for place in places_list:
        if not place:
            continue
            
        # Ensure image key/attribute exists
        if hasattr(place, 'image'):
            if not place.image:
                place.image = 'nature.jpg'
        elif isinstance(place, dict):
            if 'image' not in place or not place['image']:
                place['image'] = 'nature.jpg'
        else:
            try:
                place.image = 'nature.jpg'
            except Exception:
                pass
                
        # Now check file existence on disk
        img_name = getattr(place, 'image', None) or (place.get('image') if isinstance(place, dict) else None)
        if img_name:
            direct_path = os.path.join(app.root_path, 'static', 'images', img_name)
            if not os.path.exists(direct_path):
                found = False
                images_dir = os.path.join(app.root_path, 'static', 'images')
                if os.path.exists(images_dir):
                    for root, dirs, files in os.walk(images_dir):
                        if img_name in files:
                            found = True
                            break
                if not found:
                    if hasattr(place, 'image'):
                        place.image = 'nature.jpg'
                    elif isinstance(place, dict):
                        place['image'] = 'nature.jpg'

# Destination Folder Mapping Dictionary
# Maps database place names to actual folder names in static/images/
FOLDER_MAPPING = {
    "thiruvananthapuram": "thiruvananthapuram",
    "kollam": "kollam",
    "pathanamthitta": "pathanamthitta",
    "alappuzha": "alleppey",
    "kottayam": "kottayam",
    "idukki": "munnar",
    "ernakulam": "kochi",
    "thrissur": "thrissur",
    "palakkad": "palakkad",
    "malappuram": "malappuram",
    "kozhikode": "kozhikode",
    "wayanad": "wayanad",
    "kannur": "kannur",
    "kasaragod": "kasaragod",
    # Alternative mappings for common variations
    "munnar": "munnar",
    "kochi": "kochi",
    "alleppey": "alleppey",
    "varkala": "varkala",
    "thekkady": "thekkady",
    "kovalam": "kovalam",
    "bekal": "bekal",
    "vagamon": "vagamon",
    "athirappilly": "athirappilly"
}

def get_place_images(place_name, limit=6):
    """
    Get images for a place by reading from the actual folder structure
    
    Args:
        place_name: Name of the place from database
        limit: Maximum number of images to return
    
    Returns:
        List of image paths relative to static/images/
    """
    import os
    
    # Convert place name to folder name
    folder_name = FOLDER_MAPPING.get(place_name.lower(), place_name.lower())
    
    # Construct full folder path
    folder_path = os.path.join('static', 'images', folder_name)
    
    print(f"DEBUG: get_place_images - place_name: {place_name}, folder_name: {folder_name}, folder_path: {folder_path}")
    
    # Check if folder exists
    if not os.path.exists(folder_path):
        print(f"DEBUG: Folder does not exist: {folder_path}")
        # Return fallback images
        return [f"images/default/default{i+1}.jpg" for i in range(min(limit, 3))]
    
    # List all files in folder
    try:
        all_files = os.listdir(folder_path)
        print(f"DEBUG: Files in folder: {all_files}")
        
        # Filter for image files only
        image_files = []
        for file in all_files:
            if file.lower().endswith(('.jpg', '.jpeg', '.png')):
                image_files.append(file)
        
        print(f"DEBUG: Image files found: {image_files}")
        
        # Sort files to ensure consistent ordering
        image_files.sort()
        
        # Limit the number of images
        image_files = image_files[:limit]
        
        # Construct relative paths
        image_paths = [f"images/{folder_name}/{file}" for file in image_files]
        
        print(f"DEBUG: Returning image paths: {image_paths}")
        return image_paths
        
    except Exception as e:
        print(f"DEBUG: Error reading folder: {str(e)}")
        # Return fallback images
        return [f"images/default/default{i+1}.jpg" for i in range(min(limit, 3))]

def get_hero_image(place_name):
    """
    Get hero image for a place
    
    Args:
        place_name: Name of the place from database
    
    Returns:
        Hero image path relative to static/
    """
    images = get_place_images(place_name, limit=1)
    if images:
        return images[0]
    return "images/default/default1.jpg"

def get_itinerary_image(place_name, day_number):
    """
    Get image for itinerary day
    
    Args:
        place_name: Name of the place
        day_number: Day number (1, 2, 3, etc.)
    
    Returns:
        Itinerary image path relative to static/
    """
    images = get_place_images(place_name, limit=10)
    if images and len(images) > 0:
        # Cycle through images based on day number
        image_index = (day_number - 1) % len(images)
        return images[image_index]
    return "images/default/default1.jpg"

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login to access this page', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def generate_trip_plan(destination, days, budget, travelers, interests):
    """Generate a dynamic trip plan based on user preferences"""
    print(f"DEBUG: generate_trip_plan called with destination: {destination}, days: {days}, budget: {budget}, travelers: {travelers}, interests: {interests}")
    
    try:
        # Case-insensitive place search
        print("DEBUG: Searching for place in database")
        place = Place.query.filter(Place.name.ilike(destination.lower())).first()
        
        if not place:
            print(f"DEBUG: Place '{destination}' not found in database")
            # Try searching by title as fallback
            place = Place.query.filter(Place.title.ilike(f"%{destination}%")).first()
            if not place:
                print(f"DEBUG: Place '{destination}' not found by title search either")
                return None
        
        validate_place_images(place)
        print(f"DEBUG: Found place: {place.title}")
        
        # Get hotels for the destination
        print("DEBUG: Fetching hotels for the destination")
        hotels = Hotel.query.filter_by(place_id=place.id).all()
        print(f"DEBUG: Found {len(hotels)} hotels")
        
        # Filter hotels based on budget with improved logic
        recommended_hotels = []
        budget_lower = budget.lower()
        
        print(f"DEBUG: Filtering hotels for budget: {budget_lower}")
        for hotel in hotels:
            try:
                # Extract numeric value from price string
                price_str = hotel.price.replace(',', '').replace('₹', '').strip()
                price_value = int(price_str)
                
                if budget_lower == 'low' and price_value <= 4000:
                    recommended_hotels.append(hotel)
                elif budget_lower == 'medium' and 4000 < price_value <= 7000:
                    recommended_hotels.append(hotel)
                elif budget_lower == 'high' and price_value > 7000:
                    recommended_hotels.append(hotel)
            except (ValueError, AttributeError):
                print(f"DEBUG: Could not parse price for hotel: {hotel.name}")
                continue
        
        print(f"DEBUG: Found {len(recommended_hotels)} recommended hotels")
        
        # If no hotels match budget, return all hotels sorted by price
        if not recommended_hotels:
            print("DEBUG: No hotels matched budget, returning all hotels")
            recommended_hotels = hotels
        
        # Get activities from place
        print("DEBUG: Getting place activities")
        try:
            activities = place.activities if place.activities else ['Sightseeing', 'Local experiences', 'Cultural activities', 'Relaxation']
            if isinstance(activities, str):
                activities = json.loads(activities)
            print(f"DEBUG: Activities: {activities}")
        except (json.JSONDecodeError, AttributeError) as e:
            print(f"DEBUG: Error parsing activities: {e}")
            activities = ['Sightseeing', 'Local experiences', 'Cultural activities', 'Relaxation']
        
        # Generate day-wise itinerary with images using new helper function
        print("DEBUG: Generating day-wise itinerary with images")
        itinerary = []
        
        for day in range(1, days + 1):
            if day == 1:
                title = f"Arrival at {place.title}"
                description = "Check-in, local exploration, and getting settled in"
            elif day == days:
                title = f"Final Day in {place.title}"
                description = "Final sightseeing, shopping, and departure preparation"
            else:
                activity = activities[(day-2) % len(activities)]
                title = f"Day {day}: {activity}"
                description = f"Experience {activity} in {place.title}"
            
            # Get image using new helper function
            image = get_itinerary_image(place.name, day)
            print(f"DEBUG: Day {day} - title: {title}, image: {image}")
            
            itinerary.append({
                'day': f"Day {day}",
                'title': title,
                'description': description,
                'image': image
            })
        
        print(f"DEBUG: Generated itinerary with {len(itinerary)} days")
        
        # Budget breakdown
        budget_breakdown = {
            'accommodation': '40%',
            'food': '25%',
            'transportation': '20%',
            'activities': '15%'
        }
        
        # Suggested activities based on interests
        suggested_activities = []
        if interests:
            print("DEBUG: Processing interests")
            interests_list = [interest.strip().lower() for interest in interests.split(',')]
            print(f"DEBUG: Interests list: {interests_list}")
            
            for interest in interests_list:
                if interest in ['adventure', 'adventurous']:
                    suggested_activities.extend(['Trekking', 'Wildlife Safari', 'Water Sports'])
                elif interest in ['culture', 'cultural']:
                    suggested_activities.extend(['Temple Visits', 'Museum Tours', 'Cultural Shows'])
                elif interest in ['nature', 'natural']:
                    suggested_activities.extend(['Nature Walks', 'Bird Watching', 'Photography'])
                elif interest in ['food', 'cuisine']:
                    suggested_activities.extend(['Food Tours', 'Cooking Classes', 'Local Markets'])
        
        if not suggested_activities:
            print("DEBUG: No specific interests, using default activities")
            suggested_activities = activities[:4]
        
        print(f"DEBUG: Suggested activities: {suggested_activities}")
        
        # Prepare hotel data for template
        hotels_data = [h.to_dict() for h in recommended_hotels[:3]]
        print(f"DEBUG: Prepared {len(hotels_data)} hotels for template")
        
        result = {
            'place': place.to_dict(),
            'itinerary': itinerary,
            'budget_breakdown': budget_breakdown,
            'suggested_activities': suggested_activities,
            'hotels': hotels_data,
            'travelers': travelers
        }
        
        print("DEBUG: Trip plan generated successfully")
        return result
        
    except Exception as e:
        print(f"DEBUG: Error in generate_trip_plan: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

def create_tables():
    """Create database tables and populate with initial data"""
    with app.app_context():
        # Drop all tables first to ensure clean start
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Populate places from all_places_dict
        for key, place_data in all_places_dict.items():
            place = Place(
                name=key,
                title=place_data['title'],
                description=place_data['description'],
                image=place_data['image'],
                category=place_data['category'],
                activities=json.dumps(place_data['activities']),
                food=json.dumps(place_data['food']),
                culture=json.dumps(place_data['culture']),
                best_time=place_data.get('best_time', 'October to March'),
                weather=place_data.get('weather', '25°C - 35°C'),
                avg_budget=place_data.get('budget', 'Medium')
            )
            db.session.add(place)
        
        db.session.commit()
        
        # Add hotels for each place
        for key, place_data in all_places_dict.items():
            place = Place.query.filter_by(name=key).first()
            if place and 'hotels' in place_data:
                for hotel_data in place_data['hotels']:
                    hotel = Hotel(
                        name=hotel_data['name'],
                        price=str(hotel_data['price']),
                        rating=hotel_data['rating'],
                        image=hotel_data.get('image', ''),  # Add image field
                        place_id=place.id
                    )
                    db.session.add(hotel)
        
        db.session.commit()
        print("Database initialized with sample data")

# ===== UTILITY FUNCTIONS FOR UPDATING DESCRIPTIONS =====

# 10-sentence descriptions for all places
ten_sentence_descriptions = {
    "thiruvananthapuram": "Thiruvananthapuram, the capital of Kerala, is a vibrant city blending tradition and modernity. It is renowned for the Padmanabhaswamy Temple, a magnificent landmark with intricate architecture. Kovalam Beach offers golden sands and serene sunsets, perfect for relaxation and water activities. Shanghumugham Beach is a favorite spot for evening strolls and witnessing spectacular sunsets. The Napier Museum and Kerala Science and Technology Museum showcase the city's rich cultural heritage. The city's cuisine includes delicious Kerala Sadya and local seafood delicacies. October to March is the best time to visit, with pleasant weather and festive celebrations. The local markets are full of handicrafts, textiles, and souvenirs for tourists. Visitors can explore nearby hill stations and backwaters for scenic experiences. Thiruvananthapuram beautifully combines spiritual, cultural, and natural attractions in one city.",
    
    "kollam": "Kollam, a historic coastal city, serves as the gateway to Kerala's magnificent backwaters. The city is famous for Ashtamudi Lake, the second largest lake in Kerala, offering breathtaking houseboat experiences. Thangassery Beach features a historic lighthouse and ancient Portuguese fort ruins. The city's cashew industry is renowned worldwide, making it the Cashew Capital of Kerala. Kollam's traditional Kerala architecture and ancient temples reflect its rich cultural heritage. The local cuisine includes delicious seafood specialties and traditional Kerala Sadya. September to March is the ideal time to visit when the weather is pleasant and perfect for exploration. The city hosts vibrant festivals like Kollam Pooram, showcasing traditional Kerala culture. Visitors can enjoy shopping for spices, tea, and local handicrafts in the bustling markets. Kollam perfectly combines historical significance with natural beauty and cultural richness.",
    
    "pathanamthitta": "Pathanamthitta, known as the 'Pilgrim Capital of Kerala,' is a serene district famous for spiritual significance. The district is home to the renowned Sabarimala Temple, one of the largest pilgrimage sites in the world. The Pamba River flows through the district, offering scenic beauty and sacred bathing spots for pilgrims. The region is blessed with lush green forests and diverse wildlife in its numerous reserve forests. Pathanamthitta's cultural heritage is reflected in its traditional Kerala architecture and ancient temples. The local cuisine features authentic Kerala Sadya and traditional vegetarian dishes. November to February is the best time to visit, with pleasant weather ideal for pilgrimage and sightseeing. The district hosts the famous Aranmula Boat Race during Onam festival, showcasing Kerala's cultural traditions. Visitors can explore the ancient Aranmula Parthasarathy Temple, known for its intricate murals. Pathanamthitta offers a perfect blend of spiritual tranquility and natural beauty for visitors.",
    
    "alappuzha": "Alappuzha, famously known as the 'Venice of the East,' is a picturesque district renowned for its intricate backwater network. The district offers enchanting houseboat cruises through serene backwaters, surrounded by lush green paddy fields. The Alappuzha Beach features a historic pier and beautiful lighthouse, perfect for sunset viewing. The Nehru Trophy Boat Race held here is one of Kerala's most prestigious cultural events. The region's coir industry is world-renowned, with traditional coir products being exported globally. Alappuzha's cuisine includes delicious seafood specialties and traditional Kerala dishes. October to February is the ideal time to visit when the weather is pleasant and perfect for backwater exploration. The ancient Krishnapuram Palace showcases traditional Kerala architecture and historical artifacts. Visitors can enjoy bird watching at Kumarakom Bird Sanctuary, home to migratory birds. Alappuzha offers an unforgettable experience combining natural beauty, cultural richness, and traditional Kerala lifestyle.",
    
    "kottayam": "Kottayam, known as the 'Land of Letters, Lakes, and Latex,' is a vibrant district celebrated for its educational excellence. The district is home to the beautiful Kumarakom backwaters, offering serene houseboat experiences and bird watching opportunities. The Vembanad Lake, the longest lake in Kerala, provides breathtaking sunset views and water activities. The region's rubber plantations stretch across the landscape, making it a major rubber production center. Kottayam's cultural heritage is reflected in its ancient churches and traditional Kerala architecture. The local cuisine features authentic Kerala Sadya and traditional Syrian Christian delicacies. September to March is the best time to visit when the weather is pleasant and perfect for exploration. The district hosts the famous Ettumanoor Festival, showcasing Kerala's rich cultural traditions. Visitors can explore the ancient St. Mary's Church, one of the oldest churches in Kerala. Kottayam offers a perfect blend of educational excellence, natural beauty, and cultural richness.",
    
    "idukki": "Idukki, a picturesque hill district, is renowned for its stunning landscapes and diverse wildlife sanctuaries. The district is home to the magnificent Idukki Arch Dam, one of the world's highest arch dams. The Periyar Tiger Reserve offers thrilling wildlife safaris and boat rides on Periyar Lake. Munnar, a popular hill station, features sprawling tea gardens and misty mountain peaks. The region's spice plantations produce world-famous cardamom, pepper, and other aromatic spices. Idukki's tribal communities preserve ancient traditions and unique cultural practices. The local cuisine includes traditional Kerala dishes with distinctive hill station flavors. September to March is the ideal time to visit when the weather is pleasant and perfect for sightseeing. The district hosts the famous Idukki Summer Festival, showcasing local culture and traditions. Visitors can explore the ancient Thekkady Church and traditional tribal settlements. Idukki offers an unforgettable experience combining natural beauty, wildlife adventures, and cultural richness.",
    
    "ernakulam": "Ernakulam, the commercial capital of Kerala, is a dynamic city blending modern urban life with rich cultural heritage. The district is home to Fort Kochi, a historic area featuring ancient Portuguese architecture and Chinese fishing nets. The Marine Drive walkway offers stunning sunset views and is a popular evening destination. The Jewish Synagogue in Mattancherry is one of the oldest active synagogues in the Commonwealth. The region's spice trade history is reflected in its bustling markets and traditional warehouses. Ernakulam's cuisine includes delicious seafood specialties and traditional Kerala dishes. October to March is the best time to visit when the weather is pleasant and perfect for exploration. The district hosts the famous Kochi-Muziris Biennale, showcasing contemporary art and culture. Visitors can explore the ancient Dutch Palace and traditional Kerala art forms. Ernakulam offers a perfect blend of historical significance, modern amenities, and cultural richness.",
    
    "thrissur": "Thrissur, the cultural capital of Kerala, is renowned for its vibrant festivals and rich artistic heritage. The district is famous for the Thrissur Pooram, one of Kerala's most spectacular temple festivals. The Vadakkunnathan Temple, an ancient Shiva temple, showcases exquisite Kerala architecture and mural paintings. The Kerala Kalamandalam, a world-renowned institution, preserves traditional Kerala performing arts. The region's cultural landscape is enriched by numerous classical art schools and traditional music academies. Thrissur's cuisine includes traditional Kerala Sadya and distinctive local delicacies. October to March is the ideal time to visit when the weather is pleasant and festival season is active. The district hosts the famous Onam celebrations, showcasing Kerala's cultural richness. Visitors can explore the ancient Guruvayur Temple, one of India's most important pilgrimage centers. Thrissur offers an immersive experience of Kerala's cultural heritage, artistic traditions, and spiritual significance.",
    
    "palakkad": "Palakkad, known as the 'Gateway of Kerala,' is a scenic district blessed with abundant natural beauty and historical significance. The district is home to the majestic Palakkad Fort, an ancient monument showcasing Kerala's rich history. The Silent Valley National Park preserves pristine tropical forests and diverse wildlife species. The Malampuzha Dam and Gardens offer beautiful recreational spaces and stunning water views. The region's agricultural landscape features lush paddy fields and traditional farming practices. Palakkad's cultural heritage is reflected in its ancient temples and traditional Kerala architecture. The local cuisine includes authentic Kerala dishes and distinctive regional specialties. September to March is the best time to visit when the weather is pleasant and perfect for exploration. The district hosts the famous Kalpathy Car Festival, showcasing traditional Kerala cultural traditions. Visitors can explore the ancient Jain Temple and traditional Kerala art forms. Palakkad offers a perfect blend of historical significance, natural beauty, and cultural richness.",
    
    "malappuram": "Malappuram, a district of hills and rivers, is renowned for its rich cultural heritage and natural beauty. The district is home to the ancient Kadalundi Bird Sanctuary, a paradise for bird watchers and nature enthusiasts. The Nilambur Teak Plantations feature some of the oldest teak trees in the world. The region's historical significance is reflected in its numerous ancient mosques and traditional Kerala architecture. Malappuram's cultural landscape is enriched by its vibrant folk arts and traditional music forms. The local cuisine includes authentic Malabar dishes and distinctive regional specialties. October to March is the ideal time to visit when the weather is pleasant and perfect for exploration. The district hosts the famous Malappuram Pooram, showcasing traditional Kerala cultural traditions. Visitors can explore the ancient Thirunavaya Temple and traditional Kerala art forms. Malappuram offers a perfect blend of historical significance, natural beauty, and cultural richness.",
    
    "kozhikode": "Kozhikode, historically known as Calicut, is a vibrant coastal city celebrated for its rich cultural heritage and culinary excellence. The city is famous for its pristine beaches, including Kozhikode Beach and Beypore Beach, perfect for sunset viewing. The historic Mananchira Square and surrounding water bodies showcase traditional Kerala architecture. The region's spice trade history is reflected in its bustling markets and ancient trading connections. Kozhikode's cuisine is renowned worldwide, especially its distinctive Malabar Biryani and seafood delicacies. October to March is the ideal time to visit when the weather is pleasant and perfect for exploration. The district hosts the famous Malabar Mahotsavam, showcasing Kerala's cultural traditions. Visitors can explore the ancient Tali Shiva Temple and traditional Kerala art forms. Kozhikode offers a perfect blend of historical significance, culinary excellence, and coastal beauty.",
    
    "wayanad": "Wayanad, a picturesque hill district, is renowned for its stunning landscapes, ancient caves, and diverse wildlife. The district is home to the Edakkal Caves, featuring prehistoric petroglyphs and ancient rock carvings. The Chembra Peak offers breathtaking views and is a popular trekking destination. The region's spice plantations produce world-famous pepper, cardamom, and coffee. Wayanad's wildlife sanctuaries, including Wayanad Wildlife Sanctuary, protect diverse flora and fauna. The local cuisine includes traditional Kerala dishes with distinctive tribal influences. October to March is the ideal time to visit when the weather is pleasant and perfect for exploration. The district hosts the famous Wayanad Tourism Festival, showcasing local culture and traditions. Visitors can explore the ancient Jain temples and traditional tribal settlements. Wayanad offers an unforgettable experience combining natural beauty, archaeological significance, and cultural richness.",
    
    "kannur": "Kannur, a historic coastal district, is renowned for its pristine beaches, ancient forts, and vibrant cultural traditions. The district is home to the majestic St. Angelo's Fort, a 16th-century Portuguese fort offering stunning sea views. The famous Theyyam performances showcase Kerala's rich cultural heritage and ancient ritual traditions. The region's beautiful beaches, including Payyambalam Beach, are perfect for relaxation and sunset viewing. Kannur's handloom industry produces world-famous traditional textiles and handicrafts. The local cuisine includes delicious seafood specialties and traditional Kerala dishes. October to March is the ideal time to visit when the weather is pleasant and perfect for exploration. The district hosts the famous Kannur Tourism Festival, showcasing Kerala's cultural traditions. Visitors can explore the ancient Arakkal Museum and traditional Kerala art forms. Kannur offers a perfect blend of historical significance, cultural richness, and coastal beauty.",
    
    "kasaragod": "Kasaragod, the northernmost district of Kerala, is renowned for its ancient forts, pristine beaches, and rich cultural heritage. The district is home to the magnificent Bekal Fort, one of the largest and best-preserved forts in Kerala. The beautiful beaches, including Bekal Beach and Chandragiri Beach, offer stunning sunset views and relaxation spots. The region's cultural landscape is enriched by traditional Theyyam performances and ancient ritual art forms. Kasaragod's cuisine includes delicious Malabar dishes and distinctive regional specialties. October to March is the ideal time to visit when the weather is pleasant and perfect for exploration. The district hosts the famous Kasaragod Tourism Festival, showcasing Kerala's cultural traditions. Visitors can explore the ancient Madhur Temple and traditional Kerala art forms. The Chandragiri Fort offers breathtaking views of the confluence of rivers and the Arabian Sea. Kasaragod offers a perfect blend of historical significance, cultural richness, and natural beauty."
}

# Non-activity focused 10-sentence descriptions
non_activity_descriptions = {
    "thiruvananthapuram": "Thiruvananthapuram, the capital city of Kerala, is a magnificent blend of tradition and modernity with deep cultural roots. The city is renowned for the Padmanabhaswamy Temple, one of the wealthiest religious institutions globally, showcasing Dravidian architectural brilliance. Kovalam Beach represents the city's natural beauty with its crescent-shaped coastline and golden sands that attract visitors worldwide. The city's cultural heritage is preserved in institutions like the Napier Museum, which houses rare archaeological artifacts and historical treasures. Traditional Kerala architecture is evident in the numerous palaces and heritage buildings that dot the cityscape. The local cuisine reflects a perfect harmony of traditional Kerala flavors with modern culinary innovations. October to March offers ideal weather conditions, making it perfect for experiencing the city's cultural richness. The markets are filled with traditional handicrafts, textiles, and spices that represent Kerala's commercial heritage. The city serves as a center for classical arts, music, and traditional performing arts. Thiruvananthapuram stands as a testament to Kerala's ability to preserve its cultural heritage while embracing modern development.",
    
    "kollam": "Kollam, historically known as Quilon, is a coastal city steeped in maritime history and cultural significance. The city has been a major trading center since ancient times, connecting Kerala with international trade routes across the Arabian Sea. Ashtamudi Lake, the second largest lake in Kerala, creates a unique ecosystem that supports diverse aquatic life and traditional fishing communities. The cashew industry has made Kollam famous worldwide, earning it the title of 'Cashew Capital of Kerala.' Portuguese and Dutch colonial influences are visible in the architecture of Thangassery Fort and the historic lighthouse. The local cuisine features fresh seafood delicacies and traditional Kerala dishes with distinctive coastal flavors. The coir industry represents Kollam's traditional craftsmanship, producing world-renowned coir products exported globally. The city's cultural landscape is enriched by ancient temples that showcase exquisite Kerala architectural styles. September to March provides pleasant weather for exploring the city's historical and cultural attractions. Kollam perfectly embodies Kerala's rich maritime heritage and traditional craftsmanship.",
    
    "pathanamthitta": "Pathanamthitta, known as the 'Pilgrim Capital of Kerala,' is a district deeply rooted in spiritual traditions and natural beauty. The sacred Pamba River flows through the district, providing spiritual purification for pilgrims visiting the renowned Sabarimala Temple. The district is blessed with lush green forests that form part of the Western Ghats, creating a biodiversity hotspot. Traditional Kerala architecture is beautifully preserved in ancient temples like the Aranmula Parthasarathy Temple, known for its intricate murals. The region's cultural heritage is reflected in the famous Aranmula Boat Race, a traditional event showcasing Kerala's maritime culture. The local cuisine emphasizes traditional vegetarian dishes, particularly the authentic Kerala Sadya served on banana leaves. The district is home to numerous ancient temples that represent the pinnacle of Kerala's temple architecture. The natural landscape includes pristine waterfalls and scenic hills that enhance the spiritual atmosphere. November to February offers ideal weather for pilgrimage and cultural exploration. Pathanamthitta serves as a perfect destination for those seeking spiritual tranquility and natural serenity.",
    
    "alappuzha": "Alappuzha, famously known as the 'Venice of the East,' is a district celebrated for its intricate backwater network and cultural heritage. The interconnected waterways create a unique ecosystem that supports traditional fishing communities and diverse aquatic life. The coir industry has been the backbone of Alappuzha's economy for centuries, producing world-famous coir products. The district's cultural significance is highlighted by the Nehru Trophy Boat Race, one of Kerala's most prestigious cultural events. Traditional Kerala architecture is beautifully preserved in the ancient Krishnapuram Palace, showcasing royal heritage. The local cuisine features fresh seafood delicacies and traditional dishes influenced by the coastal environment. The agricultural landscape includes vast paddy fields that create a picturesque rural setting. The district's maritime history is reflected in its ancient trading connections with global markets. October to February provides ideal weather for experiencing the backwater culture. Alappuzha represents the perfect harmony between traditional lifestyle and natural beauty.",
    
    "kottayam": "Kottayam, known as the 'Land of Letters, Lakes, and Latex,' is a district celebrated for its educational excellence and natural beauty. The district achieved the remarkable milestone of being the first in India to achieve 100% literacy, setting an educational benchmark. Vembanad Lake, the longest lake in Kerala, creates a stunning aquatic landscape that supports diverse ecosystems. The rubber plantations stretch across the district, making it a major center for natural rubber production. Traditional Syrian Christian heritage is beautifully preserved in ancient churches like St. Mary's Church, one of Kerala's oldest. The local cuisine blends traditional Kerala flavors with distinctive Syrian Christian influences. The cultural landscape is enriched by institutions preserving classical arts and traditional music forms. The agricultural landscape includes vast paddy fields and coconut groves that create a rural paradise. The Ettumanoor Festival showcases the district's rich cultural traditions and artistic heritage. Kottayam stands as a testament to Kerala's commitment to education and cultural preservation.",
    
    "idukki": "Idukki, a picturesque hill district, is renowned for its stunning landscapes and rich biodiversity. The Idukki Arch Dam stands as an engineering marvel, being one of the world's highest arch dams built between granite hills. The district is home to the magnificent Periyar Tiger Reserve, a protected area preserving diverse wildlife species. Munnar's sprawling tea gardens create a mesmerizing green carpet across the rolling hills of the Western Ghats. The spice plantations produce world-famous cardamom, pepper, and cloves, contributing to Kerala's spice trade heritage. Traditional tribal communities preserve ancient cultural practices and unique lifestyles in the forest regions. The local cuisine features traditional Kerala dishes with distinctive hill station flavors and organic ingredients. The natural landscape includes pristine forests, waterfalls, and mountain streams that create a paradise setting. The district's cultural heritage is celebrated during the Idukki Summer Festival, showcasing local traditions. Idukki represents the perfect blend of natural beauty and cultural richness.",
    
    "ernakulam": "Ernakulam, the commercial capital of Kerala, is a dynamic city that masterfully blends historical significance with modern development. The historic Fort Kochi area preserves Portuguese and Dutch colonial architecture, creating a unique European ambiance. The Jewish Synagogue in Mattancherry stands as one of the oldest active synagogues, representing Kerala's multicultural heritage. The spice trade history spans centuries, connecting the city with global commerce routes and cultural exchanges. Traditional Kerala art forms like Kathakali and Kalaripayattu are preserved and performed in cultural centers. The local cuisine is renowned worldwide, especially the distinctive Malabar Biryani and seafood delicacies. The Marine Drive walkway offers stunning sunset views, becoming a popular gathering place for locals and visitors. The city's cultural landscape is enriched by the prestigious Kochi-Muziris Biennale, showcasing contemporary art. The Dutch Palace represents the architectural brilliance of Kerala's royal heritage. Ernakulam stands as a testament to Kerala's successful blend of tradition and modernity.",
    
    "thrissur": "Thrissur, the cultural capital of Kerala, is a city renowned for its rich artistic heritage and spiritual significance. The Vadakkunnathan Temple showcases exquisite Kerala architecture with its magnificent mural paintings and traditional design. The Kerala Kalamandalam institution preserves traditional performing arts like Kathakali and Mohiniyattam for future generations. The famous Thrissur Pooram festival represents the pinnacle of Kerala's temple festival culture, attracting millions of devotees. The Guruvayur Temple serves as one of India's most important pilgrimage centers, dedicated to Lord Krishna. Traditional Kerala cuisine is celebrated in its purest form, with emphasis on authentic Sadya and temple prasadam. The city's cultural landscape is enriched by numerous classical art schools and traditional music academies. The architectural heritage is reflected in ancient palaces and traditional buildings that dot the cityscape. The cultural significance extends to traditional crafts and handicrafts that are preserved by local artisans. Thrissur stands as the beating heart of Kerala's cultural heritage and artistic traditions.",
    
    "palakkad": "Palakkad, known as the 'Gateway of Kerala,' is a district blessed with abundant natural beauty and historical significance. The majestic Palakkad Fort stands as a testament to Kerala's rich history, built by Hyder Ali in the 18th century. The Silent Valley National Park preserves pristine tropical rainforests, creating a biodiversity hotspot of global importance. The agricultural landscape features lush paddy fields, earning the district the title of 'Rice Bowl of Kerala.' Traditional Kerala architecture is beautifully preserved in ancient temples and heritage buildings. The Malampuzha Dam creates a stunning water body that enhances the district's natural beauty. The local cuisine emphasizes authentic Kerala dishes with distinctive regional specialties and organic ingredients. The cultural heritage is celebrated during the famous Kalpathy Car Festival, showcasing traditional traditions. The Nelliyampathy hills create a picturesque backdrop with tea gardens and orange plantations. The district serves as a perfect blend of historical significance and agricultural prosperity.",
    
    "malappuram": "Malappuram, a district of hills and rivers, is renowned for its rich cultural heritage and natural beauty. The Nilambur Teak Plantations feature some of the oldest teak trees in the world, representing Kerala's forestry heritage. The Kadalundi Bird Sanctuary creates a paradise for migratory birds and nature enthusiasts. The district's historical significance is reflected in ancient mosques that showcase Islamic architectural brilliance. Traditional Kerala folk arts and music forms are preserved and performed by local cultural groups. The local cuisine features authentic Malabar dishes with distinctive regional flavors and spices. The Thirunavaya area holds immense historical importance as a center for Hindu rituals and ceremonies. The cultural landscape is enriched by traditional crafts and handicrafts that are passed down through generations. The natural beauty includes scenic hills, rivers, and backwaters that create a picturesque setting. The district serves as a perfect blend of cultural richness and natural splendor.",
    
    "kozhikode": "Kozhikode, historically known as Calicut, is a coastal city celebrated for its rich maritime heritage and culinary excellence. The city's spice trade history spans centuries, connecting Kerala with international commerce and cultural exchanges. The Mananchira Square represents the city's architectural heritage with traditional Kerala buildings and water bodies. The local cuisine is renowned worldwide, especially the distinctive Malabar Biryani and seafood preparations. The Kappad Beach holds historical significance as the landing site of Vasco da Gama in 1498. Traditional Kerala art forms and cultural performances are preserved in cultural centers across the city. The spice markets create a vibrant atmosphere filled with aromatic spices and traditional trading practices. The cultural heritage is celebrated during the famous Malabar Mahotsavam, showcasing regional traditions. The architectural landscape includes ancient temples and traditional buildings that reflect Kerala's heritage. Kozhikode stands as a testament to Kerala's maritime history and culinary excellence.",
    
    "wayanad": "Wayanad, a picturesque hill district, is renowned for its stunning landscapes and archaeological significance. The Edakkal Caves feature prehistoric petroglyphs and rock carvings dating back to 6000 BCE, representing ancient human civilization. The Chembra Peak offers breathtaking views and a unique heart-shaped lake at its summit. The Wayanad Wildlife Sanctuary preserves diverse flora and fauna, creating a biodiversity hotspot. Traditional tribal communities preserve ancient cultural practices and unique lifestyles in the forest regions. The spice plantations produce world-famous pepper, cardamom, and coffee, contributing to Kerala's spice heritage. The Banasura Sagar Dam stands as the largest earth dam in India, creating stunning island formations. The local cuisine features traditional Kerala dishes with distinctive tribal influences and organic ingredients. The cultural heritage is celebrated during the Wayanad Tourism Festival, showcasing local traditions. The district serves as a perfect blend of archaeological significance and natural beauty.",
    
    "kannur": "Kannur, a historic coastal district, is renowned for its rich cultural heritage and maritime traditions. The St. Angelo's Fort represents Portuguese colonial architecture and Kerala's defense heritage. The Theyyam performances showcase Kerala's ancient ritual traditions, creating a unique cultural experience. The handloom industry produces world-famous traditional textiles, representing Kerala's craftsmanship heritage. The Arakkal Museum preserves the region's royal heritage and maritime history. The local cuisine features fresh seafood delicacies and traditional Kerala dishes with coastal influences. The cultural landscape is enriched by traditional art forms and folk performances. The Payyambalam Beach creates a perfect setting for experiencing coastal beauty and sunset views. The Muzhappilangad Beach stands as the longest drive-in beach in Asia, offering unique coastal experiences. The district serves as a perfect blend of historical significance and cultural richness.",
    
    "kasaragod": "Kasaragod, the northernmost district of Kerala, is renowned for its ancient forts and cultural heritage. The Bekal Fort stands as one of the largest and best-preserved forts in Kerala, offering stunning sea views. The Chandragiri Fort provides breathtaking views of the confluence of rivers and the Arabian Sea. The traditional Theyyam performances preserve ancient ritual art forms that have been practiced for centuries. The local cuisine features delicious Malabar dishes with distinctive regional specialties. The Madhur Temple represents ancient Kerala architecture and spiritual significance. The cultural landscape is enriched by traditional crafts and folk art forms. The beaches create perfect settings for relaxation and experiencing coastal beauty. The district's strategic location creates a unique cultural fusion of Kerala and Karnataka traditions. Kasaragod serves as a perfect blend of historical significance and cultural richness."
}

# Short 5-6 sentence descriptions for all places
short_descriptions = {
    "thiruvananthapuram": "Thiruvananthapuram, the capital of Kerala, is rich in culture and history. It is famous for the Padmanabhaswamy Temple and scenic beaches like Kovalam and Shanghumugham. The city offers vibrant local markets and delicious Kerala cuisine, including Sadya and seafood dishes. Visitors can explore museums, cultural landmarks, and nearby hill stations. October to March is the best time to visit for pleasant weather and festivals. Thiruvananthapuram beautifully blends spiritual heritage, natural beauty, and modern city life.",
    
    "kollam": "Kollam is a historic coastal city known as the gateway to Kerala's backwaters. It features the beautiful Ashtamudi Lake, perfect for houseboat experiences and scenic views. The city is famous for its cashew industry and traditional coir products. Visitors can explore Thangassery Beach with its historic lighthouse and Portuguese fort ruins. The local cuisine offers delicious seafood and traditional Kerala Sadya. September to March is ideal for pleasant weather and cultural festivals.",
    
    "pathanamthitta": "Pathanamthitta is known as the Pilgrim Capital of Kerala, famous for the sacred Sabarimala Temple. The district features the holy Pamba River and lush green forests of the Western Ghats. Visitors can explore ancient temples like Aranmula Parthasarathy with its beautiful murals. The region offers authentic Kerala cuisine, especially traditional vegetarian Sadya. November to February provides the best weather for pilgrimage and sightseeing. Pathanamthitta combines spiritual tranquility with natural beauty.",
    
    "alappuzha": "Alappuzha, known as the Venice of the East, is famous for its beautiful backwaters and houseboats. The district offers enchanting cruises through serene waters surrounded by lush paddy fields. Visitors can enjoy the famous Nehru Trophy Boat Race and explore historic Krishnapuram Palace. The local cuisine features delicious seafood and traditional Kerala dishes. October to February provides ideal weather for backwater experiences. Alappuzha perfectly combines natural beauty with traditional Kerala lifestyle.",
    
    "kottayam": "Kottayam, known as the Land of Letters, Lakes, and Latex, is celebrated for its educational excellence and natural beauty. The district features the beautiful Kumarakom backwaters and the vast Vembanad Lake. Visitors can explore ancient churches like St. Mary's Church and traditional rubber plantations. The local cuisine blends Kerala flavors with Syrian Christian influences. September to March offers pleasant weather for exploration. Kottayam perfectly combines education, nature, and cultural heritage.",
    
    "idukki": "Idukki is a picturesque hill district renowned for its stunning landscapes and wildlife sanctuaries. The district features the magnificent Idukki Arch Dam and the beautiful Munnar tea gardens. Visitors can explore the Periyar Tiger Reserve and enjoy spice plantation tours. The local cuisine includes traditional Kerala dishes with hill station flavors. September to March provides ideal weather for sightseeing. Idukki offers a perfect blend of natural beauty and cultural richness.",
    
    "ernakulam": "Ernakulam, the commercial capital of Kerala, blends modern urban life with rich cultural heritage. The district features historic Fort Kochi with Portuguese architecture and iconic Chinese fishing nets. Visitors can explore the ancient Jewish Synagogue and enjoy sunset views at Marine Drive. The local cuisine is famous for Malabar Biryani and seafood delicacies. October to March offers ideal weather for exploration. Ernakulam perfectly combines historical significance with modern amenities.",
    
    "thrissur": "Thrissur, the cultural capital of Kerala, is renowned for its vibrant festivals and rich artistic heritage. The district features the famous Vadakkunnathan Temple and the prestigious Kerala Kalamandalam. Visitors can experience the spectacular Thrissur Pooram festival and explore the sacred Guruvayur Temple. The local cuisine offers traditional Kerala Sadya and temple prasadam. October to March provides ideal weather for cultural experiences. Thrissur stands as the beating heart of Kerala's cultural traditions.",
    
    "palakkad": "Palakkad, known as the Gateway of Kerala, is blessed with natural beauty and historical significance. The district features the majestic Palakkad Fort and the pristine Silent Valley National Park. Visitors can explore the beautiful Malampuzha Gardens and scenic Nelliyampathy hills. The local cuisine offers authentic Kerala dishes with regional specialties. September to March provides ideal weather for exploration. Palakkad perfectly blends historical heritage with natural splendor.",
    
    "malappuram": "Malappuram, a district of hills and rivers, is renowned for its rich cultural heritage. The district features the ancient Nilambur Teak Plantations and the beautiful Kadalundi Bird Sanctuary. Visitors can explore historic mosques and enjoy the scenic beauty of rolling hills. The local cuisine offers authentic Malabar dishes with distinctive flavors. October to March provides ideal weather for cultural exploration. Malappuram perfectly blends cultural richness with natural splendor.",
    
    "kozhikode": "Kozhikode, historically known as Calicut, is a vibrant coastal city celebrated for its rich heritage. The city features beautiful beaches like Kozhikode and Beypore, perfect for sunset viewing. Visitors can explore the historic Mananchira Square and the ancient Tali Shiva Temple. The local cuisine is renowned for Malabar Biryani and seafood delicacies. October to March provides ideal weather for exploration. Kozhikode perfectly blends historical significance with culinary excellence.",
    
    "wayanad": "Wayanad is a picturesque hill district renowned for its stunning landscapes and ancient caves. The district features the prehistoric Edakkal Caves and the beautiful Chembra Peak with its heart-shaped lake. Visitors can explore the Wayanad Wildlife Sanctuary and enjoy spice plantation tours. The local cuisine includes traditional Kerala dishes with tribal influences. October to March provides ideal weather for exploration. Wayanad offers a perfect blend of natural beauty and archaeological significance.",
    
    "kannur": "Kannur is a historic coastal district renowned for its pristine beaches and cultural traditions. The district features the majestic St. Angelo's Fort and the beautiful Payyambalam Beach. Visitors can experience traditional Theyyam performances and explore the world-famous handloom industry. The local cuisine offers fresh seafood and traditional Kerala dishes. October to March provides ideal weather for cultural experiences. Kannur perfectly blends historical significance with coastal beauty.",
    
    "kasaragod": "Kasaragod, the northernmost district of Kerala, is renowned for its ancient forts and cultural heritage. The district features the magnificent Bekal Fort and the beautiful Bekal and Chandragiri beaches. Visitors can experience traditional Theyyam performances and explore the ancient Madhur Temple. The local cuisine offers delicious Malabar dishes with distinctive flavors. October to March provides ideal weather for exploration. Kasaragod perfectly blends historical significance with coastal beauty."
}

def update_descriptions_ten_sentence():
    """Update all place descriptions with 10-sentence paragraphs"""
    with app.app_context():
        for place_name, description in ten_sentence_descriptions.items():
            place = Place.query.filter_by(name=place_name).first()
            if place:
                place.description = description
                print(f"Updated 10-sentence description for {place.title}")
            else:
                print(f"Place not found: {place_name}")
        
        db.session.commit()
        print("All 10-sentence descriptions updated successfully!")

def update_descriptions_non_activity():
    """Update all place descriptions with non-activity focused content"""
    with app.app_context():
        for place_name, description in non_activity_descriptions.items():
            place = Place.query.filter_by(name=place_name).first()
            if place:
                place.description = description
                print(f"Updated non-activity description for {place.title}")
            else:
                print(f"Place not found: {place_name}")
        
        db.session.commit()
        print("All non-activity focused descriptions updated successfully!")

def update_descriptions_short():
    """Update all place descriptions with short 5-6 sentence paragraphs"""
    with app.app_context():
        for place_name, description in short_descriptions.items():
            place = Place.query.filter_by(name=place_name).first()
            if place:
                place.description = description
                print(f"Updated short description for {place.title}")
            else:
                print(f"Place not found: {place_name}")
        
        db.session.commit()
        print("All short descriptions updated successfully!")

# ===== ROUTES =====
@app.route('/')
def index():
    print("Home page loaded")
    featured_places = Place.query.limit(3).all()
    validate_place_images(featured_places)
    
    # Add image paths to featured places using new helper function
    for place in featured_places:
        print(f"DEBUG: Index - Getting images for {place.name}")
        place.hero_image = get_hero_image(place.name)
        place.gallery_images = get_place_images(place.name, limit=4)
        print(f"DEBUG: Index - hero_image: {place.hero_image}, gallery_images: {place.gallery_images}")
    
    return render_template('index.html', featured_places=featured_places)

@app.route('/explore')
def explore():
    print("Explore page loaded")
    category_filter = request.args.get('category', '')
    search_query = request.args.get('search', '')
    sort_by = request.args.get('sort', 'name')
    
    # Get all places from database
    places_query = Place.query
    
    # Apply category filter
    if category_filter:
        places_query = places_query.filter(Place.category == category_filter)
    
    # Apply search filter
    if search_query:
        places_query = places_query.filter(
            Place.title.contains(search_query) | 
            Place.description.contains(search_query)
        )
    
    # Sort places
    if sort_by == 'budget':
        places = places_query.order_by(Place.avg_budget).all()
    elif sort_by == 'popularity':
        places = places_query.order_by(Place.title).all()
    else:
        places = places_query.order_by(Place.name).all()
    
    validate_place_images(places)
    
    # Add image paths to places using new helper function
    for place in places:
        print(f"DEBUG: Explore - Getting images for {place.name}")
        place.hero_image = get_hero_image(place.name)
        place.gallery_images = get_place_images(place.name, limit=3)
        print(f"DEBUG: Explore - hero_image: {place.hero_image}, gallery_images: {place.gallery_images}")
    
    # Get categories
    categories = [cat[0] for cat in db.session.query(Place.category).distinct().all()]
    
    return render_template('explore.html', places=places, categories=categories, 
                         category_filter=category_filter, search_query=search_query, sort_by=sort_by)

@app.route('/place/<place_name>')
def place_detail(place_name):
    # Debug print
    print("Clicked:", place_name)
    
    place = Place.query.filter_by(name=place_name).first()
    
    if not place:
        return render_template("404.html"), 404
    
    validate_place_images(place)
    
    # Add image paths to place using new helper function
    print(f"DEBUG: Place Detail - Getting images for {place.name}")
    place.hero_image = get_hero_image(place.name)
    place.gallery_images = get_place_images(place.name, limit=6)
    print(f"DEBUG: Place Detail - hero_image: {place.hero_image}, gallery_images: {place.gallery_images}")
    
    return render_template('place_detail.html', place=place)

@app.route('/plan', methods=['GET', 'POST'])
def plan():
    print("DEBUG: Plan page loaded")
    
    if request.method == 'POST':
        print("DEBUG: POST request received")
        
        # Get form data with validation
        destination = request.form.get('destination', '').strip()
        days_str = request.form.get('days', '3')
        budget = request.form.get('budget', 'medium').strip()
        travelers_str = request.form.get('travelers', '2')
        interests = request.form.get('interests', '').strip()
        
        print(f"DEBUG: Form data - destination: {destination}, days: {days_str}, budget: {budget}, travelers: {travelers_str}, interests: {interests}")
        
        # Validate inputs
        if not destination:
            flash('Please select a destination', 'error')
            return redirect(url_for('plan'))
        
        try:
            days = int(days_str)
            if days < 1 or days > 30:
                flash('Number of days must be between 1 and 30', 'error')
                return redirect(url_for('plan'))
        except ValueError:
            flash('Invalid number of days', 'error')
            return redirect(url_for('plan'))
        
        try:
            travelers = int(travelers_str)
            if travelers < 1 or travelers > 20:
                flash('Number of travelers must be between 1 and 20', 'error')
                return redirect(url_for('plan'))
        except ValueError:
            flash('Invalid number of travelers', 'error')
            return redirect(url_for('plan'))
        
        if budget not in ['low', 'medium', 'high']:
            flash('Invalid budget selection', 'error')
            return redirect(url_for('plan'))
        
        try:
            # Generate trip plan
            print("DEBUG: Calling generate_trip_plan function")
            plan = generate_trip_plan(destination, days, budget, travelers, interests)
            
            if plan:
                print("DEBUG: Trip plan generated successfully")
                # Save trip if user is logged in
                if 'user_id' in session:
                    print("DEBUG: Saving trip to database")
                    trip = Trip(
                        destination=destination,
                        days=days,
                        budget=budget,
                        interests=interests,
                        plan_text=json.dumps(plan),
                        user_id=session['user_id']
                    )
                    db.session.add(trip)
                    db.session.commit()
                    print("DEBUG: Trip saved successfully")
                
                return render_template('plan_result.html', 
                                     destination=destination, 
                                     days=days, 
                                     budget=budget, 
                                     travelers=travelers,
                                     interests=interests,
                                     plan=plan)
            else:
                print("DEBUG: Failed to generate trip plan")
                flash('Unable to generate trip plan. Please try again.', 'error')
                return redirect(url_for('plan'))
        except Exception as e:
            print(f"DEBUG: Error during trip planning: {str(e)}")
            import traceback
            traceback.print_exc()
            flash(f'An error occurred while generating your trip: {str(e)}', 'error')
            return redirect(url_for('plan'))
    
    # GET request - render the planning form
    print("DEBUG: Rendering plan.html form")
    places = Place.query.all()
    validate_place_images(places)
    return render_template('plan.html', places=places)

@app.route('/login', methods=['GET', 'POST'])
def login():
    print("Login page loaded")
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        if password != confirm_password:
            flash('Passwords do not match', 'error')
            return redirect(url_for('signup'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'error')
            return redirect(url_for('signup'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists', 'error')
            return redirect(url_for('signup'))
        
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    trips = Trip.query.filter_by(user_id=session['user_id']).order_by(Trip.created_at.desc()).all()
    wishlist_items = Wishlist.query.filter_by(user_id=session['user_id']).all()
    for item in wishlist_items:
        if item.place:
            validate_place_images(item.place)
    
    return render_template('dashboard.html', user=user, trips=trips, wishlist_items=wishlist_items)

@app.route('/add_to_wishlist/<place_name>')
@login_required
def add_to_wishlist(place_name):
    place = Place.query.filter_by(name=place_name).first()
    if not place:
        flash('Destination not found', 'error')
        return redirect(url_for('explore'))
    
    # Check if already in wishlist
    existing = Wishlist.query.filter_by(user_id=session['user_id'], place_id=place.id).first()
    if existing:
        flash('Already in your wishlist', 'info')
    else:
        wishlist = Wishlist(user_id=session['user_id'], place_id=place.id)
        db.session.add(wishlist)
        db.session.commit()
        flash('Added to wishlist!', 'success')
    
    return redirect(url_for('place_detail', place_name=place_name))

@app.route('/remove_from_wishlist/<place_name>')
@login_required
def remove_from_wishlist(place_name):
    place = Place.query.filter_by(name=place_name).first()
    if not place:
        flash('Destination not found', 'error')
        return redirect(url_for('explore'))
    
    wishlist_item = Wishlist.query.filter_by(user_id=session['user_id'], place_id=place.id).first()
    if wishlist_item:
        db.session.delete(wishlist_item)
        db.session.commit()
        flash('Removed from wishlist', 'info')
    
    return redirect(url_for('dashboard'))

# ===== ERROR HANDLERS =====
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

# ===== MAIN EXECUTION =====
if __name__ == '__main__':
    import sys
    
    # Check command line arguments for utility functions
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == 'update_ten_sentence':
            update_descriptions_ten_sentence()
        elif command == 'update_non_activity':
            update_descriptions_non_activity()
        elif command == 'update_short':
            update_descriptions_short()
        else:
            print("Available commands:")
            print("  update_ten_sentence - Update with 10-sentence descriptions")
            print("  update_non_activity - Update with non-activity focused descriptions")
            print("  update_short - Update with short 5-6 sentence descriptions")
    else:
        # Default: run the web application
        with app.app_context():
            create_tables()
        app.run(debug=True, host='0.0.0.0', port=5000)
