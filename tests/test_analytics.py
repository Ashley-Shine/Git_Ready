import sys
sys.path.append(".")

from backend.analytics import log_analysis, get_trending_gaps, get_average_score

# Step 1 - Simulate a few analysis runs being logged
log_analysis("rahul123", "frontend developer", 78, ["docker", "typescript", "testing"])
log_analysis("priya456", "frontend developer", 65, ["typescript", "aws", "docker"])
log_analysis("amit789", "frontend developer", 82, ["docker", "graphql"])

# Step 2 - Check trending gaps
print("\n--- Trending Gaps ---")
trending = get_trending_gaps("frontend developer")
print(trending)

# Step 3 - Check average score
print("\n--- Average Score ---")
avg = get_average_score("frontend developer")
print(avg)