def create_profiles(df):
    # --- Step 1: Prepare data ---
    numeric_df = df.select_dtypes(include=["number"]).copy()
    numeric_df["cluster"] = df["cluster"]

    profile = numeric_df.groupby("cluster").mean()

    descriptions = {}
    cluster_names = {}

    # --- Step 2: Generate intelligent descriptions ---
    for cluster, row in profile.iterrows():
        traits = []

        energy = row.get("energy", 0)
        dance = row.get("danceability", 0)
        acoustic = row.get("acousticness", 0)
        live = row.get("liveness", 0)
        instrumental = row.get("instrumentalness", 0)

        # Energy
        if energy > 0.75:
            traits.append("High energy")
        elif energy < 0.4:
            traits.append("Low energy")
        else:
            traits.append("Moderate energy")

        # Danceability
        if dance > 0.6:
            traits.append("Danceable")
        elif dance < 0.4:
            traits.append("Less danceable")

        # Acoustic
        if acoustic > 0.5:
            traits.append("Acoustic vibe")

        # Live feel
        if live > 0.6:
            traits.append("Live performance feel")

        # Instrumental
        if instrumental > 0.5:
            traits.append("Instrumental heavy")

        # Final description
        desc = " • ".join(traits)
        descriptions[cluster] = desc

        # --- Step 3: Assign smart cluster names ---
        # --- Smart cluster naming ---
        if "Live performance feel" in desc:
            name = "🎤 Live Concert Energy"

        elif "High energy" in desc and "Danceable" in desc:
            name = "⚡ Energetic Dance Hits"

        elif "High energy" in desc:
            name = "🔥 Energetic Rock"

        elif "Acoustic vibe" in desc:
            name = "🎸 Acoustic Chill"

        elif "Low energy" in desc:
            name = "🌙 Calm & Relax"

        elif "Moderate energy" in desc:
            name = "🎧 Balanced Listening"

        else:
            name = "🎶 Mixed Profile"

        cluster_names[cluster] = name

    return profile, descriptions, cluster_names