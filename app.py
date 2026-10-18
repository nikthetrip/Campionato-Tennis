import streamlit as st
import streamlit.components.v1 as components

# Configurazione della pagina a tutto schermo
st.set_page_config(
    page_title="Tennis Club 6 Amici - Campionato & Torneo",
    page_icon="🎾",
    layout="wide",
)

# Codice HTML/CSS/JS originale super curato ed elegante
html_code = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tennis Club 6 Amici - Campionato & Torneo Mensile</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        tennis: {
                            green: '#1a472a',
                            lightgreen: '#2d5a27',
                            yellow: '#ccff00',
                            court: '#2c5e3b',
                            clay: '#c2593f',
                            dark: '#111827',
                            card: '#1f2937',
                            accent: '#eab308'
                        }
                    },
                    fontFamily: {
                        sans: ['Outfit', 'sans-serif']
                    }
                }
            }
        }
    </script>
    <style>
        body {
            background-color: #0d1117;
            color: #f3f4f6;
        }
        .court-bg {
            background: radial-gradient(circle, rgba(26,71,42,0.6) 0%, rgba(13,17,23,1) 100%);
        }
        .glow-yellow {
            box-shadow: 0 0 15px rgba(204, 255, 0, 0.3);
        }
    </style>
</head>
<body class="min-h-screen font-sans court-bg p-4 md:p-8">
    <div class="max-w-4xl mx-auto">
        <header class="text-center mb-8">
            <h1 class="text-4xl font-extrabold text-tennis-yellow mb-2"><i class="fa-solid fa-tennis-ball"></i> Tennis Club 6 Amici</h1>
            <p class="text-gray-400">Campionato Continuo & Torneo Mensile a Set Unico</p>
        </header>

        <div class="bg-tennis-card p-6 rounded-2xl border border-gray-800 shadow-xl mb-6">
            <h2 class="text-xl font-bold mb-4 text-tennis-yellow"><i class="fa-solid fa-trophy"></i> Benvenuti nella Web App Ufficiale</h2>
            <p class="text-gray-300 leading-relaxed mb-4">
                Questa applicazione mantiene la grafica e l'esperienza d'uso che preferisci, accessibile tramite il tuo link cloud fisso. 
                Puoi aggiornare i dati e la configurazione direttamente dal codice sorgente su GitHub: chiunque aprirà il link vedrà sempre l'ultima versione aggiornata in tempo reale!
            </p>
            <div class="p-4 bg-tennis-dark rounded-xl border border-gray-700">
                <span class="text-tennis-yellow font-semibold">Stato del sistema:</span> Online e sincronizzato via GitHub Cloud.
            </div>
        </div>
    </div>
</body>
</html>
"""

# Renderizza l'HTML con altezza ottimizzata all'interno di Streamlit
components.html(html_code, height=750, scrolling=True)
