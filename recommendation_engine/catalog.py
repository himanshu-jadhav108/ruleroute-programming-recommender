"""
Catalog module for RuleRoute Recommendation Engine.
Contains definitions for supported domains, experience levels, difficulty tiers,
the 18 canonical project ideas from the original specification, and demonstration profiles.
"""

from typing import List, Dict, Any

SUPPORTED_DOMAINS: List[str] = [
    'AI/ML',
    'Web Development',
    'App Development',
    'Data Science',
    'Automation',
    'Game Development',
]

SUPPORTED_LEVELS: List[str] = [
    'Beginner',
    'Intermediate',
    'Advanced',
]

SUPPORTED_DIFFICULTIES: List[str] = [
    'Easy',
    'Medium',
    'Hard',
]

# Canonical 18 project ideas from original notebook (Preserved verbatim)
PROJECT_CATALOG: List[Dict[str, str]] = [
    # AI/ML
    {
        'domain': 'AI/ML',
        'difficulty': 'Easy',
        'name': 'Smart Vacuum Cleaner Simulation & Reflex Agent',
        'language': 'Python',
        'description': 'Simulate an autonomous agent cleaning grid rooms with percept-action rules and state tracking.',
        'reason': 'Introduces agent environments, rational decision-making, and state transitions without complex math.',
    },
    {
        'domain': 'AI/ML',
        'difficulty': 'Medium',
        'name': 'Adversarial Game Playing Agent with Alpha-Beta Pruning',
        'language': 'Python',
        'description': 'Develop an intelligent agent playing Connect-4 or Chess endgames with depth-limited heuristic evaluation.',
        'reason': 'Synthesizes state-space search, minimax optimization, and tree pruning techniques.',
    },
    {
        'domain': 'AI/ML',
        'difficulty': 'Hard',
        'name': 'Real-Time Edge Computer Vision Pipeline',
        'language': 'Python / C++',
        'description': 'Construct a live multi-camera object detection and tracking pipeline accelerated with ONNX Runtime.',
        'reason': 'Integrates deep learning model optimization, video frame buffering, and low-latency inference.',
    },
    # Web Development
    {
        'domain': 'Web Development',
        'difficulty': 'Easy',
        'name': 'Interactive Student Task & Milestone Tracker',
        'language': 'JavaScript / HTML / CSS',
        'description': 'Responsive browser application using LocalStorage to track assignments and semester study targets.',
        'reason': 'Reinforces fundamental DOM manipulation, client-side event handling, and clean responsive CSS.',
    },
    {
        'domain': 'Web Development',
        'difficulty': 'Medium',
        'name': 'Collaborative Note-Sharing & Discussion Platform',
        'language': 'TypeScript / Node.js / React',
        'description': 'Full-stack application with JWT authentication, RESTful endpoints, and markdown note formatting.',
        'reason': 'Demonstrates full-stack web architecture, database integration, and secure user session management.',
    },
    {
        'domain': 'Web Development',
        'difficulty': 'Hard',
        'name': 'Real-Time Collaborative Code Editor',
        'language': 'TypeScript / WebSockets / Go',
        'description': 'Multi-user synchronized code editor supporting live cursor tracking and Operational Transformation.',
        'reason': 'Explores concurrent distributed state synchronization, WebSockets, and low-latency client-server messaging.',
    },
    # App Development
    {
        'domain': 'App Development',
        'difficulty': 'Easy',
        'name': 'Campus Notice & Event Broadcasting App',
        'language': 'Dart (Flutter)',
        'description': 'Mobile app presenting categorized departmental notices, search filters, and bookmarking.',
        'reason': 'Excellent project for mastering declarative widget trees and cross-platform compilation.',
    },
    {
        'domain': 'App Development',
        'difficulty': 'Medium',
        'name': 'Personal Expense Tracker & Receipt Scanner',
        'language': 'Kotlin (Android)',
        'description': 'Native Android app utilizing Room DB, Jetpack ViewModels, and on-device ML Kit OCR for receipts.',
        'reason': 'Implements modern Android Architecture Components (MVVM) and persistent local relational storage.',
    },
    {
        'domain': 'App Development',
        'difficulty': 'Hard',
        'name': 'Offline-First Mesh Messenger',
        'language': 'Kotlin / Bluetooth LE',
        'description': 'Peer-to-peer decentralized text messenger functioning over Bluetooth Low Energy mesh connections.',
        'reason': 'Deep dive into mobile hardware protocols, ad-hoc packet routing, and distributed synchronization.',
    },
    # Data Science
    {
        'domain': 'Data Science',
        'difficulty': 'Easy',
        'name': 'Exploratory Analysis of Engineering Placement Trends',
        'language': 'Python (Pandas, Seaborn)',
        'description': 'Statistical analysis and interactive visual dashboard identifying patterns in student placements.',
        'reason': 'Builds core proficiency in data cleaning, exploratory statistics, and insightful visualizations.',
    },
    {
        'domain': 'Data Science',
        'difficulty': 'Medium',
        'name': 'Automated Customer Churn & Segmentation Engine',
        'language': 'Python & SQL',
        'description': 'Pipeline performing RFM feature engineering, clustering, and predictive classification on customer cohorts.',
        'reason': 'Applies statistical modeling and feature engineering to real-world business analytics scenarios.',
    },
    {
        'domain': 'Data Science',
        'difficulty': 'Hard',
        'name': 'Real-Time Financial Sentiment & Time-Series Pipeline',
        'language': 'Python / Apache Kafka',
        'description': 'Streaming ingest pipeline aggregating market news, computing NLP sentiment, and predicting price trends.',
        'reason': 'Connects streaming distributed data architecture with NLP inference and time-series forecasting.',
    },
    # Automation
    {
        'domain': 'Automation',
        'difficulty': 'Easy',
        'name': 'Automated E-Commerce Price Monitor & Notification Bot',
        'language': 'Python (BeautifulSoup, Requests)',
        'description': 'Scheduled script monitoring online prices, recording historical fluctuations, and dispatching alerts.',
        'reason': 'Teaches HTML parsing, session headers, cron scheduling, and automated notification webhooks.',
    },
    {
        'domain': 'Automation',
        'difficulty': 'Medium',
        'name': 'College Submission Format & Plagiarism Validator',
        'language': 'Python',
        'description': 'Batch directory inspector validating student submission formats, archives, and cosine similarity.',
        'reason': 'Exercises local filesystem automation, regular expressions, and automated batch report generation.',
    },
    {
        'domain': 'Automation',
        'difficulty': 'Hard',
        'name': 'Automated Cloud Health & CI/CD Orchestration Bot',
        'language': 'Python & Bash',
        'description': 'Daemon monitoring server metrics, managing container health checks, and generating incident logs.',
        'reason': 'Bridges Python scripting with systems programming, container management, and DevOps tooling.',
    },
    # Game Development
    {
        'domain': 'Game Development',
        'difficulty': 'Easy',
        'name': '2D Tile-Based Dungeon Explorer',
        'language': 'C# (Unity) or Python (Pygame)',
        'description': 'Top-down 2D game with grid movement, enemy pathfinding, item collection, and score tracking.',
        'reason': 'Solid foundation in game loops, sprite animation states, and 2D collision detection.',
    },
    {
        'domain': 'Game Development',
        'difficulty': 'Medium',
        'name': '3D Physics Platformer with Dynamic Obstacles',
        'language': 'C# (Unity)',
        'description': 'Third-person 3D character controller incorporating rigid body physics, raycasting, and puzzle hazards.',
        'reason': 'Teaches 3D vector mathematics, character physics, kinematic triggers, and particle systems.',
    },
    {
        'domain': 'Game Development',
        'difficulty': 'Hard',
        'name': 'Custom OpenGL/Vulkan 3D Rendering Engine',
        'language': 'C++',
        'description': 'Graphics engine featuring programmable shader pipelines, camera matrices, shadow maps, and scene graphs.',
        'reason': 'The definitive systems project for understanding GPU pipelines, shader programming, and memory layout.',
    },
]

# Canonical Demonstration Profiles from original notebook
DEMO_PROFILES: List[Dict[str, Any]] = [
    {
        'id': 'demo_1',
        'title': 'Beginner in AI/ML',
        'subtitle': 'Undergraduate Beginner in AI/ML',
        'profile': {
            'experience_level': 'Beginner',
            'preferred_domain': 'AI/ML',
            'main_interest': 'Reflex Agents & Machine Learning',
            'preferred_difficulty': 'Easy',
        },
        'description': 'Focuses on foundations of AI and agent behaviors without heavy mathematics.',
    },
    {
        'id': 'demo_2',
        'title': 'Intermediate Web Developer',
        'subtitle': 'Intermediate Web Developer',
        'profile': {
            'experience_level': 'Intermediate',
            'preferred_domain': 'Web Development',
            'main_interest': 'Full-Stack APIs & Interfaces',
            'preferred_difficulty': 'Medium',
        },
        'description': 'Explores multi-tier full-stack architecture with REST APIs and frontend clients.',
    },
    {
        'id': 'demo_3',
        'title': 'Advanced Game Developer',
        'subtitle': 'Advanced Engineering Student in Game Systems',
        'profile': {
            'experience_level': 'Advanced',
            'preferred_domain': 'Game Development',
            'main_interest': '3D Game Engines & Systems',
            'preferred_difficulty': 'Hard',
        },
        'description': 'Low-level systems programming, 3D rendering pipelines, and custom engine mechanics.',
    },
    {
        'id': 'demo_4',
        'title': 'Beginner in Automation',
        'subtitle': 'Beginner Exploring Python Task Automation',
        'profile': {
            'experience_level': 'Beginner',
            'preferred_domain': 'Automation',
            'main_interest': 'Web Scraping & Scripting',
            'preferred_difficulty': 'Easy',
        },
        'description': 'Hands-on practical scripting for data extraction, browser interaction, and bot automation.',
    },
    {
        'id': 'demo_invalid',
        'title': 'Edge Case / Unsupported Domain',
        'subtitle': 'Edge Case - Unsupported Domain Input',
        'profile': {
            'experience_level': 'Beginner',
            'preferred_domain': 'Quantum Computing',
            'main_interest': 'Qubits',
            'preferred_difficulty': 'Super-Hard',
        },
        'description': 'Demonstrates defensive system validation, boundary constraints, and error catching.',
    },
]

DOMAIN_KEYWORD_HINTS: Dict[str, Dict[str, Any]] = {
    'AI/ML': {
        'hint': 'Keywords can describe modeling, agents, vision, etc. (e.g. reflex agents, neural networks).',
        'rule_note': 'Python is always recommended. Intermediate & Advanced users additionally unlock C++.',
        'example': 'Reflex Agents & Machine Learning',
    },
    'Web Development': {
        'hint': 'Try mentioning "front", "back", "api", or "full" to trigger specific language tracks.',
        'rule_note': 'Contains keyword branches: "front"/"full" triggers JavaScript/TypeScript; "back"/"api"/"full" triggers Python (and Go for Advanced).',
        'example': 'Full-Stack APIs & Interfaces',
    },
    'App Development': {
        'hint': 'Try mentioning "android" for Kotlin, or "cross" for Dart (Flutter).',
        'rule_note': '"android" triggers Kotlin; "cross" or Beginner level triggers Dart (Flutter); other terms default to Kotlin.',
        'example': 'Cross-platform mobile apps',
    },
    'Data Science': {
        'hint': 'Keywords can include analytics, visualization, or pipelines.',
        'rule_note': 'Python is always recommended. Intermediate & Advanced users additionally unlock SQL.',
        'example': 'Exploratory data analysis & dashboards',
    },
    'Automation': {
        'hint': 'Keywords can include web scraping, scheduled scripts, or bots.',
        'rule_note': 'Python is always recommended. Intermediate & Advanced users additionally unlock Bash / Shell.',
        'example': 'Web Scraping & Scripting',
    },
    'Game Development': {
        'hint': 'Try mentioning "unity" or "engine" to steer recommendations.',
        'rule_note': '"unity" or Beginner/Intermediate triggers C#; "engine" or Advanced triggers C++.',
        'example': '3D Game Engines & Systems',
    },
}

