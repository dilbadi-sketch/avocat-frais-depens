from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Client(db.Model):
    """Modèle pour les clients"""
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)
    prenom = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    telephone = db.Column(db.String(20))
    adresse = db.Column(db.Text)
    code_postal = db.Column(db.String(10))
    ville = db.Column(db.String(100))
    siret = db.Column(db.String(20))
    type_client = db.Column(db.String(50), default='particulier')  # particulier, entreprise
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    actif = db.Column(db.Boolean, default=True)
    
    # Relations
    dossiers = db.relationship('Dossier', backref='client', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Client {self.nom} {self.prenom}>'
    
    def nom_complet(self):
        return f"{self.prenom} {self.nom}".strip()


class Dossier(db.Model):
    """Modèle pour les dossiers clients"""
    __tablename__ = 'dossiers'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    numero_dossier = db.Column(db.String(50), unique=True, nullable=False)
    objet = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    date_ouverture = db.Column(db.DateTime, default=datetime.utcnow)
    date_fermeture = db.Column(db.DateTime)
    statut = db.Column(db.String(50), default='ouvert')  # ouvert, fermé, en attente
    taux_horaire = db.Column(db.Float, default=150.0)  # Taux par défaut
    notes = db.Column(db.Text)
    
    # Relations
    frais = db.relationship('Frais', backref='dossier', lazy=True, cascade='all, delete-orphan')
    depens = db.relationship('Depens', backref='dossier', lazy=True, cascade='all, delete-orphan')
    factures = db.relationship('Facture', backref='dossier', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Dossier {self.numero_dossier}>'
    
    def total_frais(self):
        return sum(f.montant for f in self.frais)
    
    def total_depens(self):
        return sum(d.montant for d in self.depens)
    
    def total_general(self):
        return self.total_frais() + self.total_depens()


class Frais(db.Model):
    """Modèle pour les frais horaires"""
    __tablename__ = 'frais'
    
    id = db.Column(db.Integer, primary_key=True)
    dossier_id = db.Column(db.Integer, db.ForeignKey('dossiers.id'), nullable=False)
    date_travail = db.Column(db.Date, nullable=False)
    heures = db.Column(db.Float, nullable=False)  # Nombre d'heures
    taux_horaire = db.Column(db.Float, nullable=False)
    description = db.Column(db.String(255))
    montant = db.Column(db.Float, nullable=False)
    type_travail = db.Column(db.String(100))  # consultation, rédaction, audience, etc.
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Frais {self.id} - {self.montant}€>'
    
    def calculer_montant(self):
        """Calcule automatiquement le montant"""
        self.montant = self.heures * self.taux_horaire
        return self.montant


class Depens(db.Model):
    """Modèle pour les dépens (déplacements, documents, etc.)"""
    __tablename__ = 'depens'
    
    id = db.Column(db.Integer, primary_key=True)
    dossier_id = db.Column(db.Integer, db.ForeignKey('dossiers.id'), nullable=False)
    date_depens = db.Column(db.Date, nullable=False)
    type_depens = db.Column(db.String(100), nullable=False)  # deplacement, photocopie, etc.
    description = db.Column(db.String(255))
    montant = db.Column(db.Float, nullable=False)
    justificatif = db.Column(db.String(255))  # chemin du fichier
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Depens {self.type_depens} - {self.montant}€>'


class Facture(db.Model):
    """Modèle pour les factures"""
    __tablename__ = 'factures'
    
    id = db.Column(db.Integer, primary_key=True)
    dossier_id = db.Column(db.Integer, db.ForeignKey('dossiers.id'), nullable=False)
    numero_facture = db.Column(db.String(50), unique=True, nullable=False)
    date_facture = db.Column(db.DateTime, default=datetime.utcnow)
    date_echeance = db.Column(db.Date)
    montant_total = db.Column(db.Float, nullable=False)
    montant_frais = db.Column(db.Float)
    montant_depens = db.Column(db.Float)
    tva = db.Column(db.Float, default=0.0)
    montant_tva = db.Column(db.Float, default=0.0)
    statut = db.Column(db.String(50), default='brouillon')  # brouillon, emise, payee, partielle
    notes = db.Column(db.Text)
    fichier_pdf = db.Column(db.String(255))  # chemin du PDF généré
    date_paiement = db.Column(db.DateTime)
    
    def __repr__(self):
        return f'<Facture {self.numero_facture}>'


class Utilisateur(db.Model):
    """Modèle pour les utilisateurs/avocats"""
    __tablename__ = 'utilisateurs'
    
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(255), nullable=False)
    prenom = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    telephone = db.Column(db.String(20))
    cabinet = db.Column(db.String(255))
    adresse_cabinet = db.Column(db.Text)
    numero_barreau = db.Column(db.String(50))
    taux_horaire_defaut = db.Column(db.Float, default=150.0)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)
    actif = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<Utilisateur {self.nom} {self.prenom}>'
    
    def nom_complet(self):
        return f"{self.prenom} {self.nom}".strip()
