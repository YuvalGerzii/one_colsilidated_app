"""
Study Buddy Platform Models
A social network for mutual learning and knowledge sharing
"""
from typing import List, Dict, Optional
from datetime import datetime
from pydantic import BaseModel, Field


# ==================== User & Contributor Models ====================

class Contributor(BaseModel):
    """Platform contributor profile"""
    user_id: int
    username: str
    display_name: str
    bio: Optional[str] = None
    expertise_areas: List[str] = Field(default_factory=list)
    reputation_score: float = Field(default=0.0, description="0-100 reputation based on contributions")
    total_contributions: int = Field(default=0)
    total_credits_earned: float = Field(default=0.0)
    total_learners_helped: int = Field(default=0)
    verified_expert: bool = Field(default=False)
    join_date: datetime = Field(default_factory=datetime.now)
    followers_count: int = Field(default=0)
    following_count: int = Field(default=0)
    profile_image_url: Optional[str] = None
    social_links: Dict[str, str] = Field(default_factory=dict)


class LearnerProfile(BaseModel):
    """Learner profile on the platform"""
    user_id: int
    username: str
    learning_goals: List[str] = Field(default_factory=list)
    interests: List[str] = Field(default_factory=list)
    learning_style: Optional[str] = Field(None, description="visual, auditory, kinesthetic, reading_writing")
    current_skill_level: Dict[str, str] = Field(default_factory=dict, description="skill -> level mapping")
    hours_available_weekly: Optional[int] = None
    preferred_pace: Optional[str] = Field(None, description="fast, moderate, slow")
    credits_available: float = Field(default=0.0)
    total_courses_completed: int = Field(default=0)
    total_hours_learned: float = Field(default=0.0)


class SocialConnection(BaseModel):
    """Social connections between users"""
    follower_id: int
    following_id: int
    created_at: datetime = Field(default_factory=datetime.now)
    connection_strength: float = Field(default=0.0, description="0-1 based on interaction frequency")


# ==================== Knowledge Library Models ====================

class KnowledgeResource(BaseModel):
    """Individual knowledge resource in the library"""
    resource_id: int
    title: str
    description: str
    resource_type: str = Field(..., description="article, video, course, tutorial, book, podcast, interactive")
    content_url: Optional[str] = None
    content_text: Optional[str] = None
    creator_id: int
    tags: List[str] = Field(default_factory=list)
    difficulty_level: str = Field(..., description="beginner, intermediate, advanced, expert")
    estimated_time_hours: float
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    views_count: int = Field(default=0)
    likes_count: int = Field(default=0)
    bookmarks_count: int = Field(default=0)
    quality_score: float = Field(default=0.0, description="0-100 based on ratings and engagement")
    verified: bool = Field(default=False)
    is_free: bool = Field(default=True)
    price_credits: Optional[float] = None
    prerequisites: List[str] = Field(default_factory=list)
    learning_outcomes: List[str] = Field(default_factory=list)


class KnowledgeLibrary(BaseModel):
    """Curated knowledge library"""
    library_id: int
    title: str
    description: str
    curator_id: int
    resources: List[int] = Field(default_factory=list, description="List of resource IDs")
    tags: List[str] = Field(default_factory=list)
    is_public: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    followers_count: int = Field(default=0)
    quality_score: float = Field(default=0.0)


class ResourceRating(BaseModel):
    """User ratings for resources"""
    user_id: int
    resource_id: int
    rating: float = Field(..., ge=0, le=5, description="0-5 star rating")
    review_text: Optional[str] = None
    helpfulness_count: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.now)
    verified_completion: bool = Field(default=False)


# ==================== Learning Path Models ====================

class LearningPathNode(BaseModel):
    """Individual node in a learning path"""
    node_id: str
    resource_id: int
    order_index: int
    is_required: bool = Field(default=True)
    estimated_time_hours: float
    dependencies: List[str] = Field(default_factory=list, description="List of prerequisite node IDs")
    skills_gained: List[str] = Field(default_factory=list)


class LearningPath(BaseModel):
    """Structured learning path"""
    path_id: int
    title: str
    description: str
    creator_id: int
    target_skill: str
    target_level: str = Field(..., description="beginner, intermediate, advanced, expert")
    nodes: List[LearningPathNode] = Field(default_factory=list)
    total_estimated_hours: float
    difficulty_progression: str = Field(default="gradual", description="gradual, steep, mixed")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    followers_count: int = Field(default=0)
    completion_count: int = Field(default=0)
    success_rate: float = Field(default=0.0, description="Percentage of learners who completed successfully")
    is_verified: bool = Field(default=False)
    tags: List[str] = Field(default_factory=list)


class LearningPathProgress(BaseModel):
    """User's progress on a learning path"""
    user_id: int
    path_id: int
    started_at: datetime = Field(default_factory=datetime.now)
    last_activity: datetime = Field(default_factory=datetime.now)
    completed_nodes: List[str] = Field(default_factory=list)
    current_node_id: Optional[str] = None
    completion_percentage: float = Field(default=0.0)
    total_time_spent_hours: float = Field(default=0.0)
    is_completed: bool = Field(default=False)
    completion_date: Optional[datetime] = None
    pace_vs_estimate: float = Field(default=1.0, description="Actual pace / estimated pace")


# ==================== Learning Curve Models ====================

class LearningCurveDataPoint(BaseModel):
    """Single data point on learning curve"""
    timestamp: datetime
    skill_name: str
    proficiency_score: float = Field(..., ge=0, le=100, description="0-100 skill proficiency")
    hours_practiced: float
    assessment_type: Optional[str] = Field(None, description="quiz, project, peer_review, self_assessment")
    confidence_level: Optional[float] = Field(None, ge=0, le=100)


class LearningCurve(BaseModel):
    """Learning curve tracking for a skill"""
    user_id: int
    skill_name: str
    data_points: List[LearningCurveDataPoint] = Field(default_factory=list)
    current_proficiency: float = Field(default=0.0, ge=0, le=100)
    learning_velocity: float = Field(default=0.0, description="Proficiency gain per hour")
    plateau_detected: bool = Field(default=False)
    plateau_since: Optional[datetime] = None
    total_hours_practiced: float = Field(default=0.0)
    first_assessment: Optional[datetime] = None
    latest_assessment: Optional[datetime] = None
    improvement_rate: str = Field(default="normal", description="fast, normal, slow, plateau")
    predicted_mastery_date: Optional[datetime] = None


class SkillMastery(BaseModel):
    """Overall skill mastery tracking"""
    user_id: int
    skill_name: str
    mastery_level: str = Field(..., description="novice, beginner, intermediate, advanced, expert, master")
    proficiency_score: float = Field(..., ge=0, le=100)
    hours_invested: float
    projects_completed: int = Field(default=0)
    assessments_passed: int = Field(default=0)
    peer_endorsements: int = Field(default=0)
    verified_by_expert: bool = Field(default=False)
    last_practiced: datetime = Field(default_factory=datetime.now)
    retention_score: float = Field(default=100.0, description="Decreases over time without practice")


# ==================== Contribution & Monetization Models ====================

class Contribution(BaseModel):
    """Individual contribution to the platform"""
    contribution_id: int
    contributor_id: int
    contribution_type: str = Field(..., description="resource, path, review, answer, mentoring")
    resource_id: Optional[int] = None
    path_id: Optional[int] = None
    content: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    impact_score: float = Field(default=0.0, description="0-100 based on reach and quality")
    credits_earned: float = Field(default=0.0)
    views: int = Field(default=0)
    interactions: int = Field(default=0)
    learners_helped: int = Field(default=0)


class CreditTransaction(BaseModel):
    """Credit transactions for monetization"""
    transaction_id: int
    from_user_id: Optional[int] = None  # None for system rewards
    to_user_id: int
    amount: float
    transaction_type: str = Field(..., description="earned, purchased, transferred, spent, withdrawn")
    reason: str
    related_contribution_id: Optional[int] = None
    related_resource_id: Optional[int] = None
    timestamp: datetime = Field(default_factory=datetime.now)
    status: str = Field(default="completed", description="pending, completed, failed, reversed")


class RewardRule(BaseModel):
    """Rules for awarding credits"""
    rule_name: str
    trigger: str = Field(..., description="resource_view, resource_like, path_completion, quality_rating")
    credits_amount: float
    max_per_day: Optional[float] = None
    requires_verification: bool = Field(default=False)
    multiplier_for_quality: bool = Field(default=True)


class WithdrawalRequest(BaseModel):
    """Withdrawal request for earned credits"""
    request_id: int
    user_id: int
    amount: float
    payment_method: str = Field(..., description="paypal, bank_transfer, crypto")
    payment_details: Dict[str, str]
    requested_at: datetime = Field(default_factory=datetime.now)
    status: str = Field(default="pending", description="pending, approved, processing, completed, rejected")
    processed_at: Optional[datetime] = None
    transaction_fee: float = Field(default=0.0)
    net_amount: float


# ==================== Social Engagement Models ====================

class Post(BaseModel):
    """Social post on the platform"""
    post_id: int
    author_id: int
    content: str
    post_type: str = Field(..., description="text, resource_share, achievement, question, discussion")
    related_resource_id: Optional[int] = None
    related_path_id: Optional[int] = None
    tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.now)
    edited_at: Optional[datetime] = None
    likes_count: int = Field(default=0)
    comments_count: int = Field(default=0)
    shares_count: int = Field(default=0)
    visibility: str = Field(default="public", description="public, followers, private")


class Comment(BaseModel):
    """Comment on posts or resources"""
    comment_id: int
    author_id: int
    parent_id: Optional[int] = None  # For nested comments
    post_id: Optional[int] = None
    resource_id: Optional[int] = None
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    edited_at: Optional[datetime] = None
    likes_count: int = Field(default=0)
    is_expert_verified: bool = Field(default=False)


class Question(BaseModel):
    """Q&A system"""
    question_id: int
    asker_id: int
    title: str
    content: str
    tags: List[str] = Field(default_factory=list)
    difficulty_level: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    views_count: int = Field(default=0)
    answers_count: int = Field(default=0)
    is_answered: bool = Field(default=False)
    best_answer_id: Optional[int] = None
    bounty_credits: Optional[float] = None


class Answer(BaseModel):
    """Answer to a question"""
    answer_id: int
    question_id: int
    answerer_id: int
    content: str
    created_at: datetime = Field(default_factory=datetime.now)
    edited_at: Optional[datetime] = None
    upvotes: int = Field(default=0)
    is_accepted: bool = Field(default=False)
    is_expert_verified: bool = Field(default=False)
    credits_awarded: float = Field(default=0.0)


# ==================== Analytics & Insights Models ====================

class PlatformAnalytics(BaseModel):
    """Platform-wide analytics"""
    date: datetime
    total_users: int
    active_users_daily: int
    new_contributors: int
    resources_created: int
    paths_created: int
    total_learning_hours: float
    total_credits_distributed: float
    average_quality_score: float
    top_skills: List[Dict[str, any]]
    top_contributors: List[Dict[str, any]]


class ContributorAnalytics(BaseModel):
    """Analytics for individual contributors"""
    contributor_id: int
    period: str = Field(..., description="daily, weekly, monthly, all_time")
    total_views: int
    total_likes: int
    total_learners_reached: int
    credits_earned: float
    reputation_change: float
    top_performing_resources: List[int]
    engagement_rate: float = Field(default=0.0, description="Interactions / Views")
    growth_rate: float = Field(default=0.0, description="Period-over-period growth")


class LearnerAnalytics(BaseModel):
    """Analytics for learners"""
    user_id: int
    period: str = Field(..., description="daily, weekly, monthly, all_time")
    hours_learned: float
    resources_completed: int
    paths_in_progress: int
    paths_completed: int
    skills_acquired: List[str]
    average_rating_given: float
    streak_days: int
    learning_velocity: float = Field(default=0.0, description="Skills gained per hour")
    consistency_score: float = Field(default=0.0, ge=0, le=100, description="Learning consistency")


# ==================== Recommendation Models ====================

class RecommendationContext(BaseModel):
    """Context for generating recommendations"""
    user_id: int
    user_skills: List[str]
    user_interests: List[str]
    learning_goals: List[str]
    learning_style: Optional[str] = None
    time_available: Optional[int] = None
    budget_credits: Optional[float] = None


class ResourceRecommendation(BaseModel):
    """Recommended resource"""
    resource_id: int
    resource_title: str
    resource_type: str
    match_score: float = Field(..., ge=0, le=100, description="0-100 relevance score")
    match_reasons: List[str] = Field(default_factory=list)
    estimated_impact: float = Field(default=0.0, description="Expected learning value")
    creator_reputation: float


class PathRecommendation(BaseModel):
    """Recommended learning path"""
    path_id: int
    path_title: str
    match_score: float = Field(..., ge=0, le=100)
    match_reasons: List[str] = Field(default_factory=list)
    estimated_completion_time: float
    success_rate: float
    skills_to_gain: List[str]


class MentorRecommendation(BaseModel):
    """Recommended mentor/contributor"""
    mentor_id: int
    mentor_username: str
    expertise_match: float = Field(..., ge=0, le=100)
    expertise_areas: List[str]
    reputation_score: float
    teaching_style: Optional[str] = None
    availability: Optional[str] = None
    hourly_rate_credits: Optional[float] = None


# ==================== Study Group Models ====================

class StudyGroup(BaseModel):
    """Collaborative study groups"""
    group_id: int
    name: str
    description: str
    creator_id: int
    focus_skill: str
    target_level: str
    max_members: int = Field(default=10)
    current_members: int = Field(default=1)
    member_ids: List[int] = Field(default_factory=list)
    learning_path_id: Optional[int] = None
    meeting_schedule: Optional[str] = None
    is_private: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    active: bool = Field(default=True)


class StudySession(BaseModel):
    """Study session within a group"""
    session_id: int
    group_id: int
    host_id: int
    title: str
    description: Optional[str] = None
    scheduled_time: datetime
    duration_minutes: int
    attendees: List[int] = Field(default_factory=list)
    recording_url: Optional[str] = None
    notes_url: Optional[str] = None
    completed: bool = Field(default=False)


# ==================== Gamification Models ====================

class Achievement(BaseModel):
    """Platform achievements"""
    achievement_id: int
    name: str
    description: str
    icon_url: Optional[str] = None
    category: str = Field(..., description="learning, contribution, social, mastery")
    criteria: Dict[str, any]
    rarity: str = Field(..., description="common, uncommon, rare, epic, legendary")
    credits_reward: float = Field(default=0.0)
    xp_reward: int = Field(default=0)


class UserAchievement(BaseModel):
    """User's earned achievements"""
    user_id: int
    achievement_id: int
    earned_at: datetime = Field(default_factory=datetime.now)
    progress: float = Field(default=100.0, description="For multi-tier achievements")


class Leaderboard(BaseModel):
    """Leaderboard rankings"""
    leaderboard_type: str = Field(..., description="reputation, credits, learning_hours, contributions")
    period: str = Field(..., description="daily, weekly, monthly, all_time")
    skill_filter: Optional[str] = None
    rankings: List[Dict[str, any]] = Field(default_factory=list)
    last_updated: datetime = Field(default_factory=datetime.now)


# ==================== Notification Models ====================

class Notification(BaseModel):
    """User notifications"""
    notification_id: int
    user_id: int
    notification_type: str = Field(..., description="question_answer, comment, like, follow, achievement, course_update, message")
    title: str
    message: str
    link_url: Optional[str] = None
    related_user_id: Optional[int] = None
    related_resource_id: Optional[int] = None
    related_post_id: Optional[int] = None
    is_read: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    read_at: Optional[datetime] = None
    priority: str = Field(default="normal", description="low, normal, high, urgent")


class NotificationPreferences(BaseModel):
    """User notification preferences"""
    user_id: int
    email_notifications: bool = Field(default=True)
    push_notifications: bool = Field(default=True)
    question_answers: bool = Field(default=True)
    new_followers: bool = Field(default=True)
    comments_on_posts: bool = Field(default=True)
    likes_on_content: bool = Field(default=True)
    course_updates: bool = Field(default=True)
    achievement_unlocked: bool = Field(default=True)
    weekly_digest: bool = Field(default=True)
    marketing_emails: bool = Field(default=False)


# ==================== Certificate Models ====================

class Certificate(BaseModel):
    """Certificate for completed learning paths"""
    certificate_id: int
    user_id: int
    path_id: int
    path_title: str
    skill_name: str
    proficiency_level: str = Field(..., description="beginner, intermediate, advanced, expert")
    issued_date: datetime = Field(default_factory=datetime.now)
    completion_time_hours: float
    final_score: Optional[float] = Field(None, description="Final assessment score if applicable")
    certificate_url: Optional[str] = None
    verification_code: str = Field(..., description="Unique verification code")
    issuer_name: str = Field(default="Study Buddy Platform")
    is_verified: bool = Field(default=True)
    expires_at: Optional[datetime] = None
    skills_covered: List[str] = Field(default_factory=list)
    projects_completed: int = Field(default=0)


class CertificateTemplate(BaseModel):
    """Certificate design template"""
    template_id: int
    name: str
    description: str
    template_url: str
    background_color: str
    text_color: str
    border_style: str
    is_default: bool = Field(default=False)


# ==================== Skill Assessment Models ====================

class Quiz(BaseModel):
    """Quiz/assessment for skills"""
    quiz_id: int
    title: str
    description: str
    skill_name: str
    difficulty_level: str = Field(..., description="beginner, intermediate, advanced, expert")
    creator_id: int
    duration_minutes: int
    passing_score: float = Field(..., ge=0, le=100, description="Minimum score to pass")
    question_count: int
    is_public: bool = Field(default=True)
    is_timed: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    attempts_allowed: int = Field(default=3)
    tags: List[str] = Field(default_factory=list)


class QuizQuestion(BaseModel):
    """Individual quiz question"""
    question_id: int
    quiz_id: int
    question_text: str
    question_type: str = Field(..., description="multiple_choice, multiple_select, true_false, short_answer, coding")
    options: Optional[List[str]] = Field(None, description="For multiple choice questions")
    correct_answers: List[str] = Field(default_factory=list)
    explanation: Optional[str] = None
    points: int = Field(default=1)
    difficulty: str = Field(..., description="easy, medium, hard")
    code_template: Optional[str] = Field(None, description="For coding questions")
    test_cases: Optional[List[Dict[str, any]]] = Field(None, description="For coding questions")


class QuizAttempt(BaseModel):
    """User's quiz attempt"""
    attempt_id: int
    user_id: int
    quiz_id: int
    started_at: datetime = Field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None
    score: Optional[float] = Field(None, ge=0, le=100)
    passed: bool = Field(default=False)
    answers: Dict[int, any] = Field(default_factory=dict, description="question_id -> answer mapping")
    time_taken_minutes: Optional[float] = None
    attempt_number: int = Field(default=1)


class SkillAssessmentResult(BaseModel):
    """Overall skill assessment result"""
    assessment_id: int
    user_id: int
    skill_name: str
    assessment_date: datetime = Field(default_factory=datetime.now)
    overall_score: float = Field(..., ge=0, le=100)
    proficiency_level: str = Field(..., description="novice, beginner, intermediate, advanced, expert")
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    recommended_resources: List[int] = Field(default_factory=list, description="Resource IDs")
    recommended_paths: List[int] = Field(default_factory=list, description="Path IDs")
    next_assessment_date: Optional[datetime] = None
