#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module utilitaire pour les calculs de frais et dépens
"""

class CalculateurFrais:
    """Classe pour calculer les frais horaires"""
    
    @staticmethod
    def calculer_montant(heures, taux_horaire):
        """
        Calcule le montant des frais
        
        Args:
            heures (float): Nombre d'heures de travail
            taux_horaire (float): Taux horaire en euros
            
        Returns:
            float: Montant total des frais
        """
        return round(heures * taux_horaire, 2)
    
    @staticmethod
    def calculer_avec_marge(montant_base, pourcentage_marge):
        """
        Ajoute une marge au montant de base
        
        Args:
            montant_base (float): Montant initial
            pourcentage_marge (float): Pourcentage de marge à ajouter
            
        Returns:
            float: Montant avec marge appliquée
        """
        marge = montant_base * (pourcentage_marge / 100)
        return round(montant_base + marge, 2)
    
    @staticmethod
    def calculer_tva(montant_ht, taux_tva=20):
        """
        Calcule la TVA
        
        Args:
            montant_ht (float): Montant HT
            taux_tva (float): Taux de TVA en pourcentage (défaut 20%)
            
        Returns:
            dict: Dictionnaire avec montant_ht, montant_tva, montant_ttc
        """
        montant_tva = montant_ht * (taux_tva / 100)
        montant_ttc = montant_ht + montant_tva
        
        return {
            'montant_ht': round(montant_ht, 2),
            'montant_tva': round(montant_tva, 2),
            'montant_ttc': round(montant_ttc, 2),
            'taux_tva': taux_tva
        }


class CalculateurFacture:
    """Classe pour calculer les factures complètes"""
    
    @staticmethod
    def calculer_facture(montant_frais, montant_depens, taux_tva=20):
        """
        Calcule une facture complète
        
        Args:
            montant_frais (float): Total des frais horaires
            montant_depens (float): Total des dépens
            taux_tva (float): Taux de TVA (défaut 20%)
            
        Returns:
            dict: Détails de la facture
        """
        sous_total = montant_frais + montant_depens
        montant_tva = sous_total * (taux_tva / 100)
        montant_ttc = sous_total + montant_tva
        
        return {
            'montant_frais': round(montant_frais, 2),
            'montant_depens': round(montant_depens, 2),
            'sous_total': round(sous_total, 2),
            'taux_tva': taux_tva,
            'montant_tva': round(montant_tva, 2),
            'montant_ttc': round(montant_ttc, 2)
        }
    
    @staticmethod
    def appliquer_acompte(montant_ttc, pourcentage_acompte=30):
        """
        Calcule un acompte sur le montant TTC
        
        Args:
            montant_ttc (float): Montant TTC
            pourcentage_acompte (float): Pourcentage d'acompte (défaut 30%)
            
        Returns:
            dict: Montants de l'acompte et du solde
        """
        montant_acompte = montant_ttc * (pourcentage_acompte / 100)
        montant_solde = montant_ttc - montant_acompte
        
        return {
            'montant_ttc': round(montant_ttc, 2),
            'pourcentage_acompte': pourcentage_acompte,
            'montant_acompte': round(montant_acompte, 2),
            'montant_solde': round(montant_solde, 2)
        }
    
    @staticmethod
    def appliquer_remise(montant, pourcentage_remise):
        """
        Applique une remise
        
        Args:
            montant (float): Montant initial
            pourcentage_remise (float): Pourcentage de remise
            
        Returns:
            dict: Montants avant et après remise
        """
        montant_remise = montant * (pourcentage_remise / 100)
        montant_final = montant - montant_remise
        
        return {
            'montant_initial': round(montant, 2),
            'pourcentage_remise': pourcentage_remise,
            'montant_remise': round(montant_remise, 2),
            'montant_final': round(montant_final, 2)
        }


class ValidateurFrais:
    """Classe pour valider les frais et dépens"""
    
    @staticmethod
    def valider_heures(heures):
        """
        Valide que les heures sont correctes
        
        Args:
            heures (float): Nombre d'heures
            
        Returns:
            tuple: (booléen, message d'erreur si applicable)
        """
        try:
            h = float(heures)
            if h <= 0:
                return False, "Le nombre d'heures doit être supérieur à 0"
            if h > 24:
                return False, "Le nombre d'heures ne peut pas dépasser 24 par jour"
            return True, ""
        except ValueError:
            return False, "Le nombre d'heures doit être un nombre"
    
    @staticmethod
    def valider_taux(taux):
        """
        Valide que le taux est correct
        
        Args:
            taux (float): Taux horaire
            
        Returns:
            tuple: (booléen, message d'erreur si applicable)
        """
        try:
            t = float(taux)
            if t <= 0:
                return False, "Le taux horaire doit être supérieur à 0"
            return True, ""
        except ValueError:
            return False, "Le taux horaire doit être un nombre"
    
    @staticmethod
    def valider_montant(montant):
        """
        Valide qu'un montant est correct
        
        Args:
            montant (float): Montant
            
        Returns:
            tuple: (booléen, message d'erreur si applicable)
        """
        try:
            m = float(montant)
            if m < 0:
                return False, "Le montant ne peut pas être négatif"
            return True, ""
        except ValueError:
            return False, "Le montant doit être un nombre"
