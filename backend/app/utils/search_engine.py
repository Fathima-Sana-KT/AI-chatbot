def keyword_search(query, curriculum_text):
    keywords = query.lower().split()
    matched_lines = []

    for line in curriculum_text.split("\n"):
        if any(keyword in line.lower() for keyword in keywords):
            matched_lines.append(line.strip())

    return matched_lines
