Trade Like King

Version Alpha 0.0.1

*Disclaimer : Développeur débutant, à vos propres risques*

Cette application automatise la gestion de Futures sur la plateforme LN Market (https://lnmarkets.com/en).

Pré-requis:

- Portefeuille bitcoin/lightning
    - Pour fournir de la liquidité
    - Personnellement, j'utilise Phoenix wallet

- Compte sur LN Market
    - Connexion possible avec wallet lightning
    - Aucune autre information demandée (non-KYC)
    - Vous allez avoir besoin des clés API

Cette application tire son information de Trading Views,
qui offrent des signaux (STRONG SELL, SELL, BUY, STRONG BUY) en fonction de nombreux critères et selon plusieurs intervalles temporelles.
https://www.tradingview.com/symbols/XBTUSD.P/technicals/

De façon très simplifiée, à chaque n secondes, l'application

- Récupère les signaux de TradingViews
- Récupère les transactions "running"
- Ajoute de la marge si necessaire pour éviter les liquidations
- Ouvre un Futures après x signaux consécutifs
- Ferme si ROI x0% après les frais ET signaux contraires (long = sell, short = buy)

Tous ces critères sont appelés à changer selon les expérimentations.

L'application a maintenant une interface graphique.
On peut démarrer/arrêter l'application mais aussi ajuster les critères mentionnés plus haut.
Un dashboard pour suivre les principaux métriques est en cours - a suivre.

Si vous voulez supporter mes efforts ou aider à payer les tests en prod :

- kingfu@lnmarkets.com
- 1qnr4rgh8v0qtuftvykth730jweunsev6p4p4z88
    - (je vais trouver une meilleure façon qu'une adresse statique soon)
