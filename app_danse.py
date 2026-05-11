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

# --- 2. LISTE DES DANSES (Avec tes ajouts manuels) ---
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
    "She’s not afraid", "Blood Sweat and Beer", "Two pina coladas", "Fever Dream", "Oh love", 
    "No Remorse", "Orion", "Party in the Hills", "Good Lord", "A little bit harder", "Canadian Stomp", 
    "K is for Kicks", "Alligator Smile", "Delulu", "Any Man of Mine", "Devil's dance floor", 
    "Dancing in the country", "Cowboy Killer", "Ain't far from it", "Cupid Shuffle", "First Rodeo", 
    "Burning Love", "Blinding Lights", "Tie me up", "Greenlight", "Traveling Soldier", 
    "Ain't non love in Oklahoma", "Troubled Waters", "Jerusalema", "More", "Runaway Baby", 
    "Mesmorised", "Sounds like something I'd do", "Get Funky", "Infectious", "Around the fire", 
    "Hot Party", "Banana Boat", "I got better", "Jazz it up", "Country girl stomp", "Make it go Krazy", 
    "Country girl twerk", "Can't help myself", "Heart got teeth", "Lil bit", "Turn all the lights on", 
    "Love is a game", "Happen to me", "The other side", "Black betty worldwide", "Body and soul", 
    "Lemon squeezy", "Liar"
]

liste_danses = sorted(brute_danses)

st.write("---")
st.subheader("Quelles danses as-tu pratiquées ?")
selection = st.multiselect("Recherche et coche tes danses :", liste_danses)

# --- 3. NOUVELLES ZONES DE TEXTE ---
st.write("---")
col_aj, col_ap = st.columns(2)

with col_aj:
    danses_a_ajouter = st.text_area("Danses à ajouter (idées) :", placeholder="Ex: Une danse vue en festival...")

with col_ap:
    danses_a_apprendre = st.text_area("Danses à apprendre :", placeholder="Ex: Mémoriser les pas de 'The Wolf'...")
from streamlit_gsheets import GSheetsConnection

# --- 4. ENREGISTREMENT (Version Google Sheets) ---
conn = st.connection("gsheets", type=GSheetsConnection)

if st.button("Enregistrer les données", use_container_width=True):
    if nom and (selection or danses_a_ajouter or danses_a_apprendre):
        # 1. Lire les données existantes
        try:
            existing_data = conn.read(worksheet="Feuille 1", usecols=list(range(6)))
            existing_data = existing_data.dropna(how="all")
        except:
            existing_data = pd.DataFrame(columns=["Date", "Nom", "Lieu", "Danse", "À ajouter", "À apprendre"])

        # 2. Préparer les nouvelles lignes
        liste_pour_tableau = selection if selection else ["Note uniquement"]
        new_rows = pd.DataFrame({
            "Date": [date_danse.strftime("%d/%m/%Y")] * len(liste_pour_tableau),
            "Nom": [nom] * len(liste_pour_tableau),
            "Lieu": [lieu] * len(liste_pour_tableau),
            "Danse": liste_pour_tableau,
            "À ajouter": [danses_a_ajouter] * len(liste_pour_tableau),
            "À apprendre": [danses_a_apprendre] * len(liste_pour_tableau)
        })

        # 3. Fusionner et envoyer vers Google Sheets
        updated_df = pd.concat([existing_data, new_rows], ignore_index=True)
        conn.update(worksheet="Feuille 1", data=updated_df)
        
        st.success(f"C'est envoyé dans ton Google Sheets, {nom} ! 🤠")
        st.balloons()
    else:
        st.error("Remplis au moins ton nom et une information !")

# --- 5. HISTORIQUE ---
st.write("---")
if st.checkbox("Afficher l'historique complet"):
    if os.path.exists("journal_danse.csv"):
        df = pd.read_csv("journal_danse.csv")
        st.dataframe(df.sort_index(ascending=False), use_container_width=True)
    else:
        st.info("Aucun historique pour le moment.")
