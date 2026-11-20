import streamlit as st
import pandas as pd

# 1. Configuration de la page
st.set_page_config(page_title="Fragrance Recommender", page_icon="🧴", layout="wide")

# 2. Chargement des données
@st.cache_data
def charger_catalogue():
    return pd.read_csv("parfums.csv")

df = charger_catalogue()

# En-tête principal
st.title("🧴 Fragrance Recommender — Trouvez votre Signature Olfactive")
st.markdown("Répondez à **5 questions rapides** pour découvrir les parfums les plus adaptés à votre style et votre budget.")

# Navigation par onglets
tab1, tab2, tab3 = st.tabs(["🧭 Questionnaire & Résultats", "⚖️ Comparateur Face-à-Face", "📊 Catalogue Complet (150)"])

with tab1:
    with st.container(border=True):
        st.subheader("📝 Votre Profil Olfactif")
        
        col_q1, col_q2 = st.columns(2)
        with col_q1:
            q_gamme = st.radio(
                "1. Quelle gamme recherchez-vous ?",
                ["Peu importe (Tout voir)", "Dupes / Alternatives abordables", "Grandes marques (Designers)", "Haute parfumerie (Niche)"],
                horizontal=False
            )
            q_budget = st.slider("2. Quel est votre budget maximum (€) ?", min_value=20, max_value=350, value=90, step=5)
            q_intensite = st.select_slider(
                "3. Quelle tenue / présence souhaitez-vous ?",
                options=["Discret & léger", "Équilibré au quotidien", "Tenace & remarquable", "Mode Bête (Sillage massif)"],
                value="Tenace & remarquable"
            )

        with col_q2:
            q_ambiance = st.selectbox(
                "4. Quel univers olfactif vous attire le plus ?",
                [
                    "Peu importe, surprenez-moi",
                    "Frais, propre & énergisant (Agrumes, notes marines)",
                    "Chaud, sucré & gourmand (Vanille, épices, ambre)",
                    "Boisé, élégant & charismatique (Cèdre, cuir, santal)",
                    "Floral & raffiné (Rose, jasmin, fleurs blanches)"
                ]
            )
            q_moment = st.selectbox(
                "5. À quelle occasion allez-vous le porter principalement ?",
                [
                    "Polyvalent (Toutes occasions)",
                    "Tous les jours / Travail / Cours",
                    "Soirée / Rendez-vous / Sortie",
                    "Sport / Été / Vacances"
                ]
            )

        st.button("✨ Trouver mes parfums idéaux", type="primary", use_container_width=True)

    # Traduction des réponses du questionnaire en critères de scoring
    map_gamme = {
        "Peu importe (Tout voir)": "Toutes",
        "Dupes / Alternatives abordables": "Dupe",
        "Grandes marques (Designers)": "Designer",
        "Haute parfumerie (Niche)": "Niche"
    }
    map_tenue = {
        "Discret & léger": 6,
        "Équilibré au quotidien": 7,
        "Tenace & remarquable": 8,
        "Mode Bête (Sillage massif)": 9
    }

    cat_cible = map_gamme[q_gamme]
    tenue_min = map_tenue[q_intensite]

    df_filtre = df[(df["prix_eur"] <= q_budget) & (df["tenue_sur_10"] >= tenue_min)].copy()
    if cat_cible != "Toutes":
        df_filtre = df_filtre[df_filtre["categorie"] == cat_cible]

    def calculer_score_questionnaire(row):
        score = 20  # Base de compatibilité
        famille = str(row["famille"]).lower()
        occasion = str(row["occasion"]).lower()
        saison = str(row["saison"]).lower()

        # 1. Correspondance Univers Olfactif (35 pts)
        if q_ambiance == "Peu importe, surprenez-moi":
            score += 35
        elif "Frais" in q_ambiance and any(k in famille for k in ["frais", "aquatique", "hespéridé", "marin", "aromatique"]):
            score += 35
        elif "Chaud" in q_ambiance and any(k in famille for k in ["gourmand", "ambré", "vanillé", "épicé", "café", "lacté"]):
            score += 35
        elif "Boisé" in q_ambiance and any(k in famille for k in ["boisé", "cuiré", "chypré", "fougère"]):
            score += 35
        elif "Floral" in q_ambiance and any(k in famille for k in ["floral", "fruité"]):
            score += 35

        # 2. Correspondance Moment / Occasion (25 pts)
        if q_moment == "Polyvalent (Toutes occasions)":
            score += 25
        elif "Tous les jours" in q_moment and any(k in occasion for k in ["quotidien", "bureau", "polyvalent"]):
            score += 25
        elif "Soirée" in q_moment and any(k in occasion for k in ["soirée", "rendez-vous", "sortie", "club", "prestige"]):
            score += 25
        elif "Sport" in q_moment and (any(k in occasion for k in ["sport", "été", "vacances"]) or "printemps/été" in saison):
            score += 25

        # 3. Bonus Performance Tenue + Sillage (20 pts)
        score += (row["tenue_sur_10"] + row["sillage_sur_10"])
        return min(100, score)

    st.divider()

    if df_filtre.empty:
        st.warning("Aucun parfum ne correspond exactement à ce budget et cette intensité. Essayez d'augmenter légèrement votre budget ou de baisser l'intensité.")
    else:
        df_filtre["Score (%)"] = df_filtre.apply(calculer_score_questionnaire, axis=1)
        df_trie = df_filtre.sort_values(by=["Score (%)", "tenue_sur_10", "sillage_sur_10"], ascending=False)

        top = df_trie.iloc[0]
        k1, k2, k3 = st.columns(3)
        k1.metric("🥇 Recommandation N°1", f"{top['nom']}", f"{top['Score (%)']}% de compatibilité")
        k2.metric("📦 Sélection compatible", f"{len(df_trie)} parfums trouvés")
        k3.metric("💶 Budget moyen", f"{df_trie['prix_eur'].mean():.0f} €")

        st.subheader("✨ Votre sélection personnalisée")

        for _, p in df_trie.head(15).iterrows():
            with st.container(border=True):
                col_info, col_perf, col_prix = st.columns([3.5, 2, 1.2])
                
                with col_info:
                    st.subheader(f"{p['nom']} — {p['marque']}")
                    st.caption(f"Catégorie : **{p['categorie']}** | Famille : **{p['famille']}** | Saison : **{p['saison']}**")
                    if p["categorie"] == "Dupe" and p["inspiration"] != "Original":
                        st.info(f"💡 Alternative inspirée de : **{p['inspiration']}**")
                    st.markdown(f"**Pyramide olfactive :** {p['notes_tete']}, {p['notes_coeur']}, {p['notes_fond']}")
                
                with col_perf:
                    st.write(f"**Tenue :** {p['tenue_sur_10']}/10")
                    st.progress(p["tenue_sur_10"] / 10)
                    st.write(f"**Sillage :** {p['sillage_sur_10']}/10")
                    st.progress(p["sillage_sur_10"] / 10)
                    st.caption(f"Idéal pour : {p['occasion']}")
                
                with col_prix:
                    st.metric("Prix", f"{p['prix_eur']} €")
                    st.metric("Match", f"{p['Score (%)']} %")

with tab2:
    st.subheader("⚖️ Comparer deux parfums face-à-face")
    df["label_complet"] = df["nom"] + " (" + df["marque"] + " - " + df["categorie"] + ")"
    liste_labels = sorted(df["label_complet"].tolist())
    
    c_sel1, c_sel2 = st.columns(2)
    p1_label = c_sel1.selectbox("Parfum A", liste_labels, index=0)
    p2_label = c_sel2.selectbox("Parfum B", liste_labels, index=1)
    
    p1 = df[df["label_complet"] == p1_label].iloc[0]
    p2 = df[df["label_complet"] == p2_label].iloc[0]
    
    col_comp1, col_comp2 = st.columns(2)
    for col, p in [(col_comp1, p1), (col_comp2, p2)]:
        with col:
            with st.container(border=True):
                st.markdown(f"### {p['nom']} — {p['marque']}")
                st.write(f"**Catégorie :** {p['categorie']} | **Prix :** {p['prix_eur']} €")
                if p["categorie"] == "Dupe" and p["inspiration"] != "Original":
                    st.write(f"**Inspiration :** {p['inspiration']}")
                st.write(f"**Famille :** {p['famille']} | **Saison :** {p['saison']}")
                st.write(f"**Tenue / Sillage :** {p['tenue_sur_10']}/10 — {p['sillage_sur_10']}/10")
                st.info(f"**Notes :** {p['notes_tete']} • {p['notes_coeur']} • {p['notes_fond']}")

with tab3:
    st.subheader("📊 Base de données complète (150 références)")
    recherche = st.text_input("Rechercher un nom, une marque ou une inspiration (ex: Aventus, Lattafa, Vanille) :", "")
    df_affichage = df.drop(columns=["label_complet"], errors="ignore")
    if recherche.strip():
        masque = df_affichage.apply(lambda row: recherche.lower() in str(row.values).lower(), axis=1)
        df_affichage = df_affichage[masque]
    st.dataframe(df_affichage, use_container_width=True, hide_index=True)