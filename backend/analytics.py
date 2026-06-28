import os
from datetime import datetime, timedelta
from collections import Counter
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


def log_analysis(username: str, role: str, score: int, skill_gaps: list):
    """
    Logs every analysis run into analytics_log table.
    Called by Person 1 inside the /analyze endpoint.
    """
    try:
        result = supabase.table("analytics_log").insert({
            "username": username,
            "role": role,
            "score": score,
            "skill_gaps": skill_gaps
        }).execute()
        print(f"Logged analysis for {username} - {role}")
        return result.data
    except Exception as e:
        print(f"Error logging analysis: {e}")
        return None


def get_trending_gaps(role: str, days: int = 7) -> list:
    """
    Returns the most commonly missing skills for a role
    across all analysis runs in the last N days.
    """
    try:
        cutoff_date = (datetime.utcnow() - timedelta(days=days)).isoformat()

        result = supabase.table("analytics_log") \
            .select("skill_gaps") \
            .eq("role", role.lower().strip()) \
            .gte("created_at", cutoff_date) \
            .execute()

        if not result.data:
            print(f"No analytics data found for role: {role}")
            return []

        all_gaps = []
        for row in result.data:
            gaps = row.get("skill_gaps", [])
            if not gaps:
                continue
            for gap in gaps:
                # Handle both dict format and plain string format
                if isinstance(gap, dict):
                    skill_name = gap.get("skill", "")
                    if skill_name:
                        all_gaps.append(skill_name)
                elif isinstance(gap, str):
                    all_gaps.append(gap)

        if not all_gaps:
            return []

        gap_counts = Counter(all_gaps)
        trending = [skill for skill, count in gap_counts.most_common(10)]

        print(f"Trending gaps for '{role}': {trending}")
        return trending

    except Exception as e:
        print(f"Error fetching trending gaps: {e}")
        return []
def get_average_score(role: str) -> float:
    """
    Bonus function - returns average score for a role across all runs.
    Useful for the analytics dashboard.
    """
    try:
        result = supabase.table("analytics_log") \
            .select("score") \
            .eq("role", role) \
            .execute()

        if not result.data:
            return 0.0

        scores = [row["score"] for row in result.data if row.get("score") is not None]

        if not scores:
            return 0.0

        return round(sum(scores) / len(scores), 1)

    except Exception as e:
        print(f"Error calculating average score: {e}")
        return 0.0