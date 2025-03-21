 .
├──  db.sqlite3                  # SQLite Database (Generated automatically)
├──  manage.py                   # Django Management Script
├──  myapp                        # Django Application Folder
│  ├──  __init__.py               # Marks this directory as a Python package
│  ├──  api                        # API-related files
│  │  ├──  __init__.py             # Package marker
│  │  ├──  serializer.py           # (if using DRF, defines data serializers)
│  │  ├──  urls.py                 # API URL configurations
│  │  └──  views.py                # API views (contains prediction logic)
│  ├──  mapping                    # JSON mapping data
│  │  └──  plants_family_mapping.json  
│  ├──  metadata                   # Metadata files
│  │  ├──  class_idx_to_species_id.json  
│  │  └──  plantnet300K_species_id_2_name.json  
│  ├──  migrations                 # Database migrations
│  │  ├──  __init__.py
│  ├──  model                      # Machine Learning Model Storage
│  │  └──  data.pkl                 # Trained ML Model File
│  ├──  models.py                  # Django ORM Models
│  ├──  tests.py                   # Test Cases
│  └──  views.py                   # App-level views (not API-specific)
├──  myproject                     # Main Django Project Folder
│  ├──  __init__.py                
│  ├──  asgi.py                     # ASGI Configuration
│  ├──  settings.py                 # Django Project Settings
│  ├──  urls.py                     # Root URL Configuration
│  ├──  wsgi.py                     # WSGI Configuration
├──  README.md                     # Project Documentation
└──  requirements.txt               # Required Python Packages
