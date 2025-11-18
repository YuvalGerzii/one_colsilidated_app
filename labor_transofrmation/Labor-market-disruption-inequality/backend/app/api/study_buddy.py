"""
Study Buddy Platform API Endpoints
Social network for mutual learning and knowledge sharing
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from app.db.database import get_db
from app.agents.study_buddy_agent import StudyBuddyAgent
from app.models.study_buddy import (
    Contributor, LearnerProfile, KnowledgeResource, LearningPath,
    LearningCurve, Contribution, CreditTransaction, Post, Comment,
    Question, Answer, StudyGroup, RecommendationContext
)

router = APIRouter()

# Initialize Study Buddy Agent
study_buddy_agent = StudyBuddyAgent()


# ==================== Request/Response Models ====================

class CreateContributorRequest(BaseModel):
    username: str
    display_name: str
    bio: Optional[str] = None
    expertise_areas: List[str] = []

class CreateResourceRequest(BaseModel):
    title: str
    description: str
    resource_type: str
    content_url: Optional[str] = None
    content_text: Optional[str] = None
    tags: List[str] = []
    difficulty_level: str
    estimated_time_hours: float
    prerequisites: List[str] = []
    learning_outcomes: List[str] = []
    is_free: bool = True
    price_credits: Optional[float] = None

class CreateLearningPathRequest(BaseModel):
    title: str
    description: str
    target_skill: str
    target_level: str
    resource_ids: List[int]
    tags: List[str] = []

class LogLearningProgressRequest(BaseModel):
    skill_name: str
    proficiency_score: float
    hours_practiced: float
    assessment_type: Optional[str] = None
    confidence_level: Optional[float] = None

class CreatePostRequest(BaseModel):
    content: str
    post_type: str
    related_resource_id: Optional[int] = None
    tags: List[str] = []
    visibility: str = "public"

class CreateQuestionRequest(BaseModel):
    title: str
    content: str
    tags: List[str] = []
    difficulty_level: Optional[str] = None
    bounty_credits: Optional[float] = None

class CreateAnswerRequest(BaseModel):
    question_id: int
    content: str

class CreateStudyGroupRequest(BaseModel):
    name: str
    description: str
    focus_skill: str
    target_level: str
    max_members: int = 10
    is_private: bool = False

class RateResourceRequest(BaseModel):
    rating: float = Field(..., ge=0, le=5)
    review_text: Optional[str] = None


# ==================== Contributor Endpoints ====================

@router.post("/contributors/create")
def create_contributor(
    request: CreateContributorRequest,
    user_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Create a new contributor profile"""
    contributor = Contributor(
        user_id=user_id,
        username=request.username,
        display_name=request.display_name,
        bio=request.bio,
        expertise_areas=request.expertise_areas,
        reputation_score=0.0,
        total_contributions=0,
        total_credits_earned=0.0
    )

    return {
        'status': 'success',
        'message': f'Contributor profile created for {request.username}',
        'contributor': contributor.dict()
    }


@router.get("/contributors/{contributor_id}")
def get_contributor_profile(contributor_id: int, db: Session = Depends(get_db)):
    """Get contributor profile and statistics"""
    # In production, fetch from database
    # For now, return mock data
    return {
        'contributor_id': contributor_id,
        'username': f'contributor_{contributor_id}',
        'display_name': 'Expert Educator',
        'bio': 'Passionate about sharing knowledge and helping others learn',
        'expertise_areas': ['Python', 'Machine Learning', 'Web Development'],
        'reputation_score': 87.5,
        'total_contributions': 45,
        'total_credits_earned': 3250.00,
        'total_learners_helped': 1250,
        'verified_expert': True,
        'followers_count': 523,
        'following_count': 178,
        'recent_activity': [
            {'type': 'resource_created', 'title': 'Advanced Python Patterns', 'date': '2025-11-14'},
            {'type': 'path_published', 'title': 'ML Engineer Roadmap', 'date': '2025-11-12'},
            {'type': 'question_answered', 'title': 'How to optimize neural networks?', 'date': '2025-11-10'}
        ]
    }


@router.get("/contributors/{contributor_id}/analytics")
def get_contributor_analytics(
    contributor_id: int,
    period: str = Query("last_30_days", regex="^(daily|weekly|monthly|all_time)$"),
    db: Session = Depends(get_db)
):
    """Get detailed analytics for a contributor"""
    task = {
        'type': 'contributor_analytics',
        'contributor_id': contributor_id
    }

    response = study_buddy_agent.process_task(task)

    return {
        'status': 'success',
        'contributor_id': contributor_id,
        'analytics': response.data,
        'recommendations': response.recommendations
    }


@router.get("/contributors/{contributor_id}/monetization-strategy")
def get_monetization_strategy(contributor_id: int, db: Session = Depends(get_db)):
    """Get personalized monetization strategy"""
    task = {
        'type': 'monetization_strategy',
        'contributor_id': contributor_id
    }

    response = study_buddy_agent.process_task(task)

    return {
        'status': 'success',
        'contributor_id': contributor_id,
        'strategy': response.data,
        'next_steps': response.next_steps
    }


# ==================== Knowledge Library Endpoints ====================

@router.post("/resources/create")
def create_resource(
    request: CreateResourceRequest,
    creator_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Create a new knowledge resource"""
    resource = KnowledgeResource(
        resource_id=hash(request.title) % 10000,  # Mock ID
        title=request.title,
        description=request.description,
        resource_type=request.resource_type,
        content_url=request.content_url,
        content_text=request.content_text,
        creator_id=creator_id,
        tags=request.tags,
        difficulty_level=request.difficulty_level,
        estimated_time_hours=request.estimated_time_hours,
        prerequisites=request.prerequisites,
        learning_outcomes=request.learning_outcomes,
        is_free=request.is_free,
        price_credits=request.price_credits
    )

    # Assess quality
    quality_task = {
        'type': 'quality_assessment',
        'resource_id': resource.resource_id
    }
    quality_response = study_buddy_agent.process_task(quality_task)

    return {
        'status': 'success',
        'message': 'Resource created successfully',
        'resource': resource.dict(),
        'quality_assessment': quality_response.data
    }


@router.get("/resources/{resource_id}")
def get_resource(resource_id: int, db: Session = Depends(get_db)):
    """Get resource details"""
    return {
        'resource_id': resource_id,
        'title': 'Mastering Python Design Patterns',
        'description': 'Comprehensive guide to advanced Python design patterns',
        'resource_type': 'course',
        'creator_id': 101,
        'creator_name': 'PythonGuru',
        'tags': ['python', 'design-patterns', 'advanced', 'software-engineering'],
        'difficulty_level': 'advanced',
        'estimated_time_hours': 24.0,
        'quality_score': 92.5,
        'views_count': 5423,
        'likes_count': 487,
        'bookmarks_count': 234,
        'average_rating': 4.7,
        'total_reviews': 156,
        'is_free': False,
        'price_credits': 150.0,
        'prerequisites': ['Intermediate Python', 'OOP Basics'],
        'learning_outcomes': [
            'Implement 15+ design patterns',
            'Write maintainable code',
            'Understand SOLID principles',
            'Build scalable applications'
        ]
    }


@router.post("/resources/{resource_id}/rate")
def rate_resource(
    resource_id: int,
    request: RateResourceRequest,
    user_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Rate and review a resource"""
    return {
        'status': 'success',
        'message': 'Rating submitted successfully',
        'resource_id': resource_id,
        'user_rating': request.rating,
        'new_average_rating': 4.7,
        'total_ratings': 157
    }


@router.get("/resources/search")
def search_resources(
    query: Optional[str] = Query(None),
    tags: Optional[List[str]] = Query(None),
    difficulty: Optional[str] = Query(None),
    resource_type: Optional[str] = Query(None),
    min_quality: float = Query(0.0),
    max_quality: float = Query(100.0),
    min_duration: Optional[float] = Query(None),
    max_duration: Optional[float] = Query(None),
    is_free: Optional[bool] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    verified_only: bool = Query(False),
    creator_id: Optional[int] = Query(None),
    min_rating: float = Query(0.0),
    sort_by: str = Query("relevance", regex="^(relevance|popularity|newest|rating|duration|quality)$"),
    order: str = Query("desc", regex="^(asc|desc)$"),
    limit: int = Query(20),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    """Advanced search for resources with comprehensive filters and sorting"""

    # Enhanced mock search results with diverse content
    all_resources = [
        {
            'resource_id': 1,
            'title': 'Advanced Python Design Patterns for Enterprise Applications',
            'description': 'Master 15+ design patterns including Singleton, Factory, Observer, and more with real-world examples',
            'resource_type': 'course',
            'difficulty_level': 'advanced',
            'quality_score': 92.5,
            'creator_id': 101,
            'creator_name': 'PythonGuru',
            'creator_reputation': 94.0,
            'estimated_time_hours': 24.0,
            'tags': ['python', 'design-patterns', 'software-engineering', 'advanced'],
            'views_count': 5423,
            'likes_count': 487,
            'average_rating': 4.7,
            'total_reviews': 156,
            'is_free': False,
            'price_credits': 150.0,
            'verified': True,
            'created_at': '2025-10-15T10:00:00',
            'match_score': 95.0
        },
        {
            'resource_id': 2,
            'title': 'Machine Learning Fundamentals: A Complete Introduction',
            'description': 'Learn ML from scratch with hands-on projects in Python using scikit-learn and TensorFlow',
            'resource_type': 'video',
            'difficulty_level': 'beginner',
            'quality_score': 88.3,
            'creator_id': 102,
            'creator_name': 'MLExpert',
            'creator_reputation': 89.0,
            'estimated_time_hours': 12.0,
            'tags': ['machine-learning', 'ai', 'data-science', 'python'],
            'views_count': 12340,
            'likes_count': 892,
            'average_rating': 4.8,
            'total_reviews': 234,
            'is_free': True,
            'price_credits': 0.0,
            'verified': True,
            'created_at': '2025-11-01T14:30:00',
            'match_score': 92.0
        },
        {
            'resource_id': 3,
            'title': 'SQL Performance Optimization Techniques',
            'description': 'Advanced database query optimization, indexing strategies, and performance tuning',
            'resource_type': 'tutorial',
            'difficulty_level': 'intermediate',
            'quality_score': 85.7,
            'creator_id': 103,
            'creator_name': 'DBMaster',
            'creator_reputation': 87.0,
            'estimated_time_hours': 8.0,
            'tags': ['sql', 'database', 'optimization', 'performance'],
            'views_count': 3210,
            'likes_count': 245,
            'average_rating': 4.5,
            'total_reviews': 89,
            'is_free': True,
            'price_credits': 0.0,
            'verified': False,
            'created_at': '2025-10-20T09:15:00',
            'match_score': 88.0
        },
        {
            'resource_id': 4,
            'title': 'React Hooks Deep Dive: Building Modern Web Apps',
            'description': 'Master React Hooks including useState, useEffect, useContext, and custom hooks',
            'resource_type': 'course',
            'difficulty_level': 'intermediate',
            'quality_score': 90.2,
            'creator_id': 104,
            'creator_name': 'ReactPro',
            'creator_reputation': 91.0,
            'estimated_time_hours': 16.0,
            'tags': ['react', 'javascript', 'web-development', 'frontend'],
            'views_count': 8456,
            'likes_count': 623,
            'average_rating': 4.6,
            'total_reviews': 178,
            'is_free': False,
            'price_credits': 120.0,
            'verified': True,
            'created_at': '2025-10-28T11:45:00',
            'match_score': 90.0
        },
        {
            'resource_id': 5,
            'title': 'Data Structures and Algorithms Masterclass',
            'description': 'Complete guide to DSA with 200+ coding problems and solutions in Python and Java',
            'resource_type': 'course',
            'difficulty_level': 'intermediate',
            'quality_score': 94.8,
            'creator_id': 105,
            'creator_name': 'AlgoExpert',
            'creator_reputation': 96.0,
            'estimated_time_hours': 40.0,
            'tags': ['algorithms', 'data-structures', 'coding-interview', 'python', 'java'],
            'views_count': 15678,
            'likes_count': 1234,
            'average_rating': 4.9,
            'total_reviews': 456,
            'is_free': False,
            'price_credits': 200.0,
            'verified': True,
            'created_at': '2025-09-10T08:00:00',
            'match_score': 93.0
        },
        {
            'resource_id': 6,
            'title': 'Introduction to Cloud Computing with AWS',
            'description': 'Learn AWS basics including EC2, S3, Lambda, and cloud architecture fundamentals',
            'resource_type': 'video',
            'difficulty_level': 'beginner',
            'quality_score': 86.5,
            'creator_id': 106,
            'creator_name': 'CloudGuru',
            'creator_reputation': 88.0,
            'estimated_time_hours': 10.0,
            'tags': ['aws', 'cloud-computing', 'devops', 'infrastructure'],
            'views_count': 6789,
            'likes_count': 456,
            'average_rating': 4.4,
            'total_reviews': 134,
            'is_free': True,
            'price_credits': 0.0,
            'verified': True,
            'created_at': '2025-10-05T16:20:00',
            'match_score': 87.0
        },
        {
            'resource_id': 7,
            'title': 'System Design Interview Preparation',
            'description': 'Comprehensive guide to system design concepts with real company interview questions',
            'resource_type': 'article',
            'difficulty_level': 'advanced',
            'quality_score': 91.3,
            'creator_id': 107,
            'creator_name': 'TechInterviewer',
            'creator_reputation': 92.0,
            'estimated_time_hours': 6.0,
            'tags': ['system-design', 'interview', 'architecture', 'scalability'],
            'views_count': 9876,
            'likes_count': 789,
            'average_rating': 4.7,
            'total_reviews': 223,
            'is_free': False,
            'price_credits': 80.0,
            'verified': True,
            'created_at': '2025-10-18T13:30:00',
            'match_score': 89.0
        },
        {
            'resource_id': 8,
            'title': 'Docker and Kubernetes for Beginners',
            'description': 'Complete introduction to containerization with Docker and orchestration with Kubernetes',
            'resource_type': 'tutorial',
            'difficulty_level': 'beginner',
            'quality_score': 83.7,
            'creator_id': 108,
            'creator_name': 'DevOpsNinja',
            'creator_reputation': 85.0,
            'estimated_time_hours': 14.0,
            'tags': ['docker', 'kubernetes', 'devops', 'containers'],
            'views_count': 7234,
            'likes_count': 534,
            'average_rating': 4.3,
            'total_reviews': 167,
            'is_free': True,
            'price_credits': 0.0,
            'verified': False,
            'created_at': '2025-11-05T10:00:00',
            'match_score': 85.0
        },
        {
            'resource_id': 9,
            'title': 'Advanced JavaScript ES6+ Features',
            'description': 'Deep dive into modern JavaScript including async/await, promises, modules, and more',
            'resource_type': 'interactive',
            'difficulty_level': 'intermediate',
            'quality_score': 89.4,
            'creator_id': 109,
            'creator_name': 'JSNinja',
            'creator_reputation': 90.0,
            'estimated_time_hours': 12.0,
            'tags': ['javascript', 'es6', 'web-development', 'programming'],
            'views_count': 5432,
            'likes_count': 421,
            'average_rating': 4.6,
            'total_reviews': 145,
            'is_free': False,
            'price_credits': 100.0,
            'verified': True,
            'created_at': '2025-10-25T15:45:00',
            'match_score': 88.0
        },
        {
            'resource_id': 10,
            'title': 'The Art of Technical Writing',
            'description': 'Learn how to write clear, effective technical documentation and tutorials',
            'resource_type': 'course',
            'difficulty_level': 'beginner',
            'quality_score': 87.9,
            'creator_id': 110,
            'creator_name': 'DocWriter',
            'creator_reputation': 86.0,
            'estimated_time_hours': 8.0,
            'tags': ['writing', 'documentation', 'communication', 'technical-writing'],
            'views_count': 4123,
            'likes_count': 312,
            'average_rating': 4.5,
            'total_reviews': 98,
            'is_free': True,
            'price_credits': 0.0,
            'verified': False,
            'created_at': '2025-11-08T12:00:00',
            'match_score': 84.0
        },
        {
            'resource_id': 11,
            'title': 'Deep Learning with PyTorch',
            'description': 'Build neural networks from scratch and implement CNNs, RNNs, and transformers',
            'resource_type': 'course',
            'difficulty_level': 'advanced',
            'quality_score': 93.6,
            'creator_id': 111,
            'creator_name': 'AIResearcher',
            'creator_reputation': 95.0,
            'estimated_time_hours': 35.0,
            'tags': ['pytorch', 'deep-learning', 'neural-networks', 'ai'],
            'views_count': 11234,
            'likes_count': 923,
            'average_rating': 4.8,
            'total_reviews': 287,
            'is_free': False,
            'price_credits': 250.0,
            'verified': True,
            'created_at': '2025-09-20T09:30:00',
            'match_score': 91.0
        },
        {
            'resource_id': 12,
            'title': 'Git and GitHub Workflow Essentials',
            'description': 'Master version control with Git, branching strategies, and collaborative workflows',
            'resource_type': 'video',
            'difficulty_level': 'beginner',
            'quality_score': 82.3,
            'creator_id': 112,
            'creator_name': 'GitMaster',
            'creator_reputation': 84.0,
            'estimated_time_hours': 5.0,
            'tags': ['git', 'github', 'version-control', 'collaboration'],
            'views_count': 8901,
            'likes_count': 678,
            'average_rating': 4.2,
            'total_reviews': 201,
            'is_free': True,
            'price_credits': 0.0,
            'verified': False,
            'created_at': '2025-11-10T14:15:00',
            'match_score': 82.0
        },
    ]

    # Apply filters
    filtered_resources = all_resources.copy()

    # Text search filter (search in title, description, tags)
    if query:
        query_lower = query.lower()
        filtered_resources = [
            r for r in filtered_resources
            if query_lower in r['title'].lower()
            or query_lower in r['description'].lower()
            or any(query_lower in tag.lower() for tag in r['tags'])
        ]

    # Tags filter
    if tags:
        filtered_resources = [
            r for r in filtered_resources
            if any(tag in r['tags'] for tag in tags)
        ]

    # Difficulty filter
    if difficulty:
        filtered_resources = [r for r in filtered_resources if r['difficulty_level'] == difficulty]

    # Resource type filter
    if resource_type:
        filtered_resources = [r for r in filtered_resources if r['resource_type'] == resource_type]

    # Quality score filter
    filtered_resources = [
        r for r in filtered_resources
        if min_quality <= r['quality_score'] <= max_quality
    ]

    # Duration filter
    if min_duration is not None:
        filtered_resources = [r for r in filtered_resources if r['estimated_time_hours'] >= min_duration]
    if max_duration is not None:
        filtered_resources = [r for r in filtered_resources if r['estimated_time_hours'] <= max_duration]

    # Price filters
    if is_free is not None:
        filtered_resources = [r for r in filtered_resources if r['is_free'] == is_free]
    if min_price is not None:
        filtered_resources = [r for r in filtered_resources if r['price_credits'] >= min_price]
    if max_price is not None:
        filtered_resources = [r for r in filtered_resources if r['price_credits'] <= max_price]

    # Verified filter
    if verified_only:
        filtered_resources = [r for r in filtered_resources if r['verified']]

    # Creator filter
    if creator_id:
        filtered_resources = [r for r in filtered_resources if r['creator_id'] == creator_id]

    # Rating filter
    filtered_resources = [r for r in filtered_resources if r['average_rating'] >= min_rating]

    # Sorting
    sort_keys = {
        'relevance': lambda r: r['match_score'],
        'popularity': lambda r: r['views_count'],
        'newest': lambda r: r['created_at'],
        'rating': lambda r: r['average_rating'],
        'duration': lambda r: r['estimated_time_hours'],
        'quality': lambda r: r['quality_score']
    }

    if sort_by in sort_keys:
        filtered_resources.sort(key=sort_keys[sort_by], reverse=(order == 'desc'))

    # Pagination
    total_results = len(filtered_resources)
    paginated_resources = filtered_resources[offset:offset + limit]

    return {
        'status': 'success',
        'query': query,
        'total_results': total_results,
        'filters_applied': {
            'query': query,
            'tags': tags,
            'difficulty': difficulty,
            'resource_type': resource_type,
            'quality_range': [min_quality, max_quality],
            'duration_range': [min_duration, max_duration],
            'is_free': is_free,
            'price_range': [min_price, max_price],
            'verified_only': verified_only,
            'creator_id': creator_id,
            'min_rating': min_rating,
        },
        'sort_by': sort_by,
        'order': order,
        'offset': offset,
        'limit': limit,
        'results': paginated_resources,
        'facets': {
            'resource_types': _get_facet_counts(filtered_resources, 'resource_type'),
            'difficulty_levels': _get_facet_counts(filtered_resources, 'difficulty_level'),
            'price_distribution': {
                'free': len([r for r in filtered_resources if r['is_free']]),
                'paid': len([r for r in filtered_resources if not r['is_free']])
            }
        }
    }


def _get_facet_counts(resources: List[Dict], field: str) -> Dict[str, int]:
    """Helper function to get facet counts for a field"""
    counts = {}
    for resource in resources:
        value = resource.get(field)
        if value:
            counts[value] = counts.get(value, 0) + 1
    return counts


# ==================== Learning Path Endpoints ====================

@router.post("/paths/create")
def create_learning_path(
    request: CreateLearningPathRequest,
    creator_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Create a new learning path"""
    path_id = hash(request.title) % 10000

    return {
        'status': 'success',
        'message': 'Learning path created successfully',
        'path_id': path_id,
        'title': request.title,
        'creator_id': creator_id,
        'target_skill': request.target_skill,
        'total_resources': len(request.resource_ids),
        'estimated_hours': len(request.resource_ids) * 8.5,  # Mock calculation
        'tags': request.tags
    }


@router.get("/paths/{path_id}")
def get_learning_path(path_id: int, db: Session = Depends(get_db)):
    """Get learning path details"""
    return {
        'path_id': path_id,
        'title': 'From Beginner to ML Engineer',
        'description': 'Complete learning journey from basics to professional ML engineering',
        'creator_id': 201,
        'creator_name': 'MLExpert',
        'target_skill': 'Machine Learning',
        'target_level': 'advanced',
        'total_estimated_hours': 180,
        'difficulty_progression': 'gradual',
        'followers_count': 3421,
        'completion_count': 567,
        'success_rate': 78.5,
        'is_verified': True,
        'tags': ['machine-learning', 'data-science', 'python', 'career-path'],
        'modules': [
            {
                'module_id': 1,
                'title': 'Python Fundamentals',
                'resources_count': 5,
                'estimated_hours': 25,
                'is_required': True
            },
            {
                'module_id': 2,
                'title': 'Statistics & Math',
                'resources_count': 7,
                'estimated_hours': 35,
                'is_required': True
            },
            {
                'module_id': 3,
                'title': 'ML Algorithms',
                'resources_count': 12,
                'estimated_hours': 60,
                'is_required': True
            },
            {
                'module_id': 4,
                'title': 'Deep Learning',
                'resources_count': 8,
                'estimated_hours': 40,
                'is_required': True
            },
            {
                'module_id': 5,
                'title': 'MLOps & Deployment',
                'resources_count': 6,
                'estimated_hours': 20,
                'is_required': False
            }
        ]
    }


@router.post("/paths/{path_id}/enroll")
def enroll_in_path(
    path_id: int,
    user_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Enroll user in a learning path"""
    # Optimize path for user
    optimization_task = {
        'type': 'learning_path_optimization',
        'user_id': user_id,
        'path_id': path_id
    }

    response = study_buddy_agent.process_task(optimization_task)

    return {
        'status': 'success',
        'message': 'Successfully enrolled in learning path',
        'path_id': path_id,
        'user_id': user_id,
        'optimization': response.data,
        'next_steps': response.next_steps
    }


@router.get("/paths/{path_id}/progress/{user_id}")
def get_path_progress(path_id: int, user_id: int, db: Session = Depends(get_db)):
    """Get user's progress on a learning path"""
    return {
        'user_id': user_id,
        'path_id': path_id,
        'started_at': '2025-11-01T10:00:00',
        'last_activity': '2025-11-15T14:30:00',
        'completion_percentage': 42.5,
        'completed_modules': 2,
        'total_modules': 5,
        'total_time_spent_hours': 68.5,
        'pace_vs_estimate': 1.15,  # 15% faster than average
        'current_module': {
            'module_id': 3,
            'title': 'ML Algorithms',
            'progress': 35.0
        },
        'predicted_completion_date': '2025-12-28',
        'streak_days': 12,
        'milestones_achieved': [
            'First Module Complete',
            '50 Hours Practiced',
            '10 Day Streak'
        ]
    }


# ==================== Learning Curve Endpoints ====================

@router.post("/learning-curves/{user_id}/log-progress")
def log_learning_progress(
    user_id: int,
    request: LogLearningProgressRequest,
    db: Session = Depends(get_db)
):
    """Log a learning progress data point"""
    return {
        'status': 'success',
        'message': 'Progress logged successfully',
        'user_id': user_id,
        'skill': request.skill_name,
        'proficiency_score': request.proficiency_score,
        'hours_practiced': request.hours_practiced,
        'timestamp': datetime.now().isoformat()
    }


@router.get("/learning-curves/{user_id}/analyze")
def analyze_learning_curve(
    user_id: int,
    skill: str = Query(...),
    db: Session = Depends(get_db)
):
    """Analyze learning curve for a specific skill"""
    task = {
        'type': 'learning_curve_analysis',
        'user_id': user_id,
        'skill': skill
    }

    response = study_buddy_agent.process_task(task)

    return {
        'status': 'success',
        'user_id': user_id,
        'analysis': response.data,
        'recommendations': response.recommendations,
        'next_steps': response.next_steps
    }


@router.get("/learning-curves/{user_id}/dashboard")
def get_learning_dashboard(user_id: int, db: Session = Depends(get_db)):
    """Get comprehensive learning dashboard"""
    return {
        'user_id': user_id,
        'total_skills_tracked': 8,
        'total_hours_practiced': 342.5,
        'average_learning_velocity': 0.52,
        'skills_in_progress': [
            {
                'skill': 'Python',
                'proficiency': 78.5,
                'hours_practiced': 125.0,
                'phase': 'advanced',
                'plateau_status': False
            },
            {
                'skill': 'Machine Learning',
                'proficiency': 62.0,
                'hours_practiced': 98.5,
                'phase': 'intermediate',
                'plateau_status': False
            },
            {
                'skill': 'System Design',
                'proficiency': 45.0,
                'hours_practiced': 67.0,
                'phase': 'intermediate',
                'plateau_status': True
            }
        ],
        'skills_mastered': [
            {
                'skill': 'SQL',
                'mastery_level': 'expert',
                'proficiency': 92.0,
                'hours_invested': 52.0,
                'mastered_at': '2025-10-15'
            }
        ],
        'weekly_summary': {
            'hours_this_week': 18.5,
            'skills_practiced': 5,
            'proficiency_gain': 3.2,
            'streak_days': 6
        }
    }


# ==================== Recommendation Endpoints ====================

@router.post("/recommendations/content")
def get_content_recommendations(
    user_id: int = Query(...),
    learning_goals: List[str] = Query([]),
    time_available: Optional[int] = Query(None),
    budget_credits: Optional[float] = Query(None),
    db: Session = Depends(get_db)
):
    """Get personalized content recommendations"""
    context = RecommendationContext(
        user_id=user_id,
        user_skills=['Python', 'SQL', 'Data Analysis'],  # Mock - fetch from DB
        user_interests=learning_goals or ['Machine Learning', 'Web Development'],
        learning_goals=learning_goals,
        time_available=time_available,
        budget_credits=budget_credits
    )

    task = {
        'type': 'content_recommendation',
        'context': context
    }

    response = study_buddy_agent.process_task(task)

    return {
        'status': 'success',
        'user_id': user_id,
        'recommendations': response.data,
        'personalization_score': response.confidence * 100,
        'updated_at': datetime.now().isoformat()
    }


@router.get("/recommendations/study-partners/{user_id}")
def get_study_partner_recommendations(user_id: int, db: Session = Depends(get_db)):
    """Get study partner and group recommendations"""
    task = {
        'type': 'study_partner_matching',
        'user_id': user_id
    }

    response = study_buddy_agent.process_task(task)

    return {
        'status': 'success',
        'user_id': user_id,
        'matches': response.data,
        'recommendations': response.recommendations
    }


# ==================== Social Features Endpoints ====================

@router.post("/posts/create")
def create_post(
    request: CreatePostRequest,
    author_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Create a social post"""
    post = Post(
        post_id=hash(f"{author_id}{request.content}") % 100000,
        author_id=author_id,
        content=request.content,
        post_type=request.post_type,
        related_resource_id=request.related_resource_id,
        tags=request.tags,
        visibility=request.visibility
    )

    return {
        'status': 'success',
        'message': 'Post created successfully',
        'post': post.dict()
    }


@router.get("/feed/{user_id}")
def get_user_feed(
    user_id: int,
    limit: int = Query(20),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    """Get personalized feed for user"""
    # Mock feed data
    feed_items = [
        {
            'post_id': i,
            'author_id': 100 + i,
            'author_name': f'user_{100 + i}',
            'content': f'Just completed the ML course! Amazing experience. #{i}',
            'post_type': 'achievement',
            'created_at': f'2025-11-{16 - i}T{10 + i}:00:00',
            'likes_count': 20 + i * 5,
            'comments_count': 3 + i,
            'user_has_liked': False
        }
        for i in range(1, min(limit + 1, 21))
    ]

    return {
        'status': 'success',
        'user_id': user_id,
        'feed_items': feed_items,
        'total_count': 500,  # Mock total
        'offset': offset,
        'limit': limit
    }


# ==================== Q&A Endpoints ====================

@router.post("/questions/create")
def create_question(
    request: CreateQuestionRequest,
    asker_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Create a new question"""
    question = Question(
        question_id=hash(request.title) % 100000,
        asker_id=asker_id,
        title=request.title,
        content=request.content,
        tags=request.tags,
        difficulty_level=request.difficulty_level,
        bounty_credits=request.bounty_credits
    )

    return {
        'status': 'success',
        'message': 'Question posted successfully',
        'question': question.dict()
    }


@router.post("/questions/{question_id}/answer")
def answer_question(
    question_id: int,
    request: CreateAnswerRequest,
    answerer_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Post an answer to a question"""
    answer = Answer(
        answer_id=hash(f"{question_id}{answerer_id}") % 100000,
        question_id=question_id,
        answerer_id=answerer_id,
        content=request.content
    )

    return {
        'status': 'success',
        'message': 'Answer posted successfully',
        'answer': answer.dict()
    }


@router.get("/questions/{question_id}")
def get_question(question_id: int, db: Session = Depends(get_db)):
    """Get question with answers"""
    return {
        'question_id': question_id,
        'title': 'How to optimize neural network training?',
        'content': 'I\'m training a deep neural network and it\'s taking too long. What are the best practices?',
        'asker_id': 501,
        'asker_name': 'curious_learner',
        'tags': ['machine-learning', 'deep-learning', 'optimization'],
        'created_at': '2025-11-14T09:00:00',
        'views_count': 245,
        'answers_count': 7,
        'bounty_credits': 50.0,
        'is_answered': True,
        'answers': [
            {
                'answer_id': 1001,
                'answerer_id': 301,
                'answerer_name': 'ml_expert',
                'answerer_reputation': 94.5,
                'content': 'Here are the top techniques: 1) Use batch normalization...',
                'created_at': '2025-11-14T10:30:00',
                'upvotes': 15,
                'is_accepted': True,
                'is_expert_verified': True,
                'credits_awarded': 50.0
            }
        ]
    }


# ==================== Study Groups Endpoints ====================

@router.post("/study-groups/create")
def create_study_group(
    request: CreateStudyGroupRequest,
    creator_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Create a new study group"""
    group = StudyGroup(
        group_id=hash(request.name) % 10000,
        name=request.name,
        description=request.description,
        creator_id=creator_id,
        focus_skill=request.focus_skill,
        target_level=request.target_level,
        max_members=request.max_members,
        is_private=request.is_private,
        member_ids=[creator_id]
    )

    return {
        'status': 'success',
        'message': 'Study group created successfully',
        'group': group.dict()
    }


@router.post("/study-groups/{group_id}/join")
def join_study_group(
    group_id: int,
    user_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Join a study group"""
    return {
        'status': 'success',
        'message': 'Successfully joined study group',
        'group_id': group_id,
        'user_id': user_id,
        'member_count': 5
    }


@router.get("/study-groups/search")
def search_study_groups(
    skill: Optional[str] = Query(None),
    level: Optional[str] = Query(None),
    has_space: bool = Query(True),
    db: Session = Depends(get_db)
):
    """Search for study groups"""
    # Mock results
    groups = [
        {
            'group_id': i,
            'name': f'Study Group {i}',
            'focus_skill': skill or 'Python',
            'target_level': level or 'intermediate',
            'current_members': 6 + i,
            'max_members': 10,
            'has_space': True,
            'activity_level': 'high',
            'meeting_schedule': 'Tuesdays 7PM EST'
        }
        for i in range(1, 6)
    ]

    return {
        'status': 'success',
        'groups': groups,
        'total_count': len(groups)
    }


# ==================== Credits & Monetization Endpoints ====================

@router.get("/credits/balance/{user_id}")
def get_credit_balance(user_id: int, db: Session = Depends(get_db)):
    """Get user's credit balance"""
    return {
        'user_id': user_id,
        'available_credits': 1250.50,
        'pending_credits': 75.00,
        'lifetime_earned': 3850.25,
        'lifetime_spent': 2524.75,
        'current_month_earnings': 425.50
    }


@router.get("/credits/transactions/{user_id}")
def get_credit_transactions(
    user_id: int,
    limit: int = Query(20),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    """Get credit transaction history"""
    transactions = [
        {
            'transaction_id': i,
            'amount': 25.50,
            'type': 'earned',
            'reason': 'Resource views bonus',
            'timestamp': f'2025-11-{16 - i}T10:00:00',
            'status': 'completed'
        }
        for i in range(1, min(limit + 1, 21))
    ]

    return {
        'status': 'success',
        'user_id': user_id,
        'transactions': transactions,
        'total_count': 150,
        'offset': offset,
        'limit': limit
    }


@router.post("/credits/withdraw")
def request_withdrawal(
    user_id: int = Query(...),
    amount: float = Query(...),
    payment_method: str = Query(...),
    db: Session = Depends(get_db)
):
    """Request credit withdrawal"""
    fee = amount * 0.05  # 5% fee
    net_amount = amount - fee

    return {
        'status': 'success',
        'message': 'Withdrawal request submitted',
        'request_id': hash(f"{user_id}{amount}") % 100000,
        'user_id': user_id,
        'amount': amount,
        'transaction_fee': fee,
        'net_amount': net_amount,
        'payment_method': payment_method,
        'estimated_processing_time': '3-5 business days',
        'status': 'pending'
    }


# ==================== Platform Analytics Endpoints ====================

@router.get("/analytics/platform-health")
def get_platform_health(db: Session = Depends(get_db)):
    """Get platform health metrics"""
    analysis_data = {
        'analysis_type': 'platform_health',
        'timestamp': datetime.now().isoformat()
    }

    response = study_buddy_agent.analyze(analysis_data)

    return {
        'status': 'success',
        'health_metrics': response,
        'timestamp': datetime.now().isoformat()
    }


@router.get("/analytics/leaderboard")
def get_leaderboard(
    leaderboard_type: str = Query("reputation"),
    period: str = Query("monthly"),
    skill_filter: Optional[str] = Query(None),
    limit: int = Query(50),
    db: Session = Depends(get_db)
):
    """Get platform leaderboards"""
    # Mock leaderboard data
    rankings = [
        {
            'rank': i,
            'user_id': 1000 + i,
            'username': f'top_contributor_{i}',
            'score': 1000 - (i * 10),
            'badge': 'gold' if i <= 3 else 'silver' if i <= 10 else 'bronze'
        }
        for i in range(1, min(limit + 1, 51))
    ]

    return {
        'status': 'success',
        'leaderboard_type': leaderboard_type,
        'period': period,
        'skill_filter': skill_filter,
        'rankings': rankings,
        'last_updated': datetime.now().isoformat()
    }


# ==================== Agent Direct Access ====================

@router.post("/agent/task")
def run_agent_task(task: Dict[str, Any], db: Session = Depends(get_db)):
    """Direct access to Study Buddy Agent"""
    response = study_buddy_agent.process_task(task)

    return {
        'status': response.status,
        'agent_id': response.agent_id,
        'data': response.data,
        'confidence': response.confidence,
        'recommendations': response.recommendations,
        'next_steps': response.next_steps,
        'metadata': response.metadata
    }


@router.get("/agent/status")
def get_agent_status(db: Session = Depends(get_db)):
    """Get Study Buddy Agent status"""
    status = study_buddy_agent.get_status()

    return {
        'status': 'success',
        'agent_status': status
    }


# ==================== Notification Endpoints ====================

@router.get("/notifications/{user_id}")
def get_user_notifications(
    user_id: int,
    unread_only: bool = Query(False),
    limit: int = Query(50),
    offset: int = Query(0),
    db: Session = Depends(get_db)
):
    """Get user notifications"""
    # Mock notifications
    notifications = [
        {
            'notification_id': 1,
            'notification_type': 'question_answer',
            'title': 'New Answer to Your Question',
            'message': 'MLExpert answered your question about neural network optimization',
            'link_url': '/questions/12345',
            'related_user_id': 102,
            'is_read': False,
            'created_at': '2025-11-17T10:30:00',
            'priority': 'normal'
        },
        {
            'notification_id': 2,
            'notification_type': 'achievement',
            'title': 'Achievement Unlocked!',
            'message': 'You earned the "10 Day Learning Streak" badge',
            'link_url': '/achievements',
            'is_read': False,
            'created_at': '2025-11-17T09:00:00',
            'priority': 'high'
        },
        {
            'notification_id': 3,
            'notification_type': 'follow',
            'title': 'New Follower',
            'message': 'PythonGuru started following you',
            'link_url': '/profile/101',
            'related_user_id': 101,
            'is_read': True,
            'created_at': '2025-11-16T15:45:00',
            'priority': 'normal'
        },
        {
            'notification_id': 4,
            'notification_type': 'course_update',
            'title': 'Course Update',
            'message': 'New module added to "Advanced Python Design Patterns"',
            'link_url': '/resources/1',
            'related_resource_id': 1,
            'is_read': True,
            'created_at': '2025-11-15T12:20:00',
            'priority': 'normal'
        }
    ]

    if unread_only:
        notifications = [n for n in notifications if not n['is_read']]

    return {
        'status': 'success',
        'user_id': user_id,
        'notifications': notifications[offset:offset + limit],
        'unread_count': len([n for n in notifications if not n['is_read']]),
        'total_count': len(notifications)
    }


@router.post("/notifications/{notification_id}/mark-read")
def mark_notification_read(
    notification_id: int,
    user_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Mark notification as read"""
    return {
        'status': 'success',
        'notification_id': notification_id,
        'is_read': True,
        'read_at': datetime.now().isoformat()
    }


@router.post("/notifications/{user_id}/mark-all-read")
def mark_all_notifications_read(user_id: int, db: Session = Depends(get_db)):
    """Mark all notifications as read"""
    return {
        'status': 'success',
        'user_id': user_id,
        'marked_count': 2,
        'message': 'All notifications marked as read'
    }


@router.get("/notifications/{user_id}/preferences")
def get_notification_preferences(user_id: int, db: Session = Depends(get_db)):
    """Get user's notification preferences"""
    return {
        'status': 'success',
        'user_id': user_id,
        'preferences': {
            'email_notifications': True,
            'push_notifications': True,
            'question_answers': True,
            'new_followers': True,
            'comments_on_posts': True,
            'likes_on_content': True,
            'course_updates': True,
            'achievement_unlocked': True,
            'weekly_digest': True,
            'marketing_emails': False
        }
    }


@router.put("/notifications/{user_id}/preferences")
def update_notification_preferences(
    user_id: int,
    preferences: Dict[str, bool],
    db: Session = Depends(get_db)
):
    """Update user's notification preferences"""
    return {
        'status': 'success',
        'user_id': user_id,
        'message': 'Notification preferences updated',
        'preferences': preferences
    }


# ==================== Certificate Endpoints ====================

@router.get("/certificates/{user_id}")
def get_user_certificates(
    user_id: int,
    skill: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get user's certificates"""
    certificates = [
        {
            'certificate_id': 1001,
            'path_id': 1,
            'path_title': 'Python Advanced Mastery',
            'skill_name': 'Python',
            'proficiency_level': 'advanced',
            'issued_date': '2025-10-15T10:00:00',
            'completion_time_hours': 78.5,
            'final_score': 92.5,
            'verification_code': 'SB-PY-ADV-1001-2025',
            'certificate_url': '/certificates/download/1001',
            'issuer_name': 'Study Buddy Platform',
            'is_verified': True,
            'skills_covered': ['OOP', 'Design Patterns', 'Advanced Functions', 'Decorators'],
            'projects_completed': 5
        },
        {
            'certificate_id': 1002,
            'path_id': 3,
            'path_title': 'SQL Performance Optimization',
            'skill_name': 'SQL',
            'proficiency_level': 'intermediate',
            'issued_date': '2025-09-20T14:30:00',
            'completion_time_hours': 45.0,
            'final_score': 88.0,
            'verification_code': 'SB-SQL-INT-1002-2025',
            'certificate_url': '/certificates/download/1002',
            'issuer_name': 'Study Buddy Platform',
            'is_verified': True,
            'skills_covered': ['Query Optimization', 'Indexing', 'Performance Tuning'],
            'projects_completed': 3
        }
    ]

    if skill:
        certificates = [c for c in certificates if c['skill_name'].lower() == skill.lower()]

    return {
        'status': 'success',
        'user_id': user_id,
        'certificates': certificates,
        'total_count': len(certificates)
    }


@router.get("/certificates/verify/{verification_code}")
def verify_certificate(verification_code: str, db: Session = Depends(get_db)):
    """Verify a certificate by its verification code"""
    # Mock verification
    if verification_code.startswith('SB-'):
        return {
            'status': 'success',
            'is_valid': True,
            'certificate': {
                'certificate_id': 1001,
                'user_name': 'John Doe',
                'path_title': 'Python Advanced Mastery',
                'skill_name': 'Python',
                'proficiency_level': 'advanced',
                'issued_date': '2025-10-15T10:00:00',
                'verification_code': verification_code,
                'issuer_name': 'Study Buddy Platform'
            }
        }
    else:
        return {
            'status': 'error',
            'is_valid': False,
            'message': 'Invalid verification code'
        }


@router.post("/certificates/generate")
def generate_certificate(
    user_id: int = Query(...),
    path_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Generate certificate for completed learning path"""
    import secrets

    verification_code = f"SB-{secrets.token_hex(4).upper()}-{user_id}-{path_id}-2025"

    return {
        'status': 'success',
        'message': 'Certificate generated successfully',
        'certificate': {
            'certificate_id': hash(f"{user_id}{path_id}") % 100000,
            'user_id': user_id,
            'path_id': path_id,
            'verification_code': verification_code,
            'certificate_url': f'/certificates/download/{hash(f"{user_id}{path_id}") % 100000}',
            'issued_date': datetime.now().isoformat()
        }
    }


# ==================== Quiz/Assessment Endpoints ====================

@router.get("/quizzes/search")
def search_quizzes(
    skill: Optional[str] = Query(None),
    difficulty: Optional[str] = Query(None),
    limit: int = Query(20),
    db: Session = Depends(get_db)
):
    """Search for available quizzes"""
    quizzes = [
        {
            'quiz_id': 501,
            'title': 'Python Fundamentals Assessment',
            'description': 'Test your knowledge of Python basics',
            'skill_name': 'Python',
            'difficulty_level': 'beginner',
            'duration_minutes': 30,
            'passing_score': 70.0,
            'question_count': 20,
            'is_timed': True,
            'attempts_allowed': 3,
            'tags': ['python', 'basics', 'fundamentals']
        },
        {
            'quiz_id': 502,
            'title': 'Machine Learning Algorithms Quiz',
            'description': 'Comprehensive assessment of ML algorithms',
            'skill_name': 'Machine Learning',
            'difficulty_level': 'intermediate',
            'duration_minutes': 45,
            'passing_score': 75.0,
            'question_count': 30,
            'is_timed': True,
            'attempts_allowed': 2,
            'tags': ['machine-learning', 'algorithms', 'data-science']
        },
        {
            'quiz_id': 503,
            'title': 'SQL Query Optimization Challenge',
            'description': 'Advanced SQL optimization techniques',
            'skill_name': 'SQL',
            'difficulty_level': 'advanced',
            'duration_minutes': 60,
            'passing_score': 80.0,
            'question_count': 25,
            'is_timed': True,
            'attempts_allowed': 3,
            'tags': ['sql', 'optimization', 'database']
        }
    ]

    if skill:
        quizzes = [q for q in quizzes if q['skill_name'].lower() == skill.lower()]
    if difficulty:
        quizzes = [q for q in quizzes if q['difficulty_level'] == difficulty]

    return {
        'status': 'success',
        'quizzes': quizzes[:limit],
        'total_count': len(quizzes)
    }


@router.get("/quizzes/{quiz_id}")
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    """Get quiz details"""
    return {
        'quiz_id': quiz_id,
        'title': 'Python Fundamentals Assessment',
        'description': 'Test your knowledge of Python basics including data types, functions, and OOP',
        'skill_name': 'Python',
        'difficulty_level': 'beginner',
        'creator_id': 101,
        'creator_name': 'PythonGuru',
        'duration_minutes': 30,
        'passing_score': 70.0,
        'question_count': 20,
        'is_public': True,
        'is_timed': True,
        'attempts_allowed': 3,
        'tags': ['python', 'basics', 'fundamentals'],
        'average_score': 78.5,
        'completion_count': 1234
    }


@router.post("/quizzes/{quiz_id}/start")
def start_quiz_attempt(
    quiz_id: int,
    user_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Start a quiz attempt"""
    attempt_id = hash(f"{user_id}{quiz_id}{datetime.now()}") % 1000000

    return {
        'status': 'success',
        'message': 'Quiz attempt started',
        'attempt_id': attempt_id,
        'quiz_id': quiz_id,
        'user_id': user_id,
        'started_at': datetime.now().isoformat(),
        'questions': [
            {
                'question_id': 1,
                'question_text': 'What is the output of print(type([]))?',
                'question_type': 'multiple_choice',
                'options': ['<class \'list\'>', '<class \'dict\'>', '<class \'tuple\'>', '<class \'set\'>'],
                'points': 1
            },
            {
                'question_id': 2,
                'question_text': 'Which keyword is used to define a function in Python?',
                'question_type': 'multiple_choice',
                'options': ['function', 'def', 'func', 'define'],
                'points': 1
            }
            # ... more questions
        ]
    }


@router.post("/quizzes/attempts/{attempt_id}/submit")
def submit_quiz_attempt(
    attempt_id: int,
    answers: Dict[int, Any],
    user_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Submit quiz answers"""
    # Mock grading
    total_questions = 20
    correct_answers = 16
    score = (correct_answers / total_questions) * 100
    passed = score >= 70.0

    return {
        'status': 'success',
        'message': 'Quiz submitted successfully',
        'attempt_id': attempt_id,
        'user_id': user_id,
        'completed_at': datetime.now().isoformat(),
        'score': score,
        'passed': passed,
        'correct_answers': correct_answers,
        'total_questions': total_questions,
        'time_taken_minutes': 28.5,
        'feedback': 'Great job! You have a solid understanding of Python fundamentals.' if passed else 'Keep practicing! Review the topics you missed.'
    }


@router.get("/assessments/{user_id}/history")
def get_assessment_history(
    user_id: int,
    skill: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get user's assessment history"""
    assessments = [
        {
            'assessment_id': 2001,
            'quiz_id': 501,
            'quiz_title': 'Python Fundamentals Assessment',
            'skill_name': 'Python',
            'assessment_date': '2025-11-10T14:30:00',
            'score': 85.0,
            'passed': True,
            'proficiency_level': 'intermediate',
            'attempt_number': 1
        },
        {
            'assessment_id': 2002,
            'quiz_id': 503,
            'quiz_title': 'SQL Query Optimization Challenge',
            'skill_name': 'SQL',
            'assessment_date': '2025-10-25T10:15:00',
            'score': 72.0,
            'passed': False,
            'proficiency_level': 'beginner',
            'attempt_number': 2
        }
    ]

    if skill:
        assessments = [a for a in assessments if a['skill_name'].lower() == skill.lower()]

    return {
        'status': 'success',
        'user_id': user_id,
        'assessments': assessments,
        'total_count': len(assessments)
    }


@router.get("/assessments/{user_id}/skill-profile")
def get_skill_assessment_profile(user_id: int, db: Session = Depends(get_db)):
    """Get comprehensive skill assessment profile"""
    return {
        'status': 'success',
        'user_id': user_id,
        'skills_assessed': [
            {
                'skill_name': 'Python',
                'proficiency_level': 'intermediate',
                'overall_score': 85.0,
                'assessments_taken': 3,
                'last_assessment_date': '2025-11-10',
                'strengths': ['Data Structures', 'Functions', 'OOP'],
                'weaknesses': ['Decorators', 'Generators'],
                'recommended_resources': [1, 4, 9]
            },
            {
                'skill_name': 'SQL',
                'proficiency_level': 'beginner',
                'overall_score': 72.0,
                'assessments_taken': 2,
                'last_assessment_date': '2025-10-25',
                'strengths': ['Basic Queries', 'Joins'],
                'weaknesses': ['Query Optimization', 'Indexing', 'Transactions'],
                'recommended_resources': [3]
            }
        ],
        'next_assessments_recommended': [
            {
                'quiz_id': 502,
                'skill_name': 'Machine Learning',
                'title': 'Machine Learning Algorithms Quiz',
                'reason': 'Based on your Python skills, you might be ready for ML'
            }
        ]
    }
