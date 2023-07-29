Trade Like King

Version Alpha 0.0.1

Disclaimer : Développeur débutant, à vos propres risques

Cette application automatise la gestion de Futures sur la plateforme LN Market (https://lnmarkets.com/en).

Pré-requis:

    Portefeuille bitcoin (lightning network)

        Personnellement, j'utilise Phoenix wallet

    Compte sur LN Market

        Connexion possible avec wallet lightning, aucune autre information demandée (non-KYC) Vous allez avoir besoin des clés API

Cette application tire son information de Trading Views, qui offrent des signaux (STRONG SELL, SELL, BUY, STRONG BUY) en fonction de nombreux critères et selon plusieurs intervalles temporelles. https://www.tradingview.com/symbols/XBTUSD.P/technicals/

De façon très simplifiée, à chaque 45 secondes, l'application

    Récupère les transactions "running"
    Ajoute de la marge si necessaire pour éviter les liquidations
    Ouvre un Futures après 3 signaux consécutifs
    Ferme si ROI 10% après les frais ET signaux contraires

Tous ces critères sont appelés à changer selon les expérimentations.

Si vous voulez supporter mes efforts ou aider à payer les tests en prod :

    bc1qnr4rgh8v0qtuftvykth730jweunsev6p4p4z88

(je vais trouver une meilleure façon qu'une adresse statique soon)
