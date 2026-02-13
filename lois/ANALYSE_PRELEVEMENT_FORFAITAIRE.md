# ANALYSE JURIDIQUE ET TECHNIQUE -- PRELEVEMENT FORFAITAIRE (PF)

## Lois analysees

| Loi | Reference |
|-----|-----------|
| Loi relative aux Procedures Fiscales et Non Fiscales | Loi N°1/22 du 15 novembre 2020 |
| Loi de Finances 2025/2026 modifiee | Loi N°1/98 du 24 decembre 2025 |

---

# TITRE I : ARTICLES DE LA LOI DE FINANCES 2025/2026

---

## Article 77 -- Prelevement forfaitaire acompte sur importations

### Texte de l'article

> Il est opere un prelevement forfaitaire au titre d'acompte d'impot sur les revenus sur toutes les importations destinees a la revente introduites sur le territoire burundais. Le taux du prelevement forfaitaire est fixe a trois pour cent (3%) de la valeur en douane des importations, sauf pour le carburant.

### Resume

Toute marchandise importee au Burundi destinee a la revente est soumise a un prelevement de 3% calcule sur la valeur en douane (CIF). Ce prelevement est un **acompte** sur l'impot annuel sur les revenus (il sera deduit lors de la declaration annuelle). Le carburant est exclu de ce prelevement.

### Traduction technique

| Element | Valeur |
|---------|--------|
| Type | PF_ACOMPTE_IMPORTATION |
| Taux | 3% |
| Base de calcul | Valeur en douane (CIF) |
| Nature | Acompte (deductible de l'IR annuel) |
| Fait generateur | Importation destinee a la revente |
| Exclusion | Carburant |

### Logique conditionnelle

```
SI type_operation = IMPORTATION
ET destination = REVENTE
ET produit != CARBURANT
ALORS montant_pf = valeur_en_douane * 0.03
     nature = ACOMPTE
```

### Parametres API

- `taux_pf_acompte_importation` = 3%
- `base_calcul` = VALEUR_EN_DOUANE
- `produits_exclus` = [CARBURANT]
- `nature_prelevement` = ACOMPTE

---

## Article 78 -- Prelevement forfaitaire sur vehicules importes

### Texte de l'article

> Pour l'importation des vehicules, le prelevement forfaitaire est applique a partir du deuxieme vehicule d'affaires et promenades importe par individu et par an, excepte pour les vehicules en franchise douaniere.
>
> Toutefois, en cas de transfert du vehicule avant l'expiration d'une periode de deux ans, comptee a partir de la date de son importation, ce prelevement forfaitaire devient exigible.

### Resume

Le PF de 3% sur les vehicules de type affaires et promenade ne s'applique qu'a partir du **2eme vehicule** importe par un meme individu dans la meme annee. Le premier vehicule est exempt. Les vehicules en franchise douaniere sont exclus. Si un vehicule importe sans PF (1er vehicule ou franchise) est revendu ou transfere dans un delai de 2 ans apres l'importation, le PF devient retroactivement exigible.

### Traduction technique

| Element | Valeur |
|---------|--------|
| Type | PF_VEHICULE_IMPORTATION |
| Taux | 3% (meme taux Art. 77) |
| Base de calcul | Valeur en douane |
| Seuil d'application | A partir du 2eme vehicule/individu/an |
| Exemption | Vehicules en franchise douaniere |
| Clause retro | Transfert avant 2 ans = PF exigible |

### Logique conditionnelle

```
SI type_bien = VEHICULE_AFFAIRES_PROMENADE
ET nombre_vehicules_importes_annee(contribuable) >= 2
ET franchise_douaniere = NON
ALORS montant_pf = valeur_en_douane * 0.03

-- Clause retroactive
SI vehicule_importe_sans_pf = OUI
ET (date_transfert - date_importation) < 24 mois
ALORS generer_note_imposition(montant_pf)
```

### Parametres API

- `seuil_vehicules_exemptes` = 1
- `periode_comptage_vehicules` = ANNUELLE
- `delai_clause_retro_mois` = 24
- `exemption_franchise_douaniere` = true

---

## Article 78 (suite) -- Prelevement forfaitaire liberatoire sur achats locaux

### Texte de l'article

> Il est opere un prelevement forfaitaire liberatoire d'impot sur les revenus d'affaires sur les operations suivantes :
>
> a) les achats locaux effectues par des contribuables aupres des fabricants des produits suivants :
> - le sucre : 1% du prix de vente ;
> - les boissons alcoolisees et non alcoolisees produites selon les categories suivantes :
>   1° les bieres : 1% du prix ex-usine ;
>   2° les limonades : 0,5% du prix ex-usine ;
>   3° les jus de toute nature : 0,5% du prix ex-usine ;
>   4° les vins : 2% du prix ex-usine ;
>   5° les liqueurs : 20% du prix ex-usine ;
> - l'eau minerale : 1% du prix ex-usine ;
> - la farine : 0,85% du prix ex-usine ;
> - les huiles produites localement : 2% du prix de vente ;
> - les cigarettes achetees aupres des fabricants locaux : 1% du prix de vente ;
> - les tissus : 1% du prix de vente ;
> - les huiles palmistes (noix) : 2% du prix de vente ;
>
> b) les achats locaux des carburants et lubrifiants aupres des importateurs : 0,74% du prix de vente ;
>
> c) l'abattage par les bouchers :
>   1° bovin : quatre mille francs Burundi (4 000 BIF) par tete de bovin ;
>   2° caprides, ovides, porcs : deux mille francs Burundi (2 000 BIF) par tete ;
>
> d) l'achat du cafe parche : 0,9% du prix de vente.
>
> Ce prelevement forfaitaire liberatoire d'impot sur les revenus concerne uniquement les personnes qui s'approvisionnent aupres des fabricants/transformateurs. Ces derniers sont charges de la collecte, de la declaration et du paiement de ce prelevement au tresor public.

### Resume

C'est un impot **liberatoire** (definitif, non deductible de l'IR annuel) applique lors d'achats de produits locaux aupres des fabricants/transformateurs. Contrairement au PF acompte sur importations, celui-ci est definitif. Le fabricant/transformateur est le **collecteur** : c'est lui qui retient le PF lors de la vente, le declare et le reverse au Tresor public.

### Tableau des taux

| Categorie | Produit | Taux / Montant | Base de calcul |
|-----------|---------|---------------|----------------|
| a) Achats locaux | Sucre | 1% | Prix de vente |
| a) Boissons | Bieres | 1% | Prix ex-usine |
| a) Boissons | Limonades | 0,5% | Prix ex-usine |
| a) Boissons | Jus de toute nature | 0,5% | Prix ex-usine |
| a) Boissons | Vins | 2% | Prix ex-usine |
| a) Boissons | Liqueurs | 20% | Prix ex-usine |
| a) Boissons | Eau minerale | 1% | Prix ex-usine |
| a) Alimentaire | Farine | 0,85% | Prix ex-usine |
| a) Alimentaire | Huiles produites localement | 2% | Prix de vente |
| a) Tabac | Cigarettes (fabricants locaux) | 1% | Prix de vente |
| a) Textile | Tissus | 1% | Prix de vente |
| a) Alimentaire | Huiles palmistes (noix) | 2% | Prix de vente |
| b) Carburants | Carburants et lubrifiants | 0,74% | Prix de vente |
| c) Abattage | Bovin | 4 000 BIF | Par tete |
| c) Abattage | Caprides, ovides, porcs | 2 000 BIF | Par tete |
| d) Cafe | Cafe parche | 0,9% | Prix de vente |

### Logique conditionnelle

```
SI type_operation = ACHAT_LOCAL
ET fournisseur.type IN (FABRICANT, TRANSFORMATEUR)
ALORS
  config = rechercher_config_taux(code_produit)

  SI config.type_taux = POURCENTAGE
    montant_pf = base_selon_config * config.taux
  SINON SI config.type_taux = MONTANT_FIXE
    montant_pf = quantite * config.montant_fixe

  responsable_collecte = FABRICANT/TRANSFORMATEUR
  nature = LIBERATOIRE
```

### Parametres API

```
Table: config_pf_liberatoire_achats_locaux
  - id
  - code_produit
  - libelle_produit
  - categorie (ACHAT_LOCAL, CARBURANT, ABATTAGE, CAFE)
  - taux_pourcentage (nullable)
  - montant_fixe_bif (nullable)
  - base_calcul (PRIX_VENTE, PRIX_EX_USINE, PAR_UNITE)
  - unite (null, TETE_BOVIN, TETE_PETIT_BETAIL)
  - actif (boolean)
  - date_debut_validite
  - date_fin_validite
```

---

## Article 78 (dernier alinea) -- Obligation declarative du PF

### Texte de l'article

> Toute personne qui opere le prelevement conformement a la presente loi, est tenue de remplir une declaration fiscale sous la forme prescrite par le Commissaire General de l'Office Burundais des Recettes et de transferer le montant collecte dans les quinze (15) jours calendaires qui suivent le mois du prelevement.
>
> Toute personne obligee de prelever et qui se soustrait a cette obligation, est tenue personnellement de payer a l'Administration fiscale le montant de l'impot du, amendes et interets de retard compris. Elle peut recuperer l'impot paye aupres du redevable de l'impot, a l'exclusion des amendes et interets.

### Resume

Le collecteur du PF (fabricant, operateur, etc.) doit :
1. Remplir une declaration fiscale prescrite par l'OBR
2. Transferer le montant collecte dans les **15 jours calendaires** apres la fin du mois de prelevement

Si le collecteur ne preleve pas ou ne reverse pas, il devient **personnellement responsable** du montant de l'impot, amendes et interets inclus. Il pourra ensuite se retourner contre le redevable pour l'impot (mais pas pour les amendes).

### Traduction technique

| Element | Valeur |
|---------|--------|
| Delai declaration | 15 jours calendaires apres le mois du prelevement |
| Periodicite | Mensuelle |
| Responsabilite en cas de defaut | Personnelle (collecteur) |
| Recuperable sur redevable | Oui (impot seulement, pas amendes/interets) |

### Logique conditionnelle

```
date_limite = dernier_jour_mois_prelevement + 15 jours calendaires

SI date_depot > date_limite
ALORS appliquer_penalites(Art.130, Art.131, Art.126)

SI collecteur.n_a_pas_preleve = OUI
ALORS collecteur.responsabilite_personnelle = OUI
     montant_du = impot + amendes + interets
```

### Parametres API

- `delai_declaration_pf_jours` = 15
- `type_delai` = JOURS_CALENDAIRES
- `reference_base` = FIN_MOIS_PRELEVEMENT

---

## Article 83 -- Declaration des revenus locatifs

### Texte de l'article

> Par derogation a l'article 85 de la loi n°1/14 du 24 decembre 2020 portant modification de la loi n°1/02 du 24 janvier 2013 relative aux impots sur les revenus, toute personne physique et morale percevant un revenu locatif imposable doit preparer une declaration annuelle sous la forme specifiee par le Commissaire General de l'Office Burundais des Recettes et la soumettre a l'Administration fiscale au plus tard le 31 mars de l'annee qui suit celle de l'encaissement des loyers.
>
> Cette declaration doit etre unique pour les revenus locatifs encaisses sur tout le territoire.

### Resume

Toute personne percevant des loyers doit deposer une **declaration annuelle unique** couvrant tous les revenus locatifs sur le territoire, au plus tard le **31 mars** de l'annee suivante.

### Parametres API

- `date_limite_declaration_locatif` = 31 mars N+1
- `periodicite` = ANNUELLE
- `type_declaration` = UNIQUE_TERRITOIRE

---

## Article 84/85 -- Dividendes et penalites de retard

### Texte de l'article

> Au titre de la gestion budgetaire 2025/2026, les benefices nets d'impot realises par les societes a participation publique, les etablissements publics a caractere commercial ou industriel sont repartis dans un delai de trente (30) jours calendaires, comptes a partir de la date limite de declaration de l'impot sur les revenus.
>
> Les dividendes revenant a l'Etat sont verses sur les comptes de transit des recettes non fiscales de l'Office Burundais des Recettes au plus tard le quinzieme jour qui suit le mois de repartition.
>
> En cas de non-respect de l'alinea precedent, les dividendes sont majores d'une penalite de 5% par mois de retard.

### Resume

Les societes publiques ou a participation publique doivent repartir leurs benefices dans les 30 jours apres la date limite de declaration IR. Les dividendes de l'Etat doivent etre verses au plus tard le 15eme jour du mois suivant la repartition. En cas de retard : **penalite de 5% par mois**.

### Traduction technique

| Element | Valeur |
|---------|--------|
| Delai repartition benefices | 30 jours calendaires apres date limite declaration IR |
| Delai versement dividendes Etat | 15eme jour du mois suivant |
| Penalite retard | 5% par mois de retard |

### Parametres API

- `delai_repartition_benefices_jours` = 30
- `delai_versement_dividendes_etat` = 15eme jour mois suivant
- `taux_penalite_retard_dividendes` = 5% par mois

---

## Article 109 -- Redevance environnementale forfaitaire

### Texte de l'article

> Au titre de la gestion budgetaire 2025/2026, il est institue une redevance annuelle environnementale forfaitaire fixee comme suit :
>
> Pour les motocyclettes, tricycles et quadricycles :
> 1° les motocyclettes : 10 000 BIF ;
> 2° les tricycles et quadricycles a moteurs : 20 000 BIF ;
>
> Pour les vehicules et autres engins d'un poids :
> 1° inferieur ou egal a 1 400 kg : 50 000 BIF ;
> 2° de 1 401 kg a 2 500 kg : 100 000 BIF ;
> 3° de 2 501 kg a 3 500 kg : 500 000 BIF ;
> 4° de 3 501 kg a 9 000 kg : 1 000 000 BIF ;
> 5° de 9 001 kg et plus : 1 500 000 BIF.
>
> Cette redevance est payable au plus tard le 31 mars de chaque annee.
>
> Le retard de payement de cette redevance est passible d'une amende de cinquante pour cent (50%) majoree de un pour cent (1%) par mois de retard.

### Resume

Redevance annuelle obligatoire pour tous les vehicules et motos. Montant fixe selon la categorie et le poids du vehicule. Payable avant le 31 mars. En cas de retard : amende de 50% + 1% par mois supplementaire.

### Tableau des montants

| Type de vehicule / Poids | Montant annuel (BIF) |
|---------------------------|---------------------|
| Motocyclettes | 10 000 |
| Tricycles et quadricycles | 20 000 |
| Vehicules <= 1 400 kg | 50 000 |
| Vehicules 1 401 - 2 500 kg | 100 000 |
| Vehicules 2 501 - 3 500 kg | 500 000 |
| Vehicules 3 501 - 9 000 kg | 1 000 000 |
| Vehicules >= 9 001 kg | 1 500 000 |

### Exemptions (Art. 110/111)

- Vehicules de l'Etat
- Missions diplomatiques et consulaires
- Organismes internationaux ayant convention avec le Burundi
- ONG ayant convention avec le Burundi
- Vehicules electriques
- Transport en commun > 12 places : forfait de 100 000 BIF

### Parametres API

- `date_limite_paiement` = 31 mars
- `taux_amende_retard_initial` = 50%
- `taux_amende_retard_mensuel` = 1% par mois

---

## Article 111 (suite) -- Impot forfaitaire liberatoire sur transport remunere

### Texte de l'article

> Il est opere un impot forfaitaire liberatoire trimestriel sur le transport remunere. L'impot est fixe comme suit :
> 1° camion :
>   a) de moins de 7 tonnes : 39 000 BIF ;
>   b) de 7 a 10 tonnes : 54 000 BIF ;
>   c) de plus de 10 tonnes : 200 000 BIF ;
> 2° bus de plus de 35 places : 54 000 BIF ;
> 3° bus de 18 a 35 places : 39 000 BIF ;
> 4° bus de 12 a 18 places : 24 000 BIF ;
> 5° taxi voiture : 20 000 BIF ;
> 6° tricyclomoteur : 15 000 BIF ;
> 7° taxi moto : 15 000 BIF.
>
> Les contribuables tenus par les lois fiscales de faire une comptabilite complete ne sont pas concernes par cet article.

### Resume

Impot forfaitaire trimestriel pour les transporteurs. Montant fixe selon le type de vehicule. C'est un impot **liberatoire** (definitif). Les contribuables ayant une comptabilite complete sont **exclus** de ce regime (ils paient l'IR normal).

### Tableau des montants

| Type de vehicule | Montant trimestriel (BIF) |
|------------------|--------------------------|
| Camion < 7 tonnes | 39 000 |
| Camion 7 - 10 tonnes | 54 000 |
| Camion > 10 tonnes | 200 000 |
| Bus > 35 places | 54 000 |
| Bus 18 - 35 places | 39 000 |
| Bus 12 - 18 places | 24 000 |
| Taxi voiture | 20 000 |
| Tricyclomoteur | 15 000 |
| Taxi moto | 15 000 |

### Logique conditionnelle

```
SI contribuable.comptabilite_complete = OUI
ALORS non_assujetti (regime IR normal)

SINON
  montant = rechercher_montant(type_vehicule, capacite)
  periodicite = TRIMESTRIEL
  nature = LIBERATOIRE
```

---

## Article 137 -- Amende retard renouvellement carte entree vehicules

### Texte de l'article

> Il est opere une amende pour retard de renouvellement de la carte d'entree de vehicules. Le montant de l'amende est fixe a une somme equivalente a trente dollars americains (30 USD) par mois de retard.

### Parametres API

- `amende_retard_carte_vehicule` = 30 USD/mois

---

## Article 138 -- Impot sur la fortune

### Texte de l'article

> Il est applique un impot sur la fortune sur les operations suivantes :
>
> a) cinq pour cent (5%) de la valeur en douane sur les vehicules importes de type affaires et promenade a grosse cylindree de 3 500 cc et plus, a l'exception de ceux importes par des personnes physiques ou morales beneficiant de l'exoneration. A partir de l'importation du 2eme vehicule de meme type, l'impot sur la fortune passe du taux de 5% au double, au triple, ainsi de suite ;
>
> b) cinq pour cent (5%) de la valeur hors TVA d'un immeuble ou d'une fraction d'immeuble, bati ou non bati, dont la valeur marchande ou celle de contre-expertise, selon la valeur la plus elevee, est egale ou superieure a 500 000 000 BIF ;
>
> c) cinq pour cent (5%) de la valeur hors TVA a partir du troisieme immeuble ou d'une fraction d'immeuble, bati ou non bati. Si le troisieme immeuble atteint la valeur de 500 000 000 BIF, un taux de 10% est applicable.
>
> Cet impot est supporte par l'acquereur.

### Traduction technique

| Operation | Taux | Condition |
|-----------|------|-----------|
| Vehicule >= 3 500 cc (1er) | 5% de la valeur en douane | Sauf exoneres |
| Vehicule >= 3 500 cc (2eme) | 10% (double) | Meme type |
| Vehicule >= 3 500 cc (3eme) | 15% (triple) | Et ainsi de suite |
| Immeuble >= 500M BIF | 5% valeur hors TVA | Valeur marchande ou contre-expertise |
| 3eme immeuble | 5% | Valeur < 500M BIF |
| 3eme immeuble >= 500M BIF | 10% | Valeur >= 500M BIF |

---

## Article 146 -- Calcul et paiement de l'impot sur le revenu

### Texte de l'article

> Le montant de l'impot sur le revenu exigible est calcule sur base de la declaration annuelle et diminue ensuite :
> 1. des retenues operees conformement aux articles 119 et 120 ;
> 2. des acomptes trimestriels provisionnels effectues durant l'exercice fiscal ;
> 3. du credit d'impot pour l'impot paye a l'etranger ;
> 4. de l'impot paye au titre de la vente de tout actif servant a realiser les activites d'affaires ;
> 5. de toute autre retenue qui represente un acompte de l'impot sur le revenu.
>
> L'impot du est declare et paye a l'Administration fiscale au plus tard a la date limite de depot de la declaration, qui est pour l'application de la presente loi, le quinzieme jour du mois suivant celui de la realisation du revenu, pour les declarations mensuelles, et au plus tard le dernier jour du troisieme mois apres la cloture de l'exercice comptable pour les declarations annuelles.

### Resume

L'impot annuel est calcule puis diminue de tous les acomptes et retenues deja payes (dont le PF acompte importation Art. 77). C'est ici que le PF acompte est deduit. Delais : le 15 du mois suivant (mensuel) ou le dernier jour du 3eme mois apres cloture (annuel).

### Traduction technique

```
impot_net = impot_brut_calcule
           - retenues_source (Art. 119, 120)
           - acomptes_trimestriels
           - credit_impot_etranger
           - impot_vente_actifs
           - PF_ACOMPTE_IMPORTATION (Art. 77)
           - autres_retenues_acompte

date_limite_mensuelle = 15eme jour du mois suivant
date_limite_annuelle = dernier jour du 3eme mois apres cloture
```

---

## Article 148 -- Retenue a la source de 15%

### Texte de l'article

> Une retenue de quinze pour cent (15%) est pratiquee sur les paiements ci-apres effectues par les personnes residentes y compris les personnes exonerees d'impot :
> 1° les dividendes ou participations aux benefices verses par une societe residente a une autre societe residente, aux actionnaires ou aux employes ;
> [...]

### Resume

Retenue a la source de 15% sur les dividendes et autres paiements similaires. Les personnes exonerees d'impot doivent quand meme pratiquer cette retenue.

### Parametres API

- `taux_retenue_source_dividendes` = 15%

---

## Article 150 -- PF liberatoire par declaration douaniere

### Texte de l'article

> Au titre de la gestion budgetaire 2025/2026, il est opere un prelevement forfaitaire liberatoire d'impot sur le revenu, d'un montant de cinquante mille francs Burundi (50 000 BIF), par declaration douaniere. Ce prelevement est de dix mille francs Burundi (10 000 BIF) par declaration simplifiee.
>
> Toutefois, les revenus issus des autres activites ne sont pas soumis a ce prelevement, ils sont declares conformement aux lois en vigueur.

### Resume

Montant fixe preleve a chaque declaration douaniere. C'est un impot **liberatoire** uniquement pour les revenus lies a l'activite douaniere. 50 000 BIF pour une declaration standard, 10 000 BIF pour une declaration simplifiee.

### Traduction technique

| Type de declaration | Montant PF (BIF) |
|---------------------|-----------------|
| Declaration douaniere standard | 50 000 |
| Declaration simplifiee | 10 000 |

### Logique conditionnelle

```
SI type_document = DECLARATION_DOUANIERE_STANDARD
ALORS montant_pf = 50 000 BIF

SI type_document = DECLARATION_SIMPLIFIEE
ALORS montant_pf = 10 000 BIF

nature = LIBERATOIRE
champ = REVENUS_ACTIVITE_DOUANIERE_UNIQUEMENT
```

### Parametres API

- `montant_pf_declaration_standard` = 50 000
- `montant_pf_declaration_simplifiee` = 10 000
- `exercice_applicable` = 2025/2026

---

## Article 151 -- PF liberatoire sur transfert d'argent mobile

### Texte de l'article

> Il est applique un prelevement forfaitaire liberatoire d'impot sur les revenus realises par les intermediaires dans les operations de transfert d'argent mobile. Ce prelevement qui est fixe a un pour cent (1%) de la commission percue par l'intermediaire, est opere, declare et reverse par l'operateur dans les memes conditions que les autres prelevements forfaitaires liberatoires d'impot sur les revenus.

### Resume

Les intermediaires du mobile money (agents, points de service) paient un PF de **1% de leur commission**. C'est l'**operateur** (Lumicash, Ecocash, etc.) qui est responsable de la collecte, de la declaration et du reversement. Nature liberatoire.

### Traduction technique

| Element | Valeur |
|---------|--------|
| Type | PF_LIBERATOIRE_MOBILE_MONEY |
| Taux | 1% |
| Base de calcul | Commission percue par l'intermediaire |
| Collecteur/Declarant | Operateur (pas l'intermediaire) |
| Nature | Liberatoire |
| Conditions declaration | Identiques aux autres PF liberatoires (15 jours) |

### Logique conditionnelle

```
SI type_operation = TRANSFERT_ARGENT_MOBILE
ET acteur = INTERMEDIAIRE
ALORS montant_pf = commission_intermediaire * 0.01
     collecteur = OPERATEUR_TELECOM
     nature = LIBERATOIRE
     delai_declaration = 15 jours calendaires apres fin du mois
```

### Parametres API

- `taux_pf_mobile_money` = 1%
- `base_calcul` = COMMISSION_INTERMEDIAIRE
- `collecteur` = OPERATEUR

---

## Article 152 -- Contribution forfaitaire transport international routier

### Texte de l'article

> Pour le transport international routier, une contribution speciale forfaitaire annuelle, collectee par l'Office Burundais des Recettes, est adoptee.
>
> Le montant de la contribution forfaitaire annuelle est fixe comme suit :
> - agence de transport international routier des personnes par vehicules de moins de 30 places assises, enregistree au Burundi : 100 000 BIF ;
> - agence de transport international routier des personnes par vehicules de plus de 30 places assises, enregistree au Burundi : 200 000 BIF ;
> - agence de transport international routier des personnes par vehicules de moins de 30 places assises, enregistree a l'etranger : 60 USD ;
> - agence de transport international routier de personnes par vehicules de plus de 30 places assises, enregistree a l'etranger : 150 USD ;
> - agence de transport international routier des vehicules importes de l'etranger : 400 000 BIF ;
> - agence de transport international routier des marchandises par des poids lourds, enregistree au Burundi : 800 000 BIF ;
> - agence de transport des vehicules importes de l'etranger : 2 000 000 BIF.
>
> La date limite de paiement de cette contribution speciale forfaitaire est fixee au 31 mars de l'annee avec une amende de cinquante pour cent (50%) pour les retardataires.

### Tableau des montants

| Type d'agence | Lieu enregistrement | Montant annuel |
|--------------|---------------------|---------------|
| Transport personnes < 30 places | Burundi | 100 000 BIF |
| Transport personnes > 30 places | Burundi | 200 000 BIF |
| Transport personnes < 30 places | Etranger | 60 USD |
| Transport personnes > 30 places | Etranger | 150 USD |
| Transport vehicules importes | Etranger | 400 000 BIF |
| Transport marchandises poids lourds | Burundi | 800 000 BIF |
| Transport vehicules importes | -- | 2 000 000 BIF |

### Parametres API

- `date_limite_paiement` = 31 mars
- `taux_amende_retard` = 50%
- `periodicite` = ANNUELLE

---

## Article 153 -- PF sur services de convoi de vehicules importes

### Texte de l'article

> Il est opere un prelevement forfaitaire de cinq pour cent (5%) sur la remuneration des services de convoi des vehicules importes applicable sur le fret interieur.

### Resume

Un PF de 5% est preleve sur la remuneration des convoyeurs de vehicules importes, pour le trajet interieur (du poste frontiere a la destination finale).

### Parametres API

- `taux_pf_convoi_vehicules` = 5%
- `base_calcul` = REMUNERATION_SERVICE_CONVOI
- `perimetre` = FRET_INTERIEUR

---

## Article 158 -- Prelevement sur plateformes numeriques

### Texte de l'article

> Au titre de la gestion budgetaire 2025/2026, il est institue un prelevement de 10% sur les revenus de source burundaise realises par les plateformes de diffusion des contenus numeriques de type streaming, de services VOIP ou de commerce electronique, par la mise a disposition des contenus, des produits ou des services accessibles aux utilisateurs se trouvant au Burundi.
>
> Les createurs des contenus numeriques etablis au Burundi percevant des revenus issus de la monetisation de leurs contenus par des audiences internationales ou nationales, sont soumis a la legislation fiscale en vigueur au Burundi.

### Resume

Les plateformes type Netflix, YouTube, services VOIP, e-commerce qui generent des revenus au Burundi paient 10% de ces revenus. Les createurs de contenu burundais sont soumis au regime fiscal normal (pas ce prelevement specifique).

### Parametres API

- `taux_prelevement_numerique` = 10%
- `types_plateformes` = [STREAMING, VOIP, E_COMMERCE]
- `base_calcul` = REVENUS_SOURCE_BURUNDAISE

---

## Article 164 a 175 -- Taxe sur les Activites Financieres (TAF)

### Articles cles

**Article 164** : La TAF frappe les operations bancaires, financieres et le commerce de valeurs/argent.

**Article 165** : Assiette = produit net bancaire ou financier.

**Article 167** : Taux = **8%** de l'assiette.

**Article 169** :
> La TAF est declaree et payee mensuellement. La declaration et le paiement mensuels doivent etre faits aupres du service competent de l'Administration fiscale au plus tard le quinzieme jour du mois qui suit la periode imposable.

**Article 170** : Sanctions = celles prevues par la loi sur les procedures fiscales.

**Article 175** : La TAF n'est **pas deductible** du resultat imposable a l'IR.

### Parametres API

- `taux_taf` = 8%
- `base_calcul` = PRODUIT_NET_BANCAIRE
- `date_limite_declaration` = 15eme jour du mois suivant
- `periodicite` = MENSUELLE
- `deductible_ir` = NON

---

## Article 176 -- Prelevement sur services financiers mobiles

### Texte de l'article

> Il est opere un prelevement specifique de 22% applique sur les frais des services financiers mobiles. Ce prelevement est supporte par les fournisseurs des services financiers mobiles qui sont les proprietaires des plateformes.

### Resume

Prelevement de **22%** sur les **frais** (et non les commissions) des services financiers mobiles. Supporte par le fournisseur de la plateforme (pas l'utilisateur).

**Distinction avec Art. 151** : L'Art. 151 (1% sur commissions intermediaires) et l'Art. 176 (22% sur frais plateformes) ont des perimetres differents. L'Art. 151 concerne les commissions des agents intermediaires ; l'Art. 176 concerne les frais que la plateforme elle-meme applique.

### Parametres API

- `taux_prelevement_sfm` = 22%
- `base_calcul` = FRAIS_SERVICES_FINANCIERS_MOBILES
- `redevable` = FOURNISSEUR_PLATEFORME

---

## Article 180 -- Regime forfaitaire des micro-contribuables

### Texte de l'article

> Au titre de la gestion budgetaire 2025/2026, par derogation de l'article 41 de loi n°1/14 du 24 decembre 2020 portant modification de la loi n°1/02 du 24 janvier 2013 relative aux impots sur les revenus, les personnes physiques qui realisent un chiffre d'affaires annuel inferieur ou egal a vingt-cinq millions de francs Burundi (25 000 000 BIF) sont tenues de souscrire a la declaration trimestrielle. Le taux d'imposition est fixe au taux unique de 1% du chiffre d'affaires trimestriel.
>
> Les personnes physiques qui realisent, au cours d'un exercice fiscal, un chiffre d'affaires de plus de 25 000 000 BIF doivent deposer une declaration annuelle de l'impot sur les revenus et le contribuable est directement oblige de tenir une comptabilite simplifiee ou complete selon le cas.

### Resume

Les personnes physiques avec un CA annuel <= 25M BIF paient un forfait de **1% du CA trimestriel**. Au-dela de 25M BIF, passage obligatoire au regime reel avec comptabilite et declaration annuelle.

### Logique conditionnelle

```
SI contribuable.type = PERSONNE_PHYSIQUE
ET chiffre_affaires_annuel <= 25 000 000 BIF
ALORS
  regime = FORFAITAIRE_MICRO
  taux = 1%
  base = CA_TRIMESTRIEL
  periodicite = TRIMESTRIEL

SINON
  regime = REEL
  obligation = COMPTABILITE_SIMPLIFIEE ou COMPLETE
  periodicite_declaration = ANNUELLE
```

### Parametres API

- `seuil_ca_micro_contribuable` = 25 000 000 BIF
- `taux_forfaitaire_micro` = 1%
- `periodicite_micro` = TRIMESTRIEL

---

## Article 183 -- Amende forfaitaire bris de scelles douaniers

### Texte de l'article

> Au titre de la gestion budgetaire 2025/2026, sans prejudice des penalites prevues dans la loi sur la gestion des douanes de la Communaute Est Africaine, il est institue une amende administrative forfaitaire de cinquante millions de francs Burundi (50 000 000 BIF) par conteneur suivant le moyen de transport par vehicule, pour les marchandises en vrac, camion-citerne selon le cas, pour tout importateur qui echappe au controle douanier en brisant les scelles sans autorisation prealable d'un agent des douanes competent.

### Parametres API

- `amende_bris_scelles` = 50 000 000 BIF
- `unite` = PAR_CONTENEUR ou PAR_VEHICULE

---

## Article 191 -- Prime de denonciation fraude fiscale

### Texte de l'article

> Au titre de la gestion budgetaire 2025/2026, il est accorde une prime a toute personne qui revele une fraude fiscale ou douaniere. La prime est fixee a 10% des montants en principal etablis au titre des impots, taxes, droits ou redevances encaissees.

### Parametres API

- `taux_prime_denonciation` = 10%
- `base` = MONTANT_PRINCIPAL_ENCAISSE

---

# TITRE II : ARTICLES DE LA LOI RELATIVE AUX PROCEDURES FISCALES ET NON FISCALES (2020)

---

## Article 31 -- Conservation des documents de prelevement

### Texte de l'article

> Tout contribuable doit preparer, etablir et conserver tous les livres et documents relatifs :
> 1° a une dette fiscale ;
> 2° au prelevement et a la declaration des retenues a la source et autres avances decomptees sur l'impot ;
> 3° a la declaration d'impot.

## Article 32 -- Duree de conservation

### Texte de l'article

> Tous les livres et documents vises aux articles 29, 30 et 31 de la presente loi doivent etre conserves pour une duree de dix ans a compter de la date de cloture de l'exercice fiscal qu'ils concernent dans les locaux du contribuable ou de son representant situes au Burundi.

### Parametres API

- `duree_conservation_documents_ans` = 10

---

## Article 50 -- Declaration des mutations immobilieres

### Texte de l'article

> Sans prejudice des dispositions pertinentes du Code civil, toute mutation immobiliere ou de valeur mobiliere de placement ainsi que des vehicules doit obligatoirement etre authentifiee par un notaire.
>
> Les actes translatifs de droits reels authentifies doivent etre communiques au Commissaire general dans un delai de quinze (15) jours calendaires du mois suivant celui de leur authentification.
>
> A defaut de la declaration dans les delais ci-haut specifies, une amende de cinq pour cent (5%) de la valeur transactionnelle est appliquee, majoree de un pour cent (1%) par mois de retard sans toutefois depasser vingt-quatre (24) mensualites.

### Parametres API

- `delai_declaration_mutation` = 15 jours calendaires
- `amende_defaut_declaration_mutation` = 5% valeur transactionnelle
- `majoration_mensuelle` = 1% par mois
- `plafond_majorations` = 24 mois

---

## Article 56 -- Delais de prescription pour rectification

### Texte de l'article

> Pour les declarations deposees dans le delai legal, la rectification peut etre operee pendant une periode de trois (3) ans a compter de la date de depot de la declaration.
>
> Pour les declarations tardives, la rectification peut etre operee pendant une periode de trois ans a compter de la date limite de depot de la declaration.

### Parametres API

- `delai_prescription_rectification_ans` = 3

---

## Article 67 -- Delai de paiement apres note d'imposition

### Texte de l'article

> Le contribuable est oblige de payer l'impot du dans un delai de trente (30) jours calendaires a partir de la reception de la note d'imposition. L'enrolement des impositions intervient le vingt et unieme jour de la reception de la note d'imposition sauf en cas de recours.
>
> Si, apres un controle general, il se degage un solde crediteur sur le compte courant du contribuable, ce surplus est pris en compte pour le paiement des obligations fiscales futures a moins que le contribuable n'en demande le remboursement. Dans ce cas, l'Administration fiscale est obligee de restituer le surplus au contribuable dans un delai de quatre-vingt-dix (90) jours calendaires.

### Parametres API

- `delai_paiement_note_imposition_jours` = 30
- `jour_enrolement` = 21eme jour
- `delai_remboursement_surplus_jours` = 90

---

## Article 98 -- Lettre de rappel

### Texte de l'article

> Lorsque les recettes ne sont pas payees dans les delais prescrits, l'Administration fiscale adresse au contribuable une lettre de rappel indiquant le montant de recettes dues, des interets et des amendes a payer ainsi que les poursuites legales qui seront intentees au cas ou l'impot, les interets et les amendes ne seraient pas payes dans le delai de quinze (15) jours calendaires a compter de la reception de la lettre de rappel.

### Parametres API

- `delai_reponse_lettre_rappel_jours` = 15

---

## Article 99 -- Prescription du recouvrement

### Texte de l'article

> Il y a prescription pour le recouvrement des recettes apres une periode de dix (10) ans a compter de la date d'exigibilite.

### Parametres API

- `delai_prescription_recouvrement_ans` = 10

---

## Article 126 -- Interets moratoires (retard de paiement)

### Texte de l'article

> Lorsque le contribuable ne paye pas l'impot dans le delai legal, il est tenu de payer des interets de retard sur le montant de l'impot en principal. Le taux d'interet est determine par ordonnance du Ministre au 1er jour de chaque annee fiscale et est majore de 1,5 point. Si aucun taux n'est adopte, le taux de l'annee precedente est reconduit tacitement.
>
> Les interets de retard sont calcules mensuellement et non composes, a compter du premier jour qui suit la date a laquelle l'impot aurait du etre paye jusqu'au jour du paiement inclus. Chaque mois commence compte pour un mois complet.

### Resume

En cas de retard de paiement, le contribuable doit payer des interets calcules **mensuellement** et **non composes**. Le taux est fixe par ordonnance ministerielle + 1,5 point. Tout mois commence = mois complet.

### Traduction technique

```
taux_mensuel = (taux_ordonnance + 1.5) / 12
nombre_mois = arrondir_superieur(jours_retard / 30)  -- mois commence = complet
interets = montant_principal * taux_mensuel * nombre_mois
-- PAS de composition (interets sur interets)
```

### Parametres API

- `taux_base_interet` = fixe par ordonnance ministerielle
- `majoration_taux` = 1.5 points
- `calcul` = MENSUEL_NON_COMPOSE
- `regle_mois` = MOIS_COMMENCE_COMPTE_COMPLET

---

## Article 127 -- Ordre d'imputation des paiements

### Texte de l'article

> Lorsque le contribuable effectue un paiement, celui-ci est affecte successivement au recouvrement des interets, des amendes et de la dette fiscale.

### Resume

**REGLE CRITIQUE** : tout paiement est impute dans cet ordre strict :
1. **Interets** (en premier)
2. **Amendes** (en deuxieme)
3. **Principal / dette fiscale** (en dernier)

### Logique conditionnelle

```
paiement = montant_recu

-- Etape 1 : imputer aux interets
montant_impute_interets = MIN(paiement, total_interets_dus)
paiement = paiement - montant_impute_interets

-- Etape 2 : imputer aux amendes
montant_impute_amendes = MIN(paiement, total_amendes_dues)
paiement = paiement - montant_impute_amendes

-- Etape 3 : imputer au principal
montant_impute_principal = MIN(paiement, dette_fiscale_principale)
paiement = paiement - montant_impute_principal

-- Eventuel surplus = trop-percu
```

---

## Article 128 -- Interets moratoires de l'Administration

### Texte de l'article

> Lorsque l'Administration fiscale ne rembourse pas le trop verse dans le delai legal, il est tenu de payer des interets de retard sur le montant concerne. Le taux d'interet est determine par ordonnance du Ministre au 1er jour de chaque exercice fiscal.

### Resume

Si l'Administration fiscale tarde a rembourser un trop-percu, elle doit aussi payer des interets de retard au contribuable.

---

## Article 129 -- Liste des infractions fiscales

### Texte de l'article

> Un contribuable ou toute personne commet une infraction fiscale lorsque :
> 1° il ne depose pas de declaration d'impot ou les justificatifs y afferents dans le delai legal ;
> 2° il ne depose pas de declaration d'impot retenu a la source dans le delai legal ou ne preleve pas la retenue a la source bien qu'il y soit tenu ;
> 3° il ne repond pas a une demande de renseignements de l'Administration fiscale ;
> 4° il ne coopere pas a un controle fiscal ;
> 5° il ne communique pas dans les delais, sa nouvelle fonction ou designation ;
> 6° il ne s'immatricule pas conformement aux dispositions ;
> 7° il contrevient aux articles 28 a 32 (tenue des documents) ;
> 8° il ne paye pas dans le delai imparti les acomptes trimestriels provisionnels ;
> 9° il ne satisfait pas aux obligations prescrites par les lois fiscales ;
> 10° il effectue une livraison de biens ou une prestation de services sans delivrer une facture conforme.

---

## Article 130 -- Amendes fixes pour infractions

### Texte de l'article

> Lorsque l'une des infractions visees a l'article 129 de la presente loi, point 1° a 9° concerne l'exercice d'une activite d'affaires, l'amende est fixee comme suit :
> 1° cent mille (100 000) francs burundais si le contribuable est classe parmi les petits ou micro contribuables ;
> 2° trois cent mille (300 000) francs burundais si le contribuable est classe parmi les moyens contribuables ;
> 3° six cent mille (600 000) francs burundais si le contribuable est classe parmi les grands contribuables.
>
> Pour les contribuables qui ne realisent pas d'activites d'affaires, l'amende est fixee a cent mille (100 000) francs burundais.
>
> Lorsque l'infraction prevue par l'article 129, point 10° (non-facturation) est commise, l'amende est fixee a vingt pour cent (20%) de la valeur des biens livres ou des services prestes.

### Tableau des amendes

| Categorie contribuable | Amende (BIF) |
|------------------------|-------------|
| Petit / Micro contribuable | 100 000 |
| Moyen contribuable | 300 000 |
| Grand contribuable | 600 000 |
| Non-affaires | 100 000 |
| Non-facturation (Art. 129-10°) | 20% de la valeur |

---

## Article 131 -- Penalite pour paiement tardif

### Texte de l'article

> Lorsque le montant de l'impot qui figure dans la declaration d'impot ou dans la note d'imposition n'est pas paye dans le delai legal, le contribuable est passible d'une amende egale a dix pour cent (10%) du montant de l'impot du.
>
> L'amende pour paiement tardif est calculee sur le montant de l'impot du a l'exclusion des interets ou des amendes prevues aux articles 130 a 142 de la presente loi.

### Resume

Si l'impot n'est pas paye a temps : amende de **10%** calculee **uniquement** sur le principal (pas sur les interets ni les autres amendes).

### Logique conditionnelle

```
SI date_paiement > date_limite_legale
ALORS amende_paiement_tardif = montant_impot_principal * 0.10
     -- NE PAS inclure les interets ou autres amendes dans la base
```

### Parametres API

- `taux_penalite_paiement_tardif` = 10%
- `base_calcul` = IMPOT_PRINCIPAL_UNIQUEMENT

---

## Article 132 -- Penalites pour sous-estimation

### Texte de l'article

> Lorsque le controle montre que le montant de l'impot declare est inferieur au montant qui devait etre declare, a moins que la faute de calcul soit imputable a l'Administration fiscale, il est passible d'une des amendes suivantes :
>
> 1° cinq pour cent (5%) du montant de la sous-estimation si celle-ci s'eleve a 5% ou plus, mais sans toutefois atteindre 10% de l'impot qui devait etre declare ;
> 2° dix pour cent (10%) du montant de la sous-estimation si celle-ci s'eleve a 10% ou plus, mais sans toutefois atteindre 20% ;
> 3° vingt pour cent (20%) du montant de la sous-estimation si celle-ci s'eleve a 20% ou plus, mais sans toutefois atteindre 50% ;
> 4° cinquante pour cent (50%) du montant de la sous-estimation si celle-ci s'eleve a 50% ou plus.

### Tableau progressif

| Taux de sous-estimation | Taux de l'amende | Base de l'amende |
|------------------------|-----------------|-----------------|
| >= 5% et < 10% | 5% | Montant de la sous-estimation |
| >= 10% et < 20% | 10% | Montant de la sous-estimation |
| >= 20% et < 50% | 20% | Montant de la sous-estimation |
| >= 50% | 50% | Montant de la sous-estimation |
| < 5% | 0% | Pas d'amende |

### Logique conditionnelle

```
taux_sous_estimation = (impot_du_reel - impot_declare) / impot_du_reel * 100
montant_sous_estime = impot_du_reel - impot_declare

SI taux_sous_estimation < 5%
  amende = 0
SINON SI taux_sous_estimation >= 5% ET < 10%
  amende = montant_sous_estime * 0.05
SINON SI taux_sous_estimation >= 10% ET < 20%
  amende = montant_sous_estime * 0.10
SINON SI taux_sous_estimation >= 20% ET < 50%
  amende = montant_sous_estime * 0.20
SINON SI taux_sous_estimation >= 50%
  amende = montant_sous_estime * 0.50
```

---

## Article 133 -- Penalite pour imposition d'office (absence de declaration)

### Texte de l'article

> En cas d'imposition d'office pour absence de declaration, il est applique des penalites de soixante-quinze pour cent (75%) de l'impot etabli.

### Parametres API

- `taux_penalite_imposition_office` = 75%
- `base_calcul` = IMPOT_ETABLI

---

## Article 134 -- Sanction pour fraude fiscale

### Texte de l'article

> Sans prejudice des dispositions particulieres de la presente loi, toute personne qui s'est frauduleusement soustraite a l'etablissement ou au paiement partiel ou total des impots, soit qu'il ait volontairement omis de faire sa declaration, soit qu'il ait volontairement dissimule une part des sommes sujettes a l'impot, soit qu'il ait organise son insolvabilite, soit en agissant de toute autre maniere frauduleuse, est passible d'une amende administrative egale a cent pour cent (100%) de l'impot elude.

### Parametres API

- `taux_penalite_fraude` = 100%
- `base_calcul` = IMPOT_ELUDE

---

## Article 135 -- Fraude avec complicite d'un comptable agree

### Texte de l'article

> Si la fraude fiscale a ete effectuee par ou avec l'assentiment d'un professionnel agree par l'Ordre des Professions Comptables, ce professionnel encourt une amende egale a cinquante pour cent (50%) de l'impot elude.

### Parametres API

- `taux_penalite_comptable_complice` = 50%

---

## Article 140 -- Recidive

### Texte de l'article

> En cas de recidive dans le delai de cinq (5) ans, les sanctions prevues aux articles 134 et 137 de la presente loi sont doublees.

### Parametres API

- `delai_recidive_ans` = 5
- `multiplicateur_recidive` = 2

---

## Article 141 -- Prime de denonciation

### Texte de l'article

> Une prime de dix pour cent (10%) des montants, en principal, des recettes etablies est accordee a tout individu qui denonce des personnes se livrant a la fraude fiscale [...] a l'exclusion des agents de l'Administration fiscale ou de tout autre agent public implique dans la lutte contre la fraude.
>
> Cette prime est payee dans un delai ne depassant pas un mois a partir de l'encaissement.

### Parametres API

- `taux_prime_denonciation` = 10%
- `delai_paiement_prime` = 1 mois apres encaissement

---

## Article 142 -- Amende pour non-versement de retenue a la source

### Texte de l'article

> Si une personne chargee de retenir l'impot a la source ne transfere pas cet impot a l'Administration fiscale, elle est passible d'une amende egale a cent pour cent (100%) de l'impot non transfere. Il en est de meme d'une personne qui s'abstient de retenir l'impot a la source.

### Resume

Amende de **100%** si le collecteur ne reverse pas le prelevement. Cette meme amende s'applique si le collecteur ne retient meme pas l'impot. C'est la sanction la plus lourde liee directement au PF.

### Parametres API

- `taux_amende_non_versement_retenue` = 100%
- `base_calcul` = IMPOT_NON_TRANSFERE

---

## Article 143 -- Obstruction et complicite

### Texte de l'article

> Toute personne qui entrave ou tente d'entraver les activites ou les taches de l'Administration fiscale dans l'exercice de ses competences ou qui se rend coupable de complicite, d'incitation ou de conspiration avec d'autres personnes dans le but de commettre une infraction a la presente loi est passible des memes peines que celles qu'encourt le contribuable.

---

## Article 146 -- Fermeture d'etablissement

### Texte de l'article

> Lorsqu'un contribuable s'abstient de payer des impositions devenues exigibles et apres epuisement de toutes les voies de recouvrement, le Commissaire general ordonne la fermeture provisoire de son etablissement jusqu'au paiement total ou partiel de sa dette.

---

# TITRE III : SYNTHESE DES PARAMETRES A STOCKER EN BASE

| # | Parametre | Valeur | Source |
|---|-----------|--------|--------|
| 1 | taux_pf_acompte_importation | 3% | Art. 77 LF |
| 2 | taux_pf_lib_sucre | 1% | Art. 78 LF |
| 3 | taux_pf_lib_bieres | 1% | Art. 78 LF |
| 4 | taux_pf_lib_limonades | 0,5% | Art. 78 LF |
| 5 | taux_pf_lib_jus | 0,5% | Art. 78 LF |
| 6 | taux_pf_lib_vins | 2% | Art. 78 LF |
| 7 | taux_pf_lib_liqueurs | 20% | Art. 78 LF |
| 8 | taux_pf_lib_eau_minerale | 1% | Art. 78 LF |
| 9 | taux_pf_lib_farine | 0,85% | Art. 78 LF |
| 10 | taux_pf_lib_huiles_locales | 2% | Art. 78 LF |
| 11 | taux_pf_lib_cigarettes | 1% | Art. 78 LF |
| 12 | taux_pf_lib_tissus | 1% | Art. 78 LF |
| 13 | taux_pf_lib_huiles_palmistes | 2% | Art. 78 LF |
| 14 | taux_pf_lib_carburants | 0,74% | Art. 78 LF |
| 15 | montant_pf_lib_bovin | 4 000 BIF | Art. 78 LF |
| 16 | montant_pf_lib_petit_betail | 2 000 BIF | Art. 78 LF |
| 17 | taux_pf_lib_cafe_parche | 0,9% | Art. 78 LF |
| 18 | montant_pf_declaration_standard | 50 000 BIF | Art. 150 LF |
| 19 | montant_pf_declaration_simplifiee | 10 000 BIF | Art. 150 LF |
| 20 | taux_pf_mobile_money | 1% | Art. 151 LF |
| 21 | taux_pf_convoi_vehicules | 5% | Art. 153 LF |
| 22 | taux_prelevement_numerique | 10% | Art. 158 LF |
| 23 | taux_prelevement_sfm | 22% | Art. 176 LF |
| 24 | taux_forfaitaire_micro | 1% | Art. 180 LF |
| 25 | seuil_ca_micro_contribuable | 25 000 000 BIF | Art. 180 LF |
| 26 | seuil_vehicules_exemptes_pf | 1 | Art. 78 LF |
| 27 | delai_clause_retro_vehicule_mois | 24 | Art. 78 LF |
| 28 | delai_declaration_pf_jours | 15 | Art. 78 LF |
| 29 | taux_penalite_paiement_tardif | 10% | Art. 131 PF |
| 30 | taux_penalite_sous_est_5_10 | 5% | Art. 132 PF |
| 31 | taux_penalite_sous_est_10_20 | 10% | Art. 132 PF |
| 32 | taux_penalite_sous_est_20_50 | 20% | Art. 132 PF |
| 33 | taux_penalite_sous_est_50_plus | 50% | Art. 132 PF |
| 34 | taux_penalite_imposition_office | 75% | Art. 133 PF |
| 35 | taux_penalite_fraude | 100% | Art. 134 PF |
| 36 | taux_amende_non_versement | 100% | Art. 142 PF |
| 37 | amende_fixe_petit | 100 000 BIF | Art. 130 PF |
| 38 | amende_fixe_moyen | 300 000 BIF | Art. 130 PF |
| 39 | amende_fixe_grand | 600 000 BIF | Art. 130 PF |
| 40 | amende_non_facturation | 20% | Art. 130 PF |
| 41 | delai_conservation_documents_ans | 10 | Art. 32 PF |
| 42 | delai_prescription_rectification_ans | 3 | Art. 56 PF |
| 43 | delai_prescription_recouvrement_ans | 10 | Art. 99 PF |
| 44 | delai_paiement_note_imposition_jours | 30 | Art. 67 PF |
| 45 | delai_remboursement_surplus_jours | 90 | Art. 67 PF |
| 46 | taux_retenue_source_dividendes | 15% | Art. 148 LF |
| 47 | taux_taf | 8% | Art. 167 LF |
| 48 | taux_penalite_retard_dividendes | 5%/mois | Art. 85 LF |
| 49 | amende_bris_scelles | 50 000 000 BIF | Art. 183 LF |
| 50 | multiplicateur_recidive | 2x | Art. 140 PF |

---

# TITRE IV : REGLES CRITIQUES POUR L'API

1. **Ordre d'imputation des paiements** (Art. 127) : TOUJOURS Interets -> Amendes -> Principal
2. **Distinction Acompte vs Liberatoire** : Le PF acompte (Art. 77) est deductible de l'IR annuel ; les PF liberatoires sont definitifs
3. **Collecteur vs Redevable** : Le fabricant/operateur collecte et declare, pas l'acheteur
4. **Interets non composes** (Art. 126) : Calcul mensuel simple, mois commence = complet
5. **Compteur vehicules** (Art. 78) : Maintenir un compteur annuel par individu
6. **Clause retroactive vehicules** (Art. 78) : Transfert dans 2 ans = PF exigible
7. **Penalites progressives** (Art. 132) : 4 paliers selon le taux de sous-estimation
8. **Non-versement = 100%** (Art. 142) : Sanction la plus lourde sur le collecteur

---

# TITRE V : AMBIGUITES SIGNALEES

| # | Article | Ambiguite | Recommandation |
|---|---------|-----------|---------------|
| 1 | Art. 77 vs 78 | Le carburant est exclu du PF acompte importation, mais les carburants locaux ont un PF liberatoire de 0,74%. Le carburant importe directement semble totalement exempt du PF acompte. | Prevoir un flag `exclure_pf_acompte` par produit |
| 2 | Art. 150 vs 77 | Le PF de 50 000 BIF par declaration douaniere est liberatoire. On ne sait pas s'il se cumule avec le PF acompte de 3% sur les memes importations. | Clarifier avec l'OBR ; prevoir les deux configurations |
| 3 | Art. 151 vs 176 | Le PF de 1% (commissions intermediaires mobile money) et le prelevement de 22% (frais services financiers mobiles) couvrent des perimetres proches mais distincts. | Distinguer clairement : Art. 151 = commission agent ; Art. 176 = frais plateforme |
| 4 | Art. 126 | Le taux d'interet est fixe par ordonnance ministerielle chaque annee. Si aucune ordonnance n'est publiee, le taux precedent est reconduit. | Prevoir une table de taux historiques avec date de validite |

---

*Document genere a partir de l'analyse OCR des textes de loi. Les citations sont fideles aux textes extraits mais peuvent contenir de legeres imprecisions dues a la reconnaissance optique de caracteres.*
