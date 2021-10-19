def count_variants(event_log,return_variants=False):
    current_case = ""
    current_variant = ""
    caseIDColName = "Case ID"
    activityColName = "Activity"
    variants = set()
    for index, row in event_log.iterrows():
        activity = row[activityColName]
        if row[caseIDColName] != current_case:
            variants.add(current_variant)
            current_variant = ""
            current_case = row[caseIDColName]
        current_variant = current_variant + "@" + activity
    variants.add(current_variant)
    if return_variants:
        return len(variants) - 1, variants
    else:
        return len(variants) - 1