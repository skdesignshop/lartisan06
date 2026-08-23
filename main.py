from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import telebot
import os

app = Flask(__name__)
CORS(app) # Autorise l'application web à communiquer avec le serveur

# --- CONFIGURATION TELEGRAM ---
# Remplace par le token que BotFather t'a donné
TOKEN = "8906879876:AAEEmd-mC2WPKBJzNd5qrFFTOVDusoTeohc" 
# Remplace par ton ID Telegram (une suite de chiffres trouvable via @userinfobot)
ADMIN_ID = "8763693036" 

bot = telebot.TeleBot(TOKEN)

# Affiche ta page web quand quelqu'un clique sur le lien
@app.route('/')
def index():
    return send_file('index.html')

# Reçoit la commande de la mini app et l'envoie sur Telegram
@app.route('/api/order', methods=['POST'])
def receive_order():
    data = request.json
    cart = data.get('cart', {})
    user = data.get('user', 'Client Web')
    
    if not cart:
        return jsonify({"status": "error", "message": "Panier vide"}), 400

    # Construction du message pour toi
    msg = f"🛒 *NOUVELLE COMMANDE*\n👤 *Client :* {user}\n\n"
    total = 0
    
    for key, item in cart.items():
        prix_ligne = item['price'] * item['qty']
        total += prix_ligne
        msg += f"• *{item['name']}* ({item['grams']}) x{item['qty']} - *{prix_ligne}€*\n"
    
    msg += f"\n💰 *TOTAL : {total}€*"
    
    try:
        # Le bot t'envoie le message en privé
        bot.send_message(ADMIN_ID, msg, parse_mode='Markdown')
        return jsonify({"status": "success", "message": "Commande envoyée !"})
    except Exception as e:
        print("Erreur d'envoi Telegram:", e)
        return jsonify({"status": "error", "message": "Erreur serveur"}), 500

if __name__ == '__main__':
    # Configuration pour Render
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
