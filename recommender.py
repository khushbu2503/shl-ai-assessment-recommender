import json

# load catalog
with open("catalog.json", "r") as file:
    catalog = json.load(file)

def recommend_assessments(user_query):

    user_query = user_query.lower()

    recommendations = []

    for assessment in catalog:

        name = assessment["name"].lower()

        score = 0

        # Technical roles
        if any(word in user_query for word in [
            "java", "python", "developer", "coding",
            "software", "technical", "backend"
        ]):

            if any(word in name for word in [
                "java", ".net", "coding", "technical"
            ]):
                score += 3

        # Personality / communication
        if any(word in user_query for word in [
            "communication", "personality",
            "behavior", "teamwork",
            "opq","motivation"
        ]):

            if any(word in name for word in [
                "opq", "personality", "behavioral",
                "motivation"
            ]):
                score += 3

        # Cognitive / aptitude
        if any(word in user_query for word in [
            "cognitive", "aptitude",
            "problem solving", "reasoning"
        ]):

            if any(word in name for word in [
                "verify", "cognitive", "ability"
            ]):
                score += 3

        # General keyword overlap
        for word in user_query.split():

            if word in name:
                score += 1

        if score > 0:

            recommendations.append({
                "name": assessment["name"],
                "url": assessment["url"],
                "test_type": assessment["test_type"],
                "score": score
            })

    # sort highest score first
    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    # top 10 only
    final_results = []

    for item in recommendations[:10]:

        final_results.append({
            "name": item["name"],
            "url": item["url"],
            "test_type": item["test_type"]
        })

    return final_results