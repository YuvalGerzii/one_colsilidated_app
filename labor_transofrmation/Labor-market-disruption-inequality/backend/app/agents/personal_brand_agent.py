"""
Personal Brand Builder Agent
Helps build and strengthen professional personal brand across platforms
"""

from typing import Dict, List, Any
from .base_agent import BaseAgent


class PersonalBrandBuilderAgent(BaseAgent):
    """AI agent specialized in personal brand development"""

    def __init__(self):
        super().__init__(
            name="Personal Brand Builder Agent",
            role="Personal Brand Strategist",
            expertise=[
                "Personal branding",
                "Content strategy",
                "Thought leadership",
                "Social media presence",
                "Professional visibility",
                "Online reputation"
            ]
        )

    def analyze_brand_strength(self, profile_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze current personal brand strength"""

        # Platform presence
        linkedin_score = self._score_linkedin_presence(profile_data.get("linkedin", {}))
        twitter_score = self._score_twitter_presence(profile_data.get("twitter", {}))
        github_score = self._score_github_presence(profile_data.get("github", {}))
        blog_score = self._score_blog_presence(profile_data.get("blog", {}))

        overall_score = (linkedin_score * 0.4 + twitter_score * 0.2 +
                        github_score * 0.2 + blog_score * 0.2)

        brand_strength = "strong" if overall_score >= 75 else "moderate" if overall_score >= 50 else "weak"

        return {
            "overall_brand_score": round(overall_score, 1),
            "brand_strength": brand_strength,
            "platform_scores": {
                "linkedin": linkedin_score,
                "twitter": twitter_score,
                "github": github_score,
                "blog": blog_score
            },
            "brand_pillars": self._identify_brand_pillars(profile_data),
            "content_strategy": self._create_content_strategy(profile_data),
            "quick_wins": self._get_brand_quick_wins(overall_score)
        }

    def create_thought_leadership_plan(self, expertise: List[str]) -> Dict[str, Any]:
        """Create thought leadership content plan"""

        content_pillars = expertise[:3]  # Top 3 expertise areas

        monthly_plan = {
            "linkedin_posts": {
                "frequency": "3-4 per week",
                "types": ["Industry insights", "Personal experiences", "Tips & advice", "Case studies"],
                "topics": [f"{pillar} best practices" for pillar in content_pillars]
            },
            "articles": {
                "frequency": "1-2 per month",
                "platforms": ["LinkedIn Articles", "Medium", "Dev.to"],
                "topic_ideas": [f"Deep dive into {pillar}" for pillar in content_pillars]
            },
            "engagement": {
                "frequency": "Daily",
                "actions": ["Comment on 5 posts", "Share 2 valuable articles", "Answer 1 question"]
            }
        }

        return {
            "content_pillars": content_pillars,
            "monthly_content_plan": monthly_plan,
            "content_templates": self._get_content_templates(),
            "growth_strategy": self._get_growth_strategy()
        }

    def _score_linkedin_presence(self, linkedin: Dict) -> float:
        """Score LinkedIn presence"""
        score = 0
        if linkedin.get("complete_profile"): score += 30
        if linkedin.get("posts_per_month", 0) >= 4: score += 25
        if linkedin.get("followers", 0) > 500: score += 25
        if linkedin.get("engagement_rate", 0) > 2: score += 20
        return score

    def _score_twitter_presence(self, twitter: Dict) -> float:
        """Score Twitter presence"""
        score = 0
        if twitter.get("followers", 0) > 100: score += 40
        if twitter.get("tweets_per_week", 0) >= 3: score += 30
        if twitter.get("engagement_rate", 0) > 1: score += 30
        return score

    def _score_github_presence(self, github: Dict) -> float:
        """Score GitHub presence"""
        score = 0
        if github.get("repos", 0) > 5: score += 40
        if github.get("contributions_per_week", 0) > 5: score += 30
        if github.get("stars", 0) > 50: score += 30
        return score

    def _score_blog_presence(self, blog: Dict) -> float:
        """Score blog/writing presence"""
        score = 0
        if blog.get("has_blog"): score += 40
        if blog.get("posts_count", 0) > 5: score += 30
        if blog.get("monthly_views", 0) > 100: score += 30
        return score

    def _identify_brand_pillars(self, profile_data: Dict) -> List[str]:
        """Identify key brand pillars"""
        return ["Technical expertise", "Problem solving", "Team collaboration"]

    def _create_content_strategy(self, profile_data: Dict) -> Dict[str, Any]:
        """Create content distribution strategy"""
        return {
            "primary_platform": "LinkedIn",
            "secondary_platforms": ["Twitter", "Dev.to"],
            "posting_frequency": "3-4x per week",
            "content_mix": "60% educational, 20% personal stories, 20% industry commentary"
        }

    def _get_brand_quick_wins(self, score: float) -> List[str]:
        """Get quick brand-building wins"""
        return [
            "Post 1 LinkedIn article about your expertise area",
            "Comment on 10 posts from industry leaders this week",
            "Share a project or achievement with lessons learned",
            "Connect with 20 people in your target industry"
        ]

    def _get_content_templates(self) -> List[Dict[str, str]]:
        """Get content templates"""
        return [
            {
                "type": "Lesson Learned",
                "template": "I learned [LESSON] when [SITUATION]. Here's what I'd do differently: [ADVICE]",
                "example": "I learned that code reviews save 10x the time they take when we had a production bug..."
            },
            {
                "type": "Tips Post",
                "template": "5 tips for [TOPIC]: 1) [TIP] 2) [TIP] 3) [TIP] 4) [TIP] 5) [TIP]",
                "example": "5 tips for writing clean code: 1) Use descriptive names..."
            }
        ]

    def _get_growth_strategy(self) -> Dict[str, str]:
        """Get growth strategy"""
        return {
            "months_1_3": "Build foundation: Complete profiles, start posting weekly, engage daily",
            "months_4_6": "Increase visibility: Post 3x/week, write 2 articles, speak at 1 event",
            "months_7_12": "Thought leadership: Post 4x/week, write monthly articles, build newsletter"
        }
