import streamlit as st
import pandas as pd
import os

# Configuration de la page
st.set_page_config(page_title="Mon Suivi de Danse Country", page_icon="🤠")

st.title("🤠 Mon Journal de Danse Country")

# --- 1. SAISIE DES INFORMATIONS ---
col1, col2 = st.columns(2)

with col1:
    nom = st.text_input("Nom de la personne :", placeholder="Ton nom ici")
    date_danse = st.date_input("Date de la soirée :")

with col2:
    lieu = st.text_input("Où as-tu dansé ?", placeholder="Ex: Festival, Bar, Salle...")

# --- 2. LISTE DES DANSES ---
# Ta liste brute
brute_danses = [
    "Cotton Eye Joe", "Electric Slide (Man I Feel Like a Woman)", "Footloose", "A Bar Song - Tipsy", 
    "High Horse", "Country as a Boy Can Be", "Fireball", "Nothing But You", "Damn!", "American Kids", 
    "Timber / Old Town Road", "First Kiss", "All Aboard (My Baby Thinks She’s a Train)", 
    "Save a Horse - Ride a Cowboy", "The Outlaw (Whiskey Drinkin)", "Austin", "Always Humble (Humble)", 
    "Boots on Bars", "Copper Head Road", "What Makes You Country", "It Happens", "9 to 5", 
    "Back to the Start", "Cowboy Boogie", "I like it I love it", "Flatliner", "Going Ham (Crank it Up)", 
    "Glass of Wine (Cry to me)", "Burn It to the Ground", "Whiskey Whiskey (1,2,3,4)", 
    "Pieces to the Puzzle (Damn I Love Miami)", "Wobble", "Country Girl Shake", "Good Time", 
    "Give Me Shivers (Shivers)", "Head Over Boots", "Ready For It (This is It)", "Askin’ Questions", 
    "Raised Like That", "Swamp Thing", "Walkin on Me", "Banjo!", "Anthem", "Half Past Tipsy (1-2 Many)", 
    "Countdown (Turn Around 5,4,3,2,1)", "When It Rains It Pours", "Heel Toe Rodeo (Cowboy Up)", 
    "Blame’s On You (Blame)", "Shakin’ In Them Boots", "One More", "Wild and Free", "PHAT", "Cowboy Up", 
    "Honky Tonk Way (I See Country)", "Walk The Line (Freight Train)", "Irish Boots", 
    "Doctor Doctor (Bad Case Of Loving You)", "Where I Belong (Où on dansait autrefois)", "Fuego", 
    "Turn Me Loose", "Good Vibes Only (Do Something Crazy)", "Lightning Polka (Sin Wagon)", 
    "Stuck Like Glue", "Bombshell Stomp", "Off The Chain (Can’t Believe It)", "Bloodline", 
    "Stomping Ground", "Miles On It", "Chill Factor (Last Night)", "Aces and Eights (Whip It)", 
    "Come my Way", "Leave it Up", "The Sphinx (Medellin)", "Makin’ It Hot (Hot)", "Baby Slow Down (Slow Low)", 
    "Sway", "Young Forever", "16 steps", "El Passo", "3,2,1", "Three Tequila Floor (P)", 
    "Three Tequila Floor", "BucketSeat", "Tush Push", "Noise", "My Maria", "Bring Down the House", 
    "Take It Off", "Makin’ Moves", "Backseat Driver", "Soldier", "The Wolf", "Stomp 2,3,4", "Memory Lane", 
    "Scream", "Cooler Than Me", "Azucar (Café Con Leche)", "Yellow Lines", "Take Me to the Beach", 
    "Fake ID", "Wagon Wheel", "L’amour à p’tites gorgées", "Rodeo Queen", "Bacco Perbacco", "Got to Be Funky", 
    "Flex", "Liquor Talking", "Danse des lutins", "Charleston", "If Jesus Loves Me", "OMG", "Little Bird", 
    "This Bar", "PYT", "I Was On a Boat That Day", "Mindset", "Holy Moly", "Miss Thang", "The world", "Up", 
    "No truck song", "Dig Your Heels (Here’s to you and I)", "Count the beers (algo contigo)", 
    "I showed you the door", "Wild Wild West", "Descarada", "The Vibe", "Everyone needs a hero", 
    "Double D", "Rings (P)", "Toes (P)", "Good Girl", "Black Betty’s", "Bulletproof", "Rude Dude", 
    "Straight Line", "Stetson", "The feeling", "Shot for shot", "Shake señora", "Homecoming", 
    "Do my thing", "Heather on the hill", "Rattlesnake Kiss", "Get Wild", "Happy Hour", "5,6,7,8", 
    "5 divas", "Hoedown", "Sticks and Stones", "King of Clubs", "Beer Problem", "21 Reasons", 
    "She’s not afraid", "Blood Sweat and Beer", "Two pina coladas", "Fever Dream", "Oh love"
]

# Tri alphabétique
liste_danses = sorted(brute_danses)

st.write("---")
st.subheader("Quelles danses as-tu pratiquées ?")

# Affichage sous forme de multiselect (plus propre pour 158 danses)
selection = st.multiselect("Recherche et coche tes danses :", liste_danses)

# --- 3. ENREGISTREMENT ---
if st.button("Enregistrer les données", use_container_width=True):
    if nom and selection:
        # Préparation du tableau
        nouveau_suivi = pd.DataFrame({
            "Date": [date_danse.strftime("%d/%m/%Y")] * len(selection),
            "Nom": [nom] * len(selection),
            "Lieu": [lieu] * len(selection),
            "Danse": selection
        })
        
        # Sauvegarde CSV
        fichier = "journal_danse.csv"
        if not os.path.isfile(fichier):
            nouveau_suivi.to_csv(fichier, index=False)
        else:
            nouveau_suivi.to_csv(fichier, mode='a', header=False, index=False)
            
        st.success(f"Bravo {nom} ! Tes {len(selection)} danses à {lieu if lieu else 'la soirée'} sont enregistrées. ✅")
        st.balloons()
    else:
        st.error("N'oublie pas d'entrer ton nom et de choisir au moins une danse !")

# --- 4. HISTORIQUE ---
st.write("---")
if st.checkbox("Afficher l'historique complet"):
    if os.path.exists("journal_danse.csv"):
        df = pd.read_csv("journal_danse.csv")
        st.dataframe(df.sort_index(ascending=False), use_container_width=True)
    else:
        st.info("Aucun historique pour le moment.")