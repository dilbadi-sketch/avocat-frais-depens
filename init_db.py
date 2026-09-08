#!/usr/bin/env python
# -*- coding: utf-8 -*-

from app import app, db
from models import Client, Dossier, Frais, Depens, Facture, Utilisateur
from datetime import datetime, timedelta

def init_database():
    """Initialise la base de données avec des données de test"""
    with app.app_context():
        # Créer les tables
        db.create_all()
        print("✓ Tables créées avec succès")
        
        # Ajouter un utilisateur par défaut
        if Utilisateur.query.count() == 0:
            utilisateur = Utilisateur(
                nom="Martin",
                prenom="Maître",
                email="maitre@cabinet.fr",
                telephone="01 23 45 67 89",
                cabinet="Cabinet Martin",
                adresse_cabinet="123 Avenue de la République, 75011 Paris",
                numero_barreau="75001",
                taux_horaire_defaut=150.0
            )
            db.session.add(utilisateur)
            print("✓ Utilisateur par défaut créé")
        
        # Ajouter des clients de test
        if Client.query.count() == 0:
            clients = [
                Client(
                    nom="Dupont",
                    prenom="Jean",
                    email="jean.dupont@example.com",
                    telephone="06 12 34 56 78",
                    adresse="45 Rue de la Paix, 75002 Paris",
                    code_postal="75002",
                    ville="Paris",
                    type_client="particulier"
                ),
                Client(
                    nom="TechCorp",
                    email="contact@techcorp.fr",
                    telephone="01 98 76 54 32",
                    adresse="789 Boulevard de l'Innovation, 92400 Courbevoie",
                    code_postal="92400",
                    ville="Courbevoie",
                    siret="12345678901234",
                    type_client="entreprise"
                ),
                Client(
                    nom="Bernard",
                    prenom="Marie",
                    email="marie.bernard@example.com",
                    telephone="06 98 76 54 32",
                    adresse="12 Avenue Montaigne, 75008 Paris",
                    code_postal="75008",
                    ville="Paris",
                    type_client="particulier"
                )
            ]
            for client in clients:
                db.session.add(client)
            print("✓ Clients de test créés")
        
        db.session.commit()
        
        # Ajouter des dossiers de test
        if Dossier.query.count() == 0:
            client1 = Client.query.filter_by(prenom="Jean").first()
            client2 = Client.query.filter_by(nom="TechCorp").first()
            
            if client1:
                dossier1 = Dossier(
                    client_id=client1.id,
                    numero_dossier="2024-001",
                    objet="Succession familiale",
                    description="Gestion de succession - Partage de biens immobiliers et mobiliers",
                    taux_horaire=150.0,
                    statut="ouvert"
                )
                db.session.add(dossier1)
                print("✓ Dossier 1 créé")
            
            if client2:
                dossier2 = Dossier(
                    client_id=client2.id,
                    numero_dossier="2024-002",
                    objet="Contentieux commercial",
                    description="Litige avec prestataire - Réclamation de dommages et intérêts",
                    taux_horaire=200.0,
                    statut="ouvert"
                )
                db.session.add(dossier2)
                print("✓ Dossier 2 créé")
        
        db.session.commit()
        
        # Ajouter des frais de test
        if Frais.query.count() == 0:
            dossier = Dossier.query.first()
            if dossier:
                frais_list = [
                    Frais(
                        dossier_id=dossier.id,
                        date_travail=datetime.now().date() - timedelta(days=5),
                        heures=2.5,
                        taux_horaire=150.0,
                        description="Consultation initiale et analyse du dossier",
                        type_travail="consultation"
                    ),
                    Frais(
                        dossier_id=dossier.id,
                        date_travail=datetime.now().date() - timedelta(days=3),
                        heures=4.0,
                        taux_horaire=150.0,
                        description="Rédaction de courrier recommandé",
                        type_travail="rédaction"
                    ),
                    Frais(
                        dossier_id=dossier.id,
                        date_travail=datetime.now().date() - timedelta(days=1),
                        heures=1.5,
                        taux_horaire=150.0,
                        description="Préparation audience",
                        type_travail="audience"
                    )
                ]
                for frais in frais_list:
                    frais.calculer_montant()
                    db.session.add(frais)
                print("✓ Frais de test créés")
        
        db.session.commit()
        
        # Ajouter des dépens de test
        if Depens.query.count() == 0:
            dossier = Dossier.query.first()
            if dossier:
                depens_list = [
                    Depens(
                        dossier_id=dossier.id,
                        date_depens=datetime.now().date() - timedelta(days=4),
                        type_depens="déplacement",
                        description="Trajet Paris - Versailles (transport)",
                        montant=45.50
                    ),
                    Depens(
                        dossier_id=dossier.id,
                        date_depens=datetime.now().date() - timedelta(days=2),
                        type_depens="photocopies",
                        description="Copies de documents (250 pages)",
                        montant=25.00
                    ),
                    Depens(
                        dossier_id=dossier.id,
                        date_depens=datetime.now().date(),
                        type_depens="frais de dossier",
                        description="Frais de constitution du dossier",
                        montant=50.00
                    )
                ]
                for depens in depens_list:
                    db.session.add(depens)
                print("✓ Dépens de test créés")
        
        db.session.commit()
        
        print("\n✅ Base de données initialisée avec succès!")
        print(f"   - Clients: {Client.query.count()}")
        print(f"   - Dossiers: {Dossier.query.count()}")
        print(f"   - Frais: {Frais.query.count()}")
        print(f"   - Dépens: {Depens.query.count()}")

if __name__ == '__main__':
    init_database()