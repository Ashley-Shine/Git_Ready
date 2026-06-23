import sys
sys.path.append(".")

from backend.skills_taxonomy import get_taxonomy_from_supabase
from backend.skill_extractor import extract_skills
from shared.schemas import SAMPLE_CLEANED_REPO

# Use YOUR real taxonomy instead of the sample one
taxonomy = get_taxonomy_from_supabase("frontend developer")

if not taxonomy:
    print("❌ No taxonomy found in Supabase for this role")
else:
    print("✅ Taxonomy fetched successfully:")
    print(taxonomy)

    print("\n--- Running skill extraction ---")
    result = extract_skills([SAMPLE_CLEANED_REPO], taxonomy)

    print("\nMatched skills:")
    for s in result["matched"]:
        print(f"  {s['skill']} (via {s['matched_by']}, importance: {s['importance']})")

    print("\nMissing skills:")
    for s in result["missing"]:
        print(f"  {s['skill']} (importance: {s['importance']})")