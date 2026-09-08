from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from config import config
from models import db, Client, Dossier, Frais, Depens, Facture, Utilisateur
from datetime import datetime
import os

app = Flask(__name__)
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

db.init_app(app)

# Routes principales
@app.route('/')
def index():
    """Page d'accueil"""
    if app.config['TESTING'] is False:
        clients_count = Client.query.count()
        dossiers_count = Dossier.query.count()
        factures_count = Facture.query.count()
        return render_template('index.html', 
                             clients=clients_count,
                             dossiers=dossiers_count,
                             factures=factures_count)
    return render_template('index.html')

# ===== ROUTES CLIENTS =====

@app.route('/clients')
def clients_list():
    """Liste tous les clients"""
    page = request.args.get('page', 1, type=int)
    clients = Client.query.paginate(page=page, per_page=20)
    return render_template('clients/list.html', clients=clients)

@app.route('/clients/nouveau', methods=['GET', 'POST'])
def client_nouveau():
    """Créer un nouveau client"""
    if request.method == 'POST':
        client = Client(
            nom=request.form['nom'],
            prenom=request.form.get('prenom', ''),
            email=request.form['email'],
            telephone=request.form.get('telephone', ''),
            adresse=request.form.get('adresse', ''),
            code_postal=request.form.get('code_postal', ''),
            ville=request.form.get('ville', ''),
            type_client=request.form.get('type_client', 'particulier')
        )
        db.session.add(client)
        db.session.commit()
        return redirect(url_for('clients_list'))
    return render_template('clients/form.html')

@app.route('/clients/<int:id>')
def client_detail(id):
    """Détail d'un client"""
    client = Client.query.get_or_404(id)
    return render_template('clients/detail.html', client=client)

@app.route('/clients/<int:id>/editer', methods=['GET', 'POST'])
def client_editer(id):
    """Éditer un client"""
    client = Client.query.get_or_404(id)
    if request.method == 'POST':
        client.nom = request.form['nom']
        client.prenom = request.form.get('prenom', '')
        client.email = request.form['email']
        client.telephone = request.form.get('telephone', '')
        client.adresse = request.form.get('adresse', '')
        client.code_postal = request.form.get('code_postal', '')
        client.ville = request.form.get('ville', '')
        client.type_client = request.form.get('type_client', 'particulier')
        db.session.commit()
        return redirect(url_for('client_detail', id=client.id))
    return render_template('clients/form.html', client=client)

# ===== ROUTES DOSSIERS =====

@app.route('/dossiers')
def dossiers_list():
    """Liste tous les dossiers"""
    page = request.args.get('page', 1, type=int)
    statut = request.args.get('statut', 'tous')
    
    query = Dossier.query
    if statut != 'tous':
        query = query.filter_by(statut=statut)
    
    dossiers = query.paginate(page=page, per_page=20)
    return render_template('dossiers/list.html', dossiers=dossiers, statut=statut)

@app.route('/dossiers/nouveau', methods=['GET', 'POST'])
def dossier_nouveau():
    """Créer un nouveau dossier"""
    if request.method == 'POST':
        dossier = Dossier(
            client_id=request.form['client_id'],
            numero_dossier=request.form['numero_dossier'],
            objet=request.form['objet'],
            description=request.form.get('description', ''),
            taux_horaire=request.form.get('taux_horaire', 150.0),
            statut='ouvert'
        )
        db.session.add(dossier)
        db.session.commit()
        return redirect(url_for('dossier_detail', id=dossier.id))
    
    clients = Client.query.filter_by(actif=True).all()
    return render_template('dossiers/form.html', clients=clients)

@app.route('/dossiers/<int:id>')
def dossier_detail(id):
    """Détail d'un dossier"""
    dossier = Dossier.query.get_or_404(id)
    return render_template('dossiers/detail.html', dossier=dossier)

@app.route('/dossiers/<int:id>/editer', methods=['GET', 'POST'])
def dossier_editer(id):
    """Éditer un dossier"""
    dossier = Dossier.query.get_or_404(id)
    if request.method == 'POST':
        dossier.objet = request.form['objet']
        dossier.description = request.form.get('description', '')
        dossier.taux_horaire = float(request.form.get('taux_horaire', 150.0))
        dossier.statut = request.form.get('statut', 'ouvert')
        db.session.commit()
        return redirect(url_for('dossier_detail', id=dossier.id))
    
    clients = Client.query.filter_by(actif=True).all()
    return render_template('dossiers/form.html', dossier=dossier, clients=clients)

# ===== ROUTES FRAIS =====

@app.route('/frais/nouveau/<int:dossier_id>', methods=['GET', 'POST'])
def frais_nouveau(dossier_id):
    """Ajouter des frais à un dossier"""
    dossier = Dossier.query.get_or_404(dossier_id)
    
    if request.method == 'POST':
        heures = float(request.form['heures'])
        taux = float(request.form.get('taux_horaire', dossier.taux_horaire))
        
        frais = Frais(
            dossier_id=dossier_id,
            date_travail=datetime.strptime(request.form['date_travail'], '%Y-%m-%d').date(),
            heures=heures,
            taux_horaire=taux,
            description=request.form.get('description', ''),
            type_travail=request.form.get('type_travail', 'consultation')
        )
        frais.calculer_montant()
        db.session.add(frais)
        db.session.commit()
        return redirect(url_for('dossier_detail', id=dossier_id))
    
    return render_template('frais/form.html', dossier=dossier)

@app.route('/frais/<int:id>/supprimer')
def frais_supprimer(id):
    """Supprimer des frais"""
    frais = Frais.query.get_or_404(id)
    dossier_id = frais.dossier_id
    db.session.delete(frais)
    db.session.commit()
    return redirect(url_for('dossier_detail', id=dossier_id))

# ===== ROUTES DÉPENS =====

@app.route('/depens/nouveau/<int:dossier_id>', methods=['GET', 'POST'])
def depens_nouveau(dossier_id):
    """Ajouter des dépens à un dossier"""
    dossier = Dossier.query.get_or_404(dossier_id)
    
    if request.method == 'POST':
        depens = Depens(
            dossier_id=dossier_id,
            date_depens=datetime.strptime(request.form['date_depens'], '%Y-%m-%d').date(),
            type_depens=request.form['type_depens'],
            description=request.form.get('description', ''),
            montant=float(request.form['montant']),
            justificatif=request.form.get('justificatif', '')
        )
        db.session.add(depens)
        db.session.commit()
        return redirect(url_for('dossier_detail', id=dossier_id))
    
    return render_template('depens/form.html', dossier=dossier)

@app.route('/depens/<int:id>/supprimer')
def depens_supprimer(id):
    """Supprimer des dépens"""
    depens = Depens.query.get_or_404(id)
    dossier_id = depens.dossier_id
    db.session.delete(depens)
    db.session.commit()
    return redirect(url_for('dossier_detail', id=dossier_id))

# ===== ROUTES FACTURES =====

@app.route('/factures')
def factures_list():
    """Liste toutes les factures"""
    page = request.args.get('page', 1, type=int)
    statut = request.args.get('statut', 'tous')
    
    query = Facture.query
    if statut != 'tous':
        query = query.filter_by(statut=statut)
    
    factures = query.order_by(Facture.date_facture.desc()).paginate(page=page, per_page=20)
    return render_template('factures/list.html', factures=factures, statut=statut)

@app.route('/factures/nouvelle/<int:dossier_id>', methods=['GET', 'POST'])
def facture_nouvelle(dossier_id):
    """Créer une nouvelle facture"""
    dossier = Dossier.query.get_or_404(dossier_id)
    
    if request.method == 'POST':
        numero = request.form['numero_facture']
        tva = float(request.form.get('tva', 0.0))
        
        montant_frais = dossier.total_frais()
        montant_depens = dossier.total_depens()
        sous_total = montant_frais + montant_depens
        montant_tva = sous_total * (tva / 100)
        montant_total = sous_total + montant_tva
        
        facture = Facture(
            dossier_id=dossier_id,
            numero_facture=numero,
            montant_frais=montant_frais,
            montant_depens=montant_depens,
            montant_total=montant_total,
            tva=tva,
            montant_tva=montant_tva,
            statut='brouillon'
        )
        db.session.add(facture)
        db.session.commit()
        return redirect(url_for('facture_detail', id=facture.id))
    
    return render_template('factures/form.html', dossier=dossier)

@app.route('/factures/<int:id>')
def facture_detail(id):
    """Détail d'une facture"""
    facture = Facture.query.get_or_404(id)
    return render_template('factures/detail.html', facture=facture)

# API Routes pour les calculs
@app.route('/api/calculer-frais', methods=['POST'])
def api_calculer_frais():
    """API pour calculer les frais"""
    data = request.get_json()
    heures = float(data.get('heures', 0))
    taux = float(data.get('taux', 150))
    montant = heures * taux
    return jsonify({'montant': montant})

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)