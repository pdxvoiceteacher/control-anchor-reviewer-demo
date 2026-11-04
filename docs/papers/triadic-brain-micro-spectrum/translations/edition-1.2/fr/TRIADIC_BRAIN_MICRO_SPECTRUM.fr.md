> **Note de traduction française.** Traduction intégrale du manuscrit principal de l’édition locale suivante 1.2, réalisée et révisée avec l’assistance de l’IA ; aucune certification par une personne francophone compétente n’est revendiquée. Le texte anglais fait foi pour l’interprétation. Les compléments lisibles par machine restent en anglais. La mention héritée « non publié » ci-dessous appartient aux métadonnées du brouillon source ; l’édition anglaise est désormais publiée. La notation numérique anglaise est conservée : la virgule sépare les milliers et le point marque les décimales ; les symboles mathématiques, les valeurs littérales, la bibliographie, les libellés des formules, le diagramme et le code restent inchangés pour préserver la correspondance exacte avec la source.
>
> **Source anglaise figée :** [édition 1.2 du 3 novembre 2026](https://github.com/pdxvoiceteacher/control-anchor-reviewer-demo/blob/23a674cab2af23baae6e74af2aaf5c7c934ff473/docs/papers/triadic-brain-micro-spectrum/2026-11-03-edition-1.2/TRIADIC_BRAIN_MICRO_SPECTRUM.md).
>
> **SHA-256 du fichier source :** `6b870b3bc448bed2755995d099b5ca94b35e4c3c09e7e057565116bf315fc0e9`.

# Triadic Brain de l’identité des octets aux connaissances révisables

## Une analyse technique fondée sur le code source des transformations de données des contrôles et de l’investigation distribuée

**Thomas Prislac**  
**Manuscrit de recherche, édition locale succédant à la précédente, version 1.2, 3 novembre 2026**  
**Analyse du code source préservée, avec une proposition d’évaluation de la réutilisation et un objectif d’autonomie ; non publié**

## Résumé

Triadic Brain est étudié comme une architecture d’investigation attribuable, bornée et révisable. L’unité d’analyse n’est pas une particule cognitive métaphorique, mais la plus petite représentation pour laquelle une opération donnée est bien définie : une chaîne d’octets, un empan Unicode, un enregistrement applicatif, une requête fournisseur, une assertion candidate, une mise en correspondance relationnelle, un artefact de preuve ou un événement de conservation sous contrôle. Une reconstruction fondée sur le code source suit ces unités à travers l’admission authentifiée, l’envoi au modèle autorisé séparément, la capture de la réponse, l’ancrage déterministe dans les sources, l’évaluation native, la révision et la présentation. Un exemple témoin multioctet exact distingue les octets originaux de la source normalisée, de la réponse extraite et de la capture sémantique dérivée. La reconstruction met au jour une frontière importante : la passerelle JOINED ordinaire pour les sorties de modèle capturées attribue à l’incertitude non mesurée la valeur prudente un, ce qui force, sous certaines conditions, son filtre natif à refuser même une citation exacte présentant une couverture lexicale complète et une masse softmax de singleton égale à un. La réponse reste inspectable. Les quantités associées à GUFT sont distinguées selon leur producteur, leur domaine, leurs unités et leur version ; les transformations historiques de bancs d’essai, les hypothèses de champs sur graphes et les indicateurs structurels indirects actuels ne sont pas fusionnés en un score unique. Une analyse explicite du noyau réduit de rivière montre pourquoi le pas de un utilisé par son appelant effectif exige des conditions de stabilité dépendant du graphe, que la valeur par défaut plus petite du noyau n’établit pas. AHA est analysé comme un contrôle des ponts relationnels fournis, fondé sur le code source, tandis que les mécanismes d’essaim et de grammaire partagée sont distingués de la corroboration empirique. La contribution consiste en une analyse auditable des transformations implémentées et des articulations de recherche non résolues, accompagnée d’un graphe d’assertions lisible par machine. Cette étude n’effectue aucune exécution du produit ni aucune expérience d’inférence et ne revendique ni qualification en fonctionnement d’un système à trois nœuds, ni utilité sémantique calibrée, ni autorité d’action autonome.

**Mots-clés :** provenance ; architecture cognitive ; représentation ; raisonnement analogique ; incertitude ; stabilité numérique ; investigation multiagent ; gouvernance de l’information.

## 1 Question de recherche et contribution

Que devient un petit élément de données lorsqu’il entre dans Triadic Brain, et quelle justification supplémentaire existe lorsque le système présente ensuite un résultat utile ? Répondre exige de distinguer trois questions : quelle représentation a été transformée, quelle procédure l’a effectivement consommée et quelle inférence les éléments probants obtenus permettent d’étayer. Une empreinte de source peut établir une relation d’identité sans établir la vérité factuelle. Une analogie conforme à un schéma peut préserver une relation sans valider son transfert vers un nouveau domaine. Un candidat révisé peut encore ne pas disposer de l’autorisation nécessaire à un usage lourd de conséquences.

La proposition de recherche qui organise l’architecture est que l’accueil réceptif des données, la comparaison structurelle, la continuité, la mise à l’épreuve et la révision peuvent opérer sur un enregistrement typé commun tout en préservant les significations propres aux domaines et les désaccords. Cet élément commun est une grammaire des relations entre observations, transformations, hypothèses, contraintes, résidus et provenance. Il ne s’agit pas d’affirmer qu’une coordonnée à valeurs réelles représente toute la cognition. Cette lecture préserve le vocabulaire voulu de corridor, rivière, tresse et terrasse comme programme d’organisation de l’investigation, sans traiter ce vocabulaire comme la preuve d’une loi physique universelle. [I11, I12, I15]

Quatre contributions structurent cet article. Premièrement, une analyse au niveau des représentations identifie les frontières effectives entre octets, textes, assertions et artefacts dans un chemin applicatif maintenu. Deuxièmement, une analyse formelle distingue les preuves d’identité composables des affirmations non composables de vérité, d’indépendance et d’autorisation. Troisièmement, des déductions propres au code source révèlent un goulot d’étranglement dû au filtrage prudent, des espaces de noms de cohérence distincts et une condition de stabilité numérique dépendant du graphe. Quatrièmement, un programme de recherche explicite décrit comment l’investigation distribuée, la grammaire partagée et la reconstruction rétrospective pourraient être qualifiées sans transformer l’existence d’un code source en capacité démontrée.

La littérature connexe fournit des points de comparaison, non une validation par emprunt. W3C PROV-DM donne aux entités, activités, agents et dérivations un vocabulaire précis de provenance. La théorie de la mise en correspondance structurelle de Gentner motive l’examen de l’organisation relationnelle plutôt que de la ressemblance superficielle. Les recherches sur la calibration distinguent les scores normalisés des probabilités correspondant à une exactitude empirique. Aucun de ces travaux n’établit l’adéquation de cette architecture particulière. [PROV](https://www.w3.org/TR/prov-dm/), [Gentner 1983](https://groups.psych.northwestern.edu/gentner/papers/Gentner83.2b.pdf), [Guo et al 2017](https://proceedings.mlr.press/v70/guo17a.html).

## 2 Méthode et classes de preuves

### 2.1 Reconstruction du code source plutôt que nouvelle étude d’exécution

L’analyse utilise un ensemble sélectionné et clos de sources conservées à titre privé, des identités d’octets conservées séparément, des rapports historiques de qualification et des documents de recherche réconciliés. Une comparaison actualisée des sources acceptées n’a relevé que des modifications documentaires par rapport à l’instantané précédent du code d’exécution cartographié. L’inventaire sélectionné contient 163 copies de lecture ; 157 correspondent exactement à leurs objets blob Git originaux conservés séparément. Six copies de lecture issues de connecteurs contiennent un LF final supplémentaire ; la suppression de cet octet précis produit des copies sources reconstruites distinctes dont les identités complètes de blobs Git correspondent aux originaux épinglés. La cartographie privée des sources préserve les copies de lecture, les reçus de reconstruction et les empreintes distinctes, plutôt que de substituer une identité à une autre. Ces faits étayent une reconstruction bornée du code source, non un nouvel audit complet du dépôt ni une attestation de déploiement. [I01]

Aucun module du produit n’a été importé, aucun test du projet ni tâche de CI n’a été exécuté, aucun fournisseur n’a été appelé et aucun client installé ni pair actif n’a été sollicité pour cette étude. Les calculs portant sur l’exemple synthétique d’octets et les déductions analytiques élémentaires sont distincts de l’exécution du produit. L’exemple est délibérément incomplet en tant qu’enregistrement d’exécution : il ne possède ni acteur authentifié, ni profil de déploiement effectif, ni réponse réelle de fournisseur, ni horloge d’événement, ni révision humaine achevée. Les valeurs dépendant de ces entrées restent symboliques. [I01, I04]

Le vocabulaire des preuves est délibérément multidimensionnel :

| Code | Classe de preuves | Ce qu’elle établit | Ce qu’elle n’établit pas |
|---|---|---|---|
| S | Code source inspecté | Une définition, une branche ou un contrat existe dans le code source identifié | Exécution, installation ou utilité |
| C | Chemin d’appels inspecté | Un producteur spécifié est relié à un consommateur spécifié dans l’ensemble clos inspecté | Que ce chemin a été invoqué dans un déploiement |
| T | Test rédigé | Un contrôle et une population de jeux de données de test prévue existent | Un résultat concluant |
| R | Rapport d’exécution conservé | Un rapport rattaché au code source consigne une exécution historique bornée | Réexécution indépendante ou conformité au code source actuel |
| D | Déduction analytique | Une conclusion découle des équations du code source et des hypothèses énoncées | Un résultat observé en production |
| P | Mécanisme proposé | Une interface ou une expérience prévue est spécifiée | Implémentation ou adoption |
| H | Hypothèse de recherche | Une relation conjecturée ou un modèle formel est spécifié ; les tests empiriques peuvent encore exiger des définitions opérationnelles | Validité empirique |
| U | Indisponible ou non observé | Les éléments probants pertinents n’ont pas été établis ici | Zéro, fausseté ou autorisation d’inventer une valeur |

Une assertion peut porter plusieurs codes, par exemple S+C+D. Une hypothèse empirique prête à être testée nomme en outre ses observables, son périmètre et les observations susceptibles de la réfuter ; une définition formelle seule ne les fournit pas nécessairement encore. La chaîne S→C→R→déploiement→utilité n’est pas une chaîne d’implications. Une implémentation mécaniquement correcte d’un mauvais estimateur reste un mauvais estimateur. [I01, I11]

### 2.2 Qualification historique et révision indépendante

Les rapports conservés décrivent une qualification antérieure de 46 cas et un complément distinct de trois cas utilisant une capture synthétique de fournisseur, y compris l’inspection durable après perte d’un accusé de réception ou nettoyage incertain. Un autre rapport décrit 59 cas sélectionnés sans modèle, répartis sur deux sources, et explicitement non une nouvelle exécution unique de 59 cas. Les archives sous-jacentes n’étaient pas toutes disponibles pour une inspection indépendante dans cette étude. Il s’agit de rapports de classe R avec des rattachements privés exacts aux sources, non de preuves que le présent exemple témoin a été exécuté, que la sémantique de modèles en fonctionnement a été validée ou qu’un système installé à trois nœuds a été qualifié. Les tests rédigés sont consignés séparément sous T. [I18]

Les citations de sources privées I01–I20 renvoient à des chemins exacts, plages de lignes, identités de sources et périmètres de rapports dans une cartographie de révision distincte. Les références publiques sont directement liées. Cette séparation protège les informations d’implémentation et d’exploitation non publiées, mais limite la reproduction indépendante publique jusqu’à la disponibilité d’une publication autorisée et expurgée des sources et preuves. Cette limite ne peut être corrigée en citant une norme publique comme si elle prouvait un comportement privé. Pour la version 1 précédente, figée, cinq axes de révision technique délimités couvraient la fidélité aux sources, les mathématiques, la sécurité et la confidentialité, les assertions scientifiques, ainsi que la cohérence entre données machine et prose. La révision initiale a été suivie de corrections et d’une nouvelle révision indépendante des éléments concernés ; les 31 constats et recommandations dans ces périmètres ont tous été clôturés. Cette édition locale suivante préserve cette analyse des sources et ajoute la section 14.3, sa proposition de qualification et deux assertions explicatives destinées aux machines. Les résultats de révision de la version précédente ne s’étendent pas automatiquement à cet ajout ; la nouvelle édition possède son propre dossier de révision des éléments concernés. La révision technique n’implique ni acceptation par une revue, ni exécution du produit, ni qualification d’un système installé, ni reproduction empirique indépendante.

## 3 Types de représentation et plus petite unité porteuse de sens

Soient \(\mathbb B^*\) les chaînes finies d’octets, \(\mathbb U^*\) les séquences finies de valeurs scalaires Unicode, \(\mathcal J_p\) les valeurs JSON acceptées sous le profil \(p\), et \(\mathcal A\) les artefacts applicatifs typés. Une transformation est modélisée par une fonction partielle

\[
f:(x,\kappa,\pi)\rightharpoonup(y,e,z),
\tag{1}
\]

où \(\kappa\) est le contexte d’interprétation, \(\pi\) le contexte de contrôle effectif, \(e\) la preuve de l’opération et \(z\) un statut. Le refus, l’entrée indisponible et l’achèvement incertain sont des états représentés ; ils ne sont pas silencieusement remplacés par des valeurs de réussite. Il s’agit d’un modèle d’exposition, non d’une affirmation selon laquelle chaque fonction de l’implémentation possède littéralement cette signature.

L’octet est la plus petite unité adressée dans les contrats d’octets présentés. Le point de code Unicode est l’unité des coordonnées textuelles. Un jeton fournisseur est une unité définie par un tokenizer dont la correspondance dépend du modèle et du gabarit. Un type de jeton lexical est une unité différente, utilisée par le diagnostic natif des citations. Un empan d’assertion est une proposition textuelle bornée ; une correspondance de relations est l’unité du cas AHA fourni. Un événement de conservation sous contrôle est une observation consignée avec un ordre local. Un segment TCP ou un enregistrement TLS relève d’une couche de transport, non de ces unités sémantiques. UTF-8 permet à un caractère d’occuper plusieurs octets ; TCP fournit un flux d’octets plutôt que de préserver les frontières des enregistrements applicatifs. [RFC 3629](https://www.rfc-editor.org/rfc/rfc3629.html), [RFC 9293](https://www.rfc-editor.org/rfc/rfc9293.html).

Pour un artefact \(a\), le support sémantique minimal utile est donc relatif à une question. Pour vérifier un extrait, il faut au moins son texte, l’identité de sa source, la convention d’intervalle et les octets sources ou un enregistrement de vérification suffisamment digne de confiance. Pour évaluer une analogie, il faut des relations, des extrémités mises en correspondance, des restrictions de domaine et un test cible. Supprimer ces dépendances peut raccourcir un message tout en rendant l’opération voulue indéfinie. Les sources n’étayent l’existence d’aucun plus petit paquet sémantique universel. [I04, I05, I09]

Définissons séparément l’identité des octets et l’identité selon un profil :

\[
H_B(b)=\operatorname{SHA256}(b),\qquad
H_p(x)=H_B(C_p(x)),
\tag{2}
\]

où \(C_p\) est un encodage canonique explicitement versionné. Pour un JSON entrant non canonique \(b\), on a généralement \(H_B(b)\ne H_p(\operatorname{parse}(b))\). SHA-256 détecte les changements d’octets par rapport à une référence de confiance, sous ses hypothèses cryptographiques. Il n’authentifie pas l’auteur original et ne valide pas une proposition contenue dans les octets. [FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final).

Les sérialiseurs canoniques inspectés utilisent du JSON UTF-8 compact à clés triées, des nombres finis et un LF final unique. Leurs domaines acceptés diffèrent. L’un exige des chaînes déjà en NFC et rejette les codets de substitution ; le profil natif rejette en outre certains caractères de contrôle et caractères ignorables par défaut, et applique des restrictions sur les clés. Certains points d’entrée d’analyse syntaxique acceptent les espaces ordinaires du JSON, l’égalité des octets canoniques étant contrôlée à des frontières ultérieures. L’entier 1 et le flottant 1.0 peuvent être égaux lors d’une comparaison dans un langage hôte tout en se sérialisant en octets différents. Ce sont des profils du projet, non une affirmation de conformité au JSON Canonicalization Scheme. RFC 8785 constitue une comparaison utile précisément parce que les règles numériques et Unicode font partie d’un contrat de canonisation. [I02, I05]. [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html).

## 4 Le parcours maintenu et ses frontières d’autorité

La figure 1 présente le parcours JOINED ordinaire inspecté pour les sorties de modèle capturées. Les blocs représentent des responsables logiques ou des étapes d’artefacts, non des machines physiques fixes, et n’affirment pas que chacun correspond à un modèle distinct.

```text
Untrusted source + user task + explicit consent
                 |
          application intake
                 |
       authenticated gateway -------- technical rejection
                 |
       durable attempt and admission
          |              |
      AEGIS/UCC       frozen bindings
                 |
        exact dispatch authorization
                 |
        transactional claim and reservation
                 |
      provider adapter and bounded transport
                 |
      body capture + completion observations
                 |
      provider-specific text normalization
          |                    |
   CAPTURE_ONLY return     CAPTURED + JOINED
                               |
                    deterministic semantic bridge
                               |
                grounding / claims / UCM / AHA
                waveform / counterexamples / aperture
                               |
                    separately claimed Sophia audit
                               |
                   Atlas orientation and TEL closure
                               |
                     sealed inspectable artifacts
                               |
                separate human decision and permitted use
```

**Figure 1.** Reconstruction statique du chemin d’appels. Les événements sans modèle empruntent un chemin distinct d’admission et d’achèvement, sans candidat de modèle. Les observations terminales du fournisseur autres que CAPTURED ne deviennent pas implicitement des candidats natifs. Ni le schéma ni une étiquette d’artefact ne confèrent d’autorité pour une action ultérieure. [I03–I10]

L’entrée combine une source bornée, une tâche, les preuves fournies et un consentement explicite, écrit les octets exacts de la tâche avant soumission et peut lier des paires complètes sélectionnées d’une conversation antérieure. Le chemin inspecté de réutilisation contextuelle limite les messages antérieurs à 16 et le contexte canonique à 16,000 octets ; il rejette les dépassements plutôt que de tronquer silencieusement. Il s’agit d’une sélection explicite, non d’une preuve de récupération générale en mémoire. La passerelle impose un plafond de 32,768 octets au corps de la tâche et déduit l’acteur du contexte applicatif authentifié. Un texte source ne peut pas s’autoriser lui-même en revendiquant un rôle de confiance. [I03]

La passerelle transmet les octets de la tâche encodés en base64 au dispositif de conservation sous contrôle. Pour \(n\) octets d’entrée, la longueur du base64 avec remplissage est de \(4\lceil n/3\rceil\) caractères. Il s’agit d’un encodage réversible, avec surcoût, non d’un chiffrement ni d’une compression sémantique. Le dispositif de conservation consigne une tentative avant l’admission, y compris les octets soumis bornés et leur identité. L’idempotence des enregistrements lie l’acteur et la clé à la sémantique exacte de la charge utile brute : une réutilisation avec des octets modifiés produit un conflit. Les tentatives rejetées et incertaines restent dans la population observée. [I03]

L’admission fige un profil de contrôle effectif et un contexte d’exécution, valide l’autorisation relative à la tâche, à la confidentialité et au fournisseur, construit un ancrage normalisé et invoque AEGIS. Les anciens modes hors observation exécutent aussi le plan d’admission UCC ; le profil d’observation inspecté ne conserve ce plan de compatibilité qu’à titre de définition et effectue plus tard une évaluation métier consultative distincte, tandis que les frontières techniques relatives aux entrées, aux rôles, à la confidentialité, à la capacité et à l’envoi restent appliquées. Ainsi, « contrôlé » ne signifie pas que chaque politique nommée constitue un veto exécutable dans chaque mode. Ici, le contrôle applicatif de confidentialité vérifie le consentement explicite à la tâche et la concordance avec l’identifiant de politique configuré. La porte de contrôle native de confidentialité transmet cette base déclarée et vérifie son contrat booléen/base ; elle ne classe pas indépendamment les contenus sensibles et n’établit pas l’adéquation de la politique pour chaque personne concernée ou destinataire. Une analyse syntaxique réussie ne transforme pas en autorité les instructions d’une source non fiable. [I03]

L’envoi exige l’enregistrement exact en file d’attente, sa version et l’empreinte de la requête. La prise en charge transactionnelle revérifie les limites et liaisons pertinentes, construit le corps de la requête fournisseur et effectue une réservation comptable avant l’invocation. Une réservation ne prouve ni l’achèvement distant ni une facturation. Les requêtes en cours reprises après redémarrage deviennent UNKNOWN plutôt que d’être répétées aveuglément. La logique d’ingénierie s’apparente au moindre privilège et à la médiation complète, mais la présence de ces principes de conception n’est pas une certification de sécurité. [I06]. [Saltzer and Schroeder 1975](https://web.mit.edu/Saltzer/www/publications/protection/Basic.html).

## 5 Un exemple témoin multioctet exact

### 5.1 Octets et coordonnées

Prenons la source illustrative ` Café.\r\n` et la tâche `Quote the source.`. La source contient un U+0020 initial, le caractère U+00E9 déjà en NFC et CRLF. Posons, sans appel de modèle, que le texte de réponse extrait est `Café.`. Le normaliseur de la passerelle applicative est

\[
N(s)=\operatorname{NFC}\!\left(\operatorname{CRtoLF}
 (\operatorname{CRLFtoLF}(s))\right).\operatorname{strip}()+\mathrm{LF}.
\tag{3}
\]

NFC concerne l’équivalence canonique Unicode ; la substitution des fins de ligne et la suppression des espaces aux extrémités sont des opérations applicatives supplémentaires. Elles ne doivent pas être attribuées à la norme de normalisation Unicode. L’ancrage natif direct suit un autre contrat : il convertit les fins de ligne et supprime les espaces aux extrémités, mais exige une entrée déjà en NFC plutôt que d’appliquer silencieusement NFC. L’admission canonique initiale peut également rejeter une entrée non NFC avant la passerelle ultérieure. Cet exemple témoin est déjà en NFC et ne démontre pas l’acceptation d’une graphie décomposée arbitraire. [I02, I04, I05]. [Unicode UAX 15 revision 57](https://www.unicode.org/reports/tr15/tr15-57.html).

| Représentation | UTF-8 hex | Points de code | Octets | SHA-256 |
|---|---|---:|---:|---|
| Source originale | `20436166c3a92e0d0a` | 8 | 9 | `4068c2d9de08c36023e33a7858bf0d9e36bfa39017edd2af2d1927ed413e2498` |
| Source normalisée | `436166c3a92e0a` | 6 | 7 | `ead8f00c3b7dd22fe4ea6e1679b51bbbe2696e72b0692a278bf100aae0928b9d` |
| Réponse extraite | `436166c3a92e` | 5 | 6 | `7d84df6634452499da807a641b387dbcb28193ef940a6fb297ac86c652d5ca75` |

Ce sont des identités calculées d’octets synthétiques, non des preuves d’inférence capturées. U+00E9 occupe deux octets UTF-8. L’intervalle de la réponse est [0,5) en points de code et [0,6) en octets UTF-8. Ce sont des coordonnées semi-ouvertes indexées à partir de zéro dans la source normalisée, non des coordonnées de grappes de graphèmes, UTF-16, de tokenizer ou de fichier original. [I04]

Dans ce parcours, le constructeur d’ancrage natif reçoit les sept octets déjà normalisés. Par conséquent, ses empreintes de source et de source normalisée coïncident, tandis que l’identité originale de neuf octets demeure dans la liaison d’admission distincte. Un appelant de plus bas niveau transmettant directement les octets originaux produirait une identité différente de source native. Un article qui appelle chacune de ces représentations « la source brute » perd la distinction qu’il prétend expliquer. [I04, I05]

L’équation (3) est plusieurs-à-un. Par exemple, les distinctions d’espaces aux extrémités disparaissent. Il n’existe donc pas d’inverse général \(N^{-1}\). La conservation de l’empreinte originale permet de consigner quel original a été admis uniquement lorsque la liaison de conservation de confiance est disponible ; l’empreinte seule ne permet pas de reconstruire les octets supprimés. Cela établit une frontière concrète de perte d’information sans prétendre que l’opération préserve le sens dans les langages ou formats sensibles aux espaces.

### 5.2 Expansion et identité des artefacts

La source courte n’est pas l’entrée complète du modèle. Une enveloppe illustrative source/preuves/tâche compte 161 octets UTF-8, et son tableau JSON canonique à un message compte 200 octets. Un corps de réponse fabriqué au format fournisseur, utilisé uniquement pour illustrer la sérialisation, compte 91 octets et porte une identité explicite NOT_EXECUTED. Aucun comptage de tokenizer, aucune latence, aucune identité de fournisseur ni capture de paquets ne sont déduits de ces tailles. L’enveloppe complète de la requête et la configuration du fournisseur demeurent non spécifiées. [I04]

L’ancrage natif segmente le texte normalisé aux frontières de paragraphes, avec un repli par lignes pour un paragraphe unique multiligne. Il n’infère pas de propositions minimales. L’exemple témoin produit un segment contenant le texte `Café.`, des décalages indépendants en points de code et en octets, ainsi que l’empreinte de l’extrait ci-dessus. Le JSONL construit du segment correspondant compte 243 octets, son manifeste 525 octets et le JSON de capture sémantique dérivée 684 octets. Ces artefacts plus volumineux portent des informations de coordonnées, d’identité et de contrôle. Ils illustrent le surcoût de la traçabilité des responsabilités, non un rapport d’efficacité de bout en bout mesuré. [I04, I05]

La sérialisation crée d’autres domaines d’identité. Les octets nus de la réponse ont une longueur de six ; le scalaire JSON natif `"Café."` suivi d’un LF a une longueur de neuf ; l’objet `{"text":"Café."}` suivi d’un LF a une longueur de 18 ; une graphie de comparaison utilisant des échappements ASCII a une longueur de 22. Omettre le LF terminal de l’objet donne 17 octets et une empreinte différente. Des chaînes décodées égales n’impliquent pas des artefacts sérialisés égaux. L’exemple témoin lisible par machine consigne les octets et empreintes exacts pour chaque comparaison. [I04]

## 6 Traitement du modèle et limites de visibilité de la trace

### 6.1 Sémantique des adaptateurs et du transport

Les profils de fournisseurs pris en charge définissent des contrats textuels bornés et non diffusés en continu. Un adaptateur de type génération peut sérialiser un historique étiqueté par rôles en une seule chaîne de prompt, tandis que les adaptateurs de type conversation envoient des tableaux de messages et qu’un autre profil utilise des blocs typés d’entrée et de sortie textuelles. L’existence d’une enveloppe applicative commune ne rend pas identiques la tokenisation des fournisseurs ni leurs gabarits de conversation. La normalisation de la réponse vérifie la forme d’achèvement prise en charge : un texte complet peut devenir CAPTURED ; un refus explicite reste REFUSED ; les erreurs HTTP deviennent FAILED ; une sortie incomplète, limitée en longueur ou non prise en charge peut devenir UNKNOWN. Les appels d’outils et les modalités non prises en charge ne peuvent pas être silencieusement interprétés comme la réponse textuelle prise en charge. [I06]

Le transport maintenu conserve des observations du corps de réponse applicatif, non des trames Ethernet, des paquets IP, des segments TCP, des enregistrements TLS ou les octets complets des en-têtes HTTP. Le cadrage HTTP et la protection des enregistrements TLS sont des couches distinctes. Un bloc livré par une bibliothèque n’est ni un paquet réseau stable ni un jeton de modèle. La configuration inspectée désactive HTTP/2, refuse les redirections, ignore les proxys de l’environnement et demande un encodage de contenu identity ; ce sont des paramètres du code source, non des mesures d’une session. La spécification TLS 1.3 de 2018 est citée ici comme référence de couche, non comme affirmation portant sur une connexion négociée particulière ou sur la spécification la plus récente. [I06]. [RFC 9112](https://www.rfc-editor.org/rfc/rfc9112.html), [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446.html).

Pour les parcours externes, le code source spécifie une résolution d’adresses publiques approuvée, une cible de connexion numérique avec Host/SNI officiel, la vérification TLS, des observations du pair connecté et de l’empreinte du certificat, ainsi que des bornes sur la requête, la réponse, le délai et le nettoyage. Les parcours locaux ont des contraintes de bouclage distinctes. Les contrôles de répétition de secrets connus peuvent empêcher la mise à disposition d’un corps, mais n’établissent pas une prévention exhaustive des fuites de données. La protection du transport ne rend pas les valeurs de source et de contexte secrètes pour leur point de calcul autorisé ; le §15 distingue cette visibilité du périmètre des copies conservées. Les octets observés du corps et ceux du préfixe conservé possèdent des longueurs et empreintes distinctes, afin qu’un préfixe borné ne soit pas présenté à tort comme un corps complet. [I06]

### 6.2 Internes du modèle sous hypothèse conditionnelle

Pour un environnement d’exécution fondé sur un transformeur, une décomposition de référence utile est

\[
u\xrightarrow{\text{format}_t}\tilde u
\xrightarrow{\tau_v}(t_1,\dots,t_n)
\xrightarrow{\text{embedding}}H_0
\xrightarrow{F_{\theta,b}}H_L
\xrightarrow{\text{head/decoding}}(\hat t_1,\dots,\hat t_m)
\xrightarrow{\operatorname{decode}_v}\hat u.
\tag{4}
\]

Ici, \(v,t,\theta,b\) désignent le tokenizer et sa version, le formatage d’entrée et son gabarit, les paramètres et le contexte du moteur de calcul, non des valeurs observées. Le décodeur nommé ne suppose pas l’existence d’un inverse bijectif de la tokenisation. Un bloc d’attention standard utilise

\[
\operatorname{Attn}(Q,K,V)
=\operatorname{softmax}(QK^\top/\sqrt{d_k}+M)V.
\tag{5}
\]

Dans l’équation (5), \(d_k\) est la dimension des requêtes et des clés, et M est le masque d’attention additif ; softmax opère sur les clés. Les équations (4)–(5) fournissent un contexte architectural. Elles n’identifient ni les couches du moteur d’exécution réel, ni sa quantification, ses activations cachées, son état KV ou l’aléa de décodage. Le travail original sur le Transformer établit cette construction de l’attention, non l’implémentation d’un quelconque déploiement privé. [Vaswani et al 2017](https://arxiv.org/abs/1706.03762v7).

La trace applicative inspectée ne révèle ni la séquence réelle de jetons, ni l’expansion du gabarit appliqué, ni les tenseurs internes, ni l’erreur numérique du moteur de calcul, ni les mises à jour d’entraînement. Les comptages d’utilisation rapportés sont des déclarations du fournisseur soumises à validation contractuelle. L’identité des poids hébergés n’est pas observée ; l’identité locale configurée ou de disponibilité n’est pas une attestation d’exécution. La génération par modèle constitue donc, dans cette analyse, une transformation causalement importante mais opaque en interne. L’analyse déterministe de la passerelle native est inspectable en aval et ne doit pas être confondue avec une fenêtre sur le calcul latent du modèle. [I06]

### 6.3 Achèvement comme produit d’états

Utilisons le produit d’états explicatif

\[
Z=(z_{admit},z_{dispatch},z_{body},z_{norm},z_{eval},
z_{posture},z_{review},z_{use},z_{payload},z_{cleanup}).
\tag{6}
\]

Un corps peut être complet alors que le nettoyage reste incertain. Une inférence distante peut avoir eu lieu même si l’accusé de réception de la capture locale est perdu. L’exécution historique peut rester achevée après expiration de la charge utile conservée. CAPTURED peut coexister avec le REFUSE natif et un HOLD du réviseur. L’annulation consigne une tentative d’intervention, non la preuve que le calcul distant a cessé. Les identités exactes permettent une réconciliation plutôt que l’hypothèse dangereuse selon laquelle une requête non acquittée n’a jamais été exécutée. Cette factorisation est un modèle analytique des distinctions présentes dans les sources, non un nouveau schéma unifié d’état d’exécution. [I06, I10, I14]

## 7 Transformations natives du texte de réponse à un candidat révisé

### 7.1 Assertions déterministes et liaison aux preuves

La passerelle sémantique normalise le texte terminal extrait et découpe en assertions les empans de paragraphes ou de lignes débarrassés de leurs espaces aux extrémités. Elle ne coupe pas aux points, ce qui évite certaines erreurs liées aux décimales et aux abréviations, mais ne revendique pas non plus l’extraction de propositions. Pour chaque empan, elle recherche une sous-chaîne exacte dans les segments d’ancrage. Une première correspondance exacte produit une référence SUPPORTS déclarée par le candidat ; l’absence de correspondance ne produit aucune référence. L’opération propose un appui citationnel, non une implication sémantique ni une sélection exhaustive des sources. [I05]

La passerelle consigne trois identités distinctes : corps fournisseur en amont, enveloppe fournisseur normalisée et capture sémantique dérivée. La « sortie brute » en aval de l’adaptateur de candidat capturé est ce JSON sémantique dérivé. Sa quarantaine contient 684 octets dans cet exemple témoin, non le corps fournisseur original. L’adaptateur est une façade locale sans invocation de modèle. Confondre les deux adaptateurs laisserait entendre à tort qu’un audit en aval a relu indépendamment les octets de réponse en direct. [I05, I07]

Le contrat de données suivant est une **projection illustrative**, non une requête exécutable du produit ni le schéma complet littéral du candidat :

```json
{
  "representation": "claim_excerpt_projection",
  "evidence_class": "CONSTRUCTED_NOT_EXECUTED",
  "text": "Café.",
  "coordinate_domain": "normalized_source",
  "code_point_interval": [0, 5],
  "utf8_byte_interval": [0, 6],
  "source_sha256": "ead8f00c3b7dd22fe4ea6e1679b51bbbe2696e72b0692a278bf100aae0928b9d",
  "excerpt_sha256": "7d84df6634452499da807a641b387dbcb28193ef940a6fb297ac86c652d5ca75",
  "declared_relation": "SUPPORTS",
  "semantic_entailment_established": false,
  "authority_effect": "NONE"
}
```

La validation des assertions reconstruit l’identité source/segment, l’identité de l’extrait, l’identité du texte de l’assertion, l’inclusion des intervalles et la concordance octets/points de code ; les références qui se chevauchent dans une assertion sont marquées comme invalides. La catégorie d’appui dépend de l’intégrité des citations et de la relation déclarée. Un tokenizer lexical fixe utilise des empans Unicode de type mot, la neutralisation de la casse et des mots vides anglais. Sa couverture des types de jetons uniques est un diagnostic, non le nombre de jetons du fournisseur ni une vraisemblance factuelle. Pour l’exemple témoin, l’assertion et l’extrait se réduisent chacun à `{café}`, donnant une couverture de un et aucun type de jeton résiduel. [I05]

Les identifiants de candidats utilisent un préfixe de 24 caractères hexadécimaux du SHA-256 de la concaténation ASCII de deux chaînes complètes d’empreintes hexadécimales. La graine contient donc 128 octets ASCII, non 64 octets d’empreintes binaires. Ce préfixe est une étiquette de 96 bits ; l’empreinte complète de l’artefact reste l’identité utilisée dans les assertions d’intégrité. Les étiquettes des ensembles d’ancrage utilisent de même un préfixe de 20 caractères hexadécimaux. Les étiquettes tronquées ne doivent pas remplacer discrètement les empreintes complètes d’artefacts dans les preuves ou les raisonnements sur les collisions. [I05]

### 7.2 Classement UCM et invariant prudent d’incertitude

Soit \(r\) la fraction des assertions non marquées comme non étayées, et \(u\in[0,1]\) le champ d’incertitude du candidat. Les axes structurels par défaut sont

\[
a=(E_{cpl},T_{tr},E_s,\lambda_{phase},\mu_{contain})
=(r,1,1,1-u,r),\qquad \psi_{CL}=E_{cpl}T_{tr}.
\tag{7}
\]

Ce sont des indicateurs indirects sans dimension définis par le code source. Leurs noms n’établissent ni symétrie éthique empirique, ni empathie psychologique, ni stabilité de phase physique. Les métadonnées fournies pour l’ensemble des axes et les hypothèses déclarées par l’appelant sont des entrées distinctes dans le contrat natif. [I07]

Pour une population non vide de scores finis \(s_i\) répartie selon des groupes d’équivalence déclarés \(g\), UCM calcule

\[
p_i=\frac{\exp(s_i-s_{max})}{\sum_j\exp(s_j-s_{max})},\quad
P_g=\sum_{i\in g}p_i,\quad
m=P_{(1)}-P_{(2)}.
\tag{8}
\]

Les masses des groupes sont ordonnées de façon décroissante, et \(P_{(2)}=0\) lorsqu’il n’existe qu’un seul groupe. La population complète détermine le résultat ; top-k n’affecte que la présentation, avec consignation des masses affichées conservées et omises. Le code appelle \(p_i\) des probabilités a posteriori, mais les scores d’entrée sont des logits déclarés par l’appelant, non des log-vraisemblances mesurées. Un singleton reçoit nécessairement une masse de un, même si l’unique option est erronée. Normaliser n’est pas calibrer, distinction également centrale dans les recherches empiriques sur la calibration. [I07]. [Guo et al 2017](https://proceedings.mlr.press/v70/guo17a.html).

L’ordre de priorité implémenté est non compensatoire. REFUSE s’applique en l’absence de références sources authentifiées, si la transparence est inférieure à .20, si l’incertitude est au moins .85, si des assertions non étayées subsistent ou si une hypothèse fournie est hors distribution. Sinon, HOLD s’applique pour \(\psi_{CL}<.45\), un indicateur de symétrie éthique inférieur à .50, une incertitude supérieure à .40, une marge d’équivalence inférieure à .10 ou un statut de motif nouveau ou ambigu. Les autres cas donnent PASS_SCREEN, avec révision humaine obligatoire et autorité NONE. Ces seuils sont des faits du code source, non des frontières de décision scientifiquement validées. [I07]

**Invariant conditionnel.** Chaque invocation réussie du constructeur JOINED ordinaire inspecté pour les sorties de modèle capturées fixe \(u=1.0\), explicitement comme maximum prudent non mesuré. Si le constructeur et le filtre UCM natifs inchangés sont ensuite atteints avec des artefacts valides, \(u\ge.85\), donc REFUSE s’ensuit quels que soient les autres axes ou logits. Pour l’exemple témoin, \(r=1\), \(a=(1,1,1,0,1)\), \(\psi_{CL}=1\), \(p_1=1\) et \(m=1\), mais le contrôle d’incertitude refuse malgré tout. Il s’agit de preuves S+C+D concernant ce parcours, non d’un taux d’erreur observé ni d’un énoncé global sur toutes les réponses. [I07]

CAPTURE_ONLY n’exécute pas cette branche native. Les événements sans modèle n’ont pas de candidat de modèle. Une API de capture de plus bas niveau peut recevoir une autre incertitude conforme au schéma dans le cadre d’un contrat différent. Aucun de ces faits ne justifie de fabriquer une incertitude moindre pour faire réussir le parcours ordinaire. Un estimateur alternatif aurait besoin de sa propre définition, de sa population de calibration, de son traitement des échecs et d’une intégration en aval qualifiée. Le comportement prudent actuel préserve l’inspection tout en refusant une promotion épistémique.

### 7.3 Forme d’onde synthétique et recherche bornée de contre-exemples

La forme d’onde de référence actuelle encode les cinq axes ordonnés sous la forme

\[
x_j=\operatorname{round}_{12}\!\left[
\frac15\sum_{k=1}^5a_k\sin(2\pi kj/N)\right],\quad
E_{codec}=\operatorname{round}_{12}\left[N^{-1}\sum_jx_j^2\right].
\tag{9}
\]

Le domaine d’échantillonnage est l’entier \(N\in[16,4096]\), avec \(j=0,\ldots,N-1\) et, par défaut, \(N=64\). La phase est exprimée en cycles par enregistrement synthétique, non en temps en secondes. Avant arrondi, l’orthogonalité discrète donne \(E_{codec}=\sum_k a_k^2/50\) pour ces nombres d’échantillons, donc .08 pour l’exemple témoin. Cette déduction n’est pas une exécution mesurée de forme d’onde. Différents vecteurs d’axes peuvent avoir la même énergie ; l’énergie seule perd donc l’information de répartition. Aucune fréquence physique d’une personne, d’un modèle ou d’un archétype n’est mesurée, et l’utilité interdomaines demeure explicitement non établie. [I08]

L’étape des contre-exemples dresse la liste des assertions non étayées et recherche un ensemble fini de marqueurs de limitation dans les jetons lexicaux des segments sources. L’exemple témoin ne produit aucune correspondance. Ce zéro signifie qu’aucune correspondance n’a été détectée par cette méthode bornée ; il ne constitue ni une réfutation exhaustive, ni un débat contradictoire entre modèles, ni la preuve que la proposition n’a aucun contre-exemple. [I08]

### 7.4 Révision Aperture et sortie utile

Aperture évalue des conditions impératives concernant le consentement à la tâche, le prédicat de politique de confidentialité transmis, le consentement facultatif à la rétention PMR, l’ancrage, le contexte, la quarantaine, les preuves des assertions, l’absence de refus UCM et l’absence de rejet AHA. L’échec d’une condition impérative produit REFUSE avant l’examen de mises en attente moins strictes. Sur les entrées par ailleurs valides de l’exemple témoin, seul le contrôle UCM échoue. L’absence d’AHA est conservée séparément mais ne remplace pas le motif de la condition impérative. PMR est désactivé dans ce parcours ordinaire, tandis que la conservation requise des preuves reste active. « Aucune écriture PMR » ne peut donc pas signifier « aucun contenu n’a été stocké ». [I08]

Sophia recalcule séparément certaines relations entre artefacts, dont les empans, la carte des assertions, la projection UCM complète, les résidus, la forme d’onde, AHA, les contre-exemples, aperture et TEL. Il utilise une tolérance numérique locale de \(10^{-12}\) lorsque cela est spécifié ; l’égalité des empreintes d’octets constitue une autre condition. Il lit des reçus de vérification dits raw-free, qui excluent certains octets bruts, plutôt que les octets de quarantaine et indique explicitement qu’il n’a pas vérifié indépendamment ces octets absents. Il ne réexécute pas les prédicats de politique UCC. [I10]

Pour l’exemple témoin conditionnellement valide, le refus UCM/aperture correctement consigné et l’indisponibilité d’AHA produisent Sophia HOLD, pas nécessairement REJECT. Des artefacts mal formés ou incohérents peuvent produire un rejet. Atlas associe ce HOLD à quarantine/do_not_publish, avec décision humaine en attente. Un audit PASS exigerait encore une révision humaine. La sortie rendue peut présenter la citation exacte, les preuves, les conditions non résolues et la provenance sans qualifier la citation de faisant autorité. Un retour de clarification est REQUESTED_NOT_EXECUTED ; il ne prouve pas qu’une boucle automatique de réparation a été exécutée. [I10]

Le scellement suit l’audit, l’orientation et la finalisation TEL. Il inventorie les octets et empreintes exacts des charges utiles et lie les artefacts retournés. Il ne constitue ni une signature, ni une immutabilité face à un hôte privilégié, ni une certification sémantique. L’export facultatif d’archive est une autre représentation, avec sa propre identité d’octets et ses hypothèses de compression. Le produit utile de cet exemple est une explication inspectable de la mise en attente d’une citation apparemment parfaite. C’est un résultat substantiel, même s’il ne s’agit pas d’une réponse finale approuvée. [I10]

## 8 GUFT comme grammaire comparative typée

### 8.1 Préserver les espaces de noms plutôt que choisir un scalaire universel

GUFT est conservé comme terme du projet. Cet article n’en infère pas un nouveau développement et n’affirme pas que des quantités de noms semblables partagent un estimateur. L’enregistrement approprié pour une quantité est

\[
q=(\text{namespace},\text{formula version},\text{domain},\text{inputs},
\text{units},\text{producer},\text{consumer},\text{missingness},
\text{clipping},\text{evidence class}).
\tag{10}
\]

L’équation (10) est un contrat d’exposition. Elle n’est pas présentée comme un schéma universel d’exécution déjà appliqué partout. Elle empêche qu’une transformation de banc d’essai, un indicateur de couverture des sources, un rapport d’inversion de série temporelle et une quantité de verrouillage de phase deviennent silencieusement interchangeables simplement parce que tous s’appellent E, T, Ψ ou Λ. [I11]

Le produit local borné \(\Psi_{local}=ET\), sous \(E,T\in[0,1]\), satisfait \(0\le ET\le E\le1\). Ce théorème élémentaire est valide pour les opérandes déclarés. Le code source Lean conservé contient les termes de preuve correspondants, mais cette étude ne les a pas compilés et n’a pas audité les imports. Aucune preuve algébrique ne peut établir qu’un producteur non calibré mesure la transparence ou l’empathie. Une autre expression exploratoire de stabilité est

\[
\Psi_{stability}=\frac{ET E_s\Lambda_{lock}}
 {\Delta S+D+\varepsilon}.
\tag{11}
\]

Elle n’appartient pas nécessairement à [0,1], et \(\varepsilon>0\) ne garantit pas un dénominateur positif si d’autres termes sont signés. \(\Lambda_{lock}\) n’est pas le Λ de dérive maximale de la télémétrie. L’équation définissant intégralement un objet nommé séparément Formula-of-Record n’a pas été retrouvée dans les fenêtres de code source délimitées ; aucune formule n’est reconstruite ici à partir de son étiquette. [I11]

### 8.2 Télémétrie historique effective des bancs d’essai

Un estimateur conservé lit des valeurs numériques dans des CSV de bancs d’essai, prend les valeurs absolues dans un préfixe borné, filtre les grandes entrées assimilables à des entiers selon une règle de repli et calcule

\[
p=\operatorname{mean}_{k\le4000}\log(1+|x_k|),\qquad
E=\operatorname{clip}_{01}(e^{-p/80}).
\tag{12}
\]

Les commentaires du code source indiquent que le diviseur 80 a été choisi pour maintenir E assez élevé pour les contrôles Ψ ; c’est un choix d’échelle de conception, non une calibration sémantique empirique. Sa valeur par défaut en l’absence de nombres est \(E=1,p=0,count=0\). T provient de la couverture d’audit avec des replis favorables ; \(E_s\) provient de l’achèvement des sections avec d’autres replis. Pour la référence \(v_0=(E,T,\Psi,E_s)\) et les réexécutions \(v_i\),

\[
d_i=\tfrac14\|v_i-v_0\|_1,\quad
\Delta S=m^{-1}\sum_i d_i,\quad
\Lambda=\max_i d_i,
\tag{13}
\]

les deux sorties étant nulles lorsqu’aucune réexécution n’existe. L’enveloppe répète la charge de travail sans modification explicite de la graine de perturbation. Son consommateur inspecté orienté texte n’utilise pas le texte pour construire la mesure du banc d’essai. Ce sont des valeurs de banc d’essai et d’audit associées à une piste, non des mesures démontrées de la qualité sémantique de ce candidat. Les champs numériques mixtes des CSV ne sont pas normalisés en unités physiques. [I11]

Le potentiel de navigation est

\[
P=3\Psi+1.5E+1.5T+1.2E_s-2\Delta S-\Lambda+2b_{diversity}.
\tag{14}
\]

Un rapport d’intégrité distinct divise la moyenne historique de Ψ multipliée par les derniers T et \(E_s\) par la variance d’échantillon des \(\Delta S\) historiques, le Λ historique maximal, une pénalité de contradiction et \(10^{-6}\). Il est non borné et peut croître parce que son dénominateur est petit. Les étiquettes de cycle de vie suivent des seuils ordonnés, et l’appelant inspecté n’exclut que les pistes élaguées. Les historiques de pistes JSON ne constituent ni un graphe durable de dépendances entre assertions ni un mécanisme d’effacement pour la confidentialité. [I11]

### 8.3 Familles de séries temporelles et de phases

Les variantes historiques de séries temporelles normalisent les différences, puis calculent la moyenne, l’écart-type de population, la moyenne des changements absolus adjacents, le rapport strict d’inversions de signe et le flux net. La somme des différences successives se télescope en \(s_n-s_1\). Aucun diviseur de temps écoulé n’apparaît ; ce sont donc des changements par échantillon plutôt que des dérivées par seconde. Les variantes ultérieures modifient le prétraitement et ajoutent des constantes de domaine déclarées ; leurs sorties ne doivent pas réétiqueter rétroactivement les exécutions antérieures. Pour une source discrète, l’entropie de Shannon est l’opposé de l’espérance de la log-probabilité sous un modèle probabiliste et une base logarithmique déclarés. Un écart-type ou un changement entre extrémités n’acquiert pas cette signification par le nom d’une variable. [I11]. [Shannon 1948](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf).

Une proposition de domaine donneur fondée sur les formes d’onde définit trois diagnostics pondérés par la phase,

\[
C^+=\Psi(1+\cos\Delta\phi)/2,\quad
C^-=\Psi(1-\cos\Delta\phi)/2,\quad
Q_\perp=\Psi\sin^2\Delta\phi.
\tag{15}
\]

Les diagnostics héritent des unités du Ψ sélectionné. Bien que \(C^++C^-=\Psi\), \(Q_\perp\) est un diagnostic distinct, non une troisième part additive d’énergie. Une interprétation en puissance physique exigerait un modèle de signal et un intervalle de moyennage spécifiés. Pour des fréquences fixes, la différence de phase varie à \(2\pi(f_2-f_1)\). Appliquer de telles relations à la traduction cognitive ou à l’investigation itérative est une analogie déclarée séparément. Cette famille de donneurs n’est pas le codec synthétique de référence de l’équation (9), et une cohérence élevée ou un verrouillage de phase ne suffisent pas à impliquer un bénéfice constructif ni une permission d’agir. [I11]

### 8.4 Un donneur à annulation cohérente et une hypothèse cible testable

Considérons les signaux donneurs analytiques \(x_1(t)=A\sin(\omega t)\) et \(x_2(t)=A\sin(\omega t+\pi)\), avec la même amplitude constante \(A>0\), une pulsation non nulle \(\omega\) et une relation de phase fixe. Leur somme est identiquement nulle bien que chaque signal soit non nul et que la phase relative soit stable. Sur un nombre entier de périodes, chacun a un carré moyen de \(A^2/2\), tandis que la somme a un carré moyen nul. C’est une identité exacte de signaux idéalisés, non une nouvelle expérience de forme d’onde, une affirmation de conservation de l’énergie physique ou un résultat sur la cognition. Dans le diagnostic donneur avec un \(\Psi>0\) choisi, l’opposition de phase donne \(C^+=0,C^-=\Psi,Q_\perp=0\). La structure peut donc rester spécifiée lorsqu’un agrégat observé s’annule. [I11]

L’hypothèse cible proposée est plus étroite : préserver une objection bien étayée et sa relation avec un candidat peut réduire l’accord superficiel tout en améliorant l’adéquation probatoire évaluée indépendamment. Un test figerait avant l’évaluation les populations sources, les tâches cibles, les objections et les budgets ; comparerait un traitement préservant explicitement les relations à une présentation appariée du même matériau sans carte relationnelle ; et masquerait la condition aux évaluateurs. Des critères de résultat définis séparément mesureraient l’appui factuel, le désaccord substantiel préservé, les assertions non étayées et la charge de révision. Une absence d’amélioration de l’appui définie à l’avance, ou une augmentation des assertions non étayées au budget indiqué, irait à l’encontre du bénéfice cible revendiqué. L’accord seul n’est pas le résultat recherché. Il s’agit d’un plan de test de classe H/P sans résultat cible : l’algèbre du donneur n’établit pas l’adéquation de l’analogie. [I09, I11, I13]

## 9 Corridors rivières terrasses et conséquences numériques

### 9.1 Spécification de recherche et implémentation réduite

La spécification de recherche des champs sur graphes distingue la densité de corridor C, la densité de rivière R, la densité de terrasse \(T^{terr}\), le potentiel Θ, la mémoire M et les termes d’instabilité. Elle définit

\[
F_{ij}=w_{ij}\frac{C_i+C_j}{2}(\Theta_j-\Theta_i),\qquad
A_i=\frac{|\sum_jF_{ij}|}{\sum_j|F_{ij}|+\varepsilon},
\tag{16}
\]

et une loi d’évolution de rivière de la forme

\[
\dot R_i=D_R\sum_jw_{ij}(R_j-R_i)
-\operatorname{div}_G(R\nabla_G\Theta)_i
+C_iA_i(\alpha_R+\beta_RM_i)-\mu_RR_i
-\nu_R([\Delta S_i]_++[\Lambda_i]_+)R_i-\chi_RR_i^3.
\tag{17}
\]

Une loi de terrasse ajoute une diffusion transportée, une source de rivière pondérée par la stabilité, un appui de mémoire/cohérence, une perte et une saturation cubique. Ces équations préservent les intentions de conception d’exploration, d’accumulation et de stabilisation provisoire. Elles exigent une orientation explicite du graphe, une discrétisation, des conditions aux limites, des unités de coefficients, des définitions d’estimateurs et une sémantique d’admissibilité avant que des assertions numériques ou scientifiques puissent en découler. La borne \(0\le A_i<1\), pour des entrées finies et un ε positif, est une conséquence arithmétique de l’inégalité triangulaire, non une validation de « l’accord ». [I12]

Le noyau réduit inspecté est sensiblement plus simple. Pour une liste d’arêtes non orientées de poids w, il calcule

\[
(LR)_i=\sum_jw_{ij}(R_j-R_i),\quad
g_i=\frac{\sum_jw_{ij}(\Psi_j-\Psi_i)^2}{\sum_jw_{ij}},
\tag{18}
\]

avec g fixé à zéro lorsque le dénominateur est non positif, puis

\[
R_i^{n+1}=\operatorname{clip}_{01}
\{R_i^n+h[D_r(LR^n)_i+\alpha g_i-\beta R_i^n]\}.
\tag{19}
\]

Les valeurs par défaut du noyau sont \(h=.05,D_r=.08,\alpha=.6,\beta=.1\), avec écrêtage facultatif. L’appelant d’évolution inspecté fournit explicitement **h=1.0**. Il appelle ensuite la mise à jour réduite de terrasse avec le même pas,

\[
T_i^{n+1}=\operatorname{clip}_{01}
\{T_i^n+h(\kappa R_i^{n+1}-\mu g_i-\nu T_i^n)\},
\tag{20}
\]

dont les valeurs par défaut du noyau comprennent \(h=.1,\kappa=.15,\mu=.10,\nu=.03\). Dans cet appelant, la phase de terrasse consomme le champ de rivière nouvellement mis à jour et écrêté \(R^{n+1}\) ; elle recalcule g à partir du champ Ψ, inchangé entre ces phases. Il s’agit d’une mise à jour séquentielle, non d’une mise à jour simultanée à partir de l’ancien état. Aucune des deux équations n’implémente tous les termes de transport, de mémoire et cubiques de la spécification plus complète. Une passerelle heuristique produisant des rivières nommées est encore un autre producteur, non une discrétisation de l’équation (17). [I12]

### 9.2 Stabilité au pas effectif de l’appelant

Les déductions suivantes supposent des poids non orientés finis et non négatifs, un Ψ fixe, \(D_r\ge0\), \(\beta>0\) et l’absence d’écrêtage. Soit \(L_+\) le laplacien positif du graphe, de sorte que \(L=-L_+\). Alors

\[
\dot R=-(D_rL_++\beta I)R+\alpha g,
\qquad R_* =\alpha(D_rL_++\beta I)^{-1}g.
\tag{21}
\]

Dans un mode propre de valeur propre laplacienne \(\lambda_k\), Euler explicite multiplie l’erreur par \(1-h(D_r\lambda_k+\beta)\). Le disque standard de stabilité d’Euler explicite fournit le cadre ; son application à cette équation du code source donne la condition de décroissance stricte

\[
0<h<\frac{2}{D_r\lambda_{max}+\beta}.
\tag{22}
\]

[Driscoll and Braun on absolute stability](https://fncbook.com/absstab-diffusion/).

Avec h=1 effectif et les coefficients par défaut, l’équation (22) exige \(\lambda_{max}<23.75\). La valeur par défaut h=.05 du noyau exige au contraire \(\lambda_{max}<498.75\). Pour R initial non négatif et un forçage non négatif \(\alpha g\), comme avec les valeurs par défaut indiquées, une condition suffisante de positivité coefficient par coefficient est \(h(D_rd_i+\beta)\le1\) pour tout degré pondéré \(d_i\), donnant \(d_i\le11.25\) à h=1. La positivité et la décroissance spectrale stricte sont des propriétés différentes. Aucune n’établit une borne supérieure de un sans conditions supplémentaires sur le forçage. [D from I12]

Un contre-exemple exact à la stabilité universelle utilise un graphe hypothétique à deux nœuds avec une arête de poids 20 et des Ψ fixes égaux, de sorte que \(g=0\) et \(\lambda_{max}=40\). Le multiplicateur du mode de différence est \(-2.3\) à h=1, contre .835 à h=.05. Avec écrêtage, partons de \(R^0=(1,0)\). L’état suivant non projeté est \((-.7,1.6)\), la projection donne donc \((0,1)\) ; le pas suivant retourne à \((1,0)\). Le caractère borné coexiste avec une orbite exacte de période deux dans ce noyau isolé à entrée fixe. C’est un exemple construit algébriquement, non un test exécuté ni une affirmation concernant un graphe réellement déployé.

Sans écrêtage, sommer l’équation (21) annule la diffusion symétrique et donne

\[
\frac{d}{dt}\sum_iR_i=\alpha\sum_i g_i-\beta\sum_iR_i.
\tag{23}
\]

La densité de rivière n’est généralement pas conservée. L’écrêtage apporte une correction de projection. Une mise à l’échelle uniforme des poids modifie la raideur de diffusion tout en laissant g normalisé inchangé pour un facteur positif. Des arêtes miroirs dupliquées peuvent également modifier l’accumulation. Une évaluation numérique valide doit conserver l’identité du graphe, les poids, le pas, les incréments avant projection et les résidus de projection. Aucun spectre de graphe réel ni aucune exécution dans cette étude n’établit que l’appelant de production était instable. [I12]

### 9.3 Investigation récursive et régimes de représentation

La récursion maîtresse de recherche est

\[
X_{n+1}=\mathcal M\circ\mathcal S\circ\mathcal R(X_n),
\tag{24}
\]

où l’entrée réceptive, la structuration et la continuité/métabolisme agissent sur l’état évolutif de la tâche. Ces passes fonctionnelles ne s’identifient pas une à une à trois composants nommés ni à trois modèles fixes. L’état peut conserver des hypothèses, des contradictions, un budget et des tests inachevés ; répéter un prompt ne suffit pas à établir un perfectionnement. [I12]

Une proposition réduite d’état complexe utilise \(Z_n=\Psi_n+iK_n\) et \(Z_{n+1}=\rho_ne^{i\theta_n}Z_n+\eta_n\). Pour \(a=\rho e^{i\theta}\ne1\) constant et η constant, \(Z_*=\eta/(1-a)\) et \(Z_n-Z_*=a^n(Z_0-Z_*)\). Ainsi, \(|\rho|<1\) contracte les perturbations ; \(|\rho|>1\) les amplifie génériquement. Pour \(|a_n|\le r<1\) et un forçage borné \(|\eta_n|\le B\),

\[
|Z_n|\le r^n|Z_0|+B(1-r^n)/(1-r).
\tag{25}
\]

Cette borne ne garantit pas la convergence vers une valeur unique, et la rotation peut déplacer la coordonnée réelle hors de [0,1]. Appeler un régime rivière ou terrasse ne résout pas ces questions mathématiques. Un champ vectoriel plat n’est pas un équilibre tant que la condition définissante de point fixe ou de dérivée nulle n’est pas satisfaite. [I12]

Les formules écologiques plus générales reliant transfert, ramification, capture, pluralité et renouvellement restent des définitions de classe H. Leurs types scalaires ou vectoriels non résolus, les domaines de leurs dénominateurs et leurs estimateurs empiriques constituent un travail de recherche substantiel. Les dérivations écologiques plus complètes et leur opérationnalisation restent hors de l’analyse détaillée de cet article ; ces propositions formelles ne sont pas toutes des hypothèses empiriques prêtes à être testées. Elles ne servent pas ici à noter des personnes ou des institutions. Préserver les hypothèses avec leurs conditions manquantes est plus fidèle que de les déclarer lois établies ou de les effacer comme simple langage décoratif.

## 10 AHA et transformations explicites entre domaines

Un cas AHA fourni contient deux à cinq graphes donneurs, un graphe cible, des correspondances de nœuds, relations et invariants, des disanalogies, des transformations d’unités et d’échelle déclarées, un observable cible, un comparateur ou une hypothèse nulle, un horizon, une observation abaissant la confiance et une déclaration de réfutation. L’enveloppe native exige l’ensemble exact de références aux segments et empreintes d’ancrage. Le moteur inspecté vérifie l’existence, le type, l’orientation et les paires d’extrémités mises en correspondance des relations déclarées. Les relations donneuses non mises en correspondance restent visibles. Les identifiants de familles de sources déclarées en double sont rejetés, mais des étiquettes différentes ne suffisent pas à établir des origines indépendantes. [I09]

Soient les structures donneuse et cible \(G_D=(V_D,E_D)\) et \(G_T=(V_T,E_T)\), avec l’application de nœuds fournie \(\phi\). Une relation vérifiée \((u,r,v)\in E_D\) est structurellement préservée lorsque la relation cible requise \((\phi(u),r',\phi(v))\in E_T\) existe sous la transformation de relation déclarée. Dans le moteur actuel, les types et orientations des relations mises en correspondance doivent coïncider exactement ; la carte de relations fournie associe des identifiants et n’exécute pas de transformation sémantique ou d’unités. La notation affichée de r vers r′ est une généralisation conceptuelle dont le cas particulier implémenté exige cette égalité. Savoir si les relations décrivent des mécanismes causaux comparables relève d’une assertion scientifique supplémentaire. La théorie de la mise en correspondance structurelle fait de la préservation des relations un objet d’investigation fondé ; elle ne certifie pas un transfert particulier du donneur vers la cible. [Gentner 1983](https://groups.psych.northwestern.edu/gentner/papers/Gentner83.2b.pdf).

Les sorties effectives restent typées : \(P_{epi}\) est un statut probatoire ordinal NOT_SCORABLE ; \(C_{bridge}\) contient les constats sur les composants structurels ; \(V_{test}\) fournit des informations qualitatives de valeur informationnelle, de faisabilité et de risque, avec un coût non fourni ; \(Q_{AHA}\) est un rang d’attention fixé à un, explicitement non probabiliste. Plusieurs valeurs PASS résultent de déclarations acceptées ou de contrôles structurels, non d’expériences cibles observées. L’enveloppe étiquette la couverture des références de filiation et fixe à false l’évaluation de la non-vacuité sémantique et la démonstration d’utilité sémantique. [I09]

L’absence de cas fourni signifie UNAVAILABLE. La réponse de six octets de l’exemple témoin ne crée pas spontanément de graphes donneurs, ne découvre pas de correspondance et n’exécute pas de test de réfutation. REVIEWABLE signifie qu’un cas peut être inspecté. Cela n’établit ni découverte, ni corroboration, ni adoption. La découverte automatique de donneurs, le retour d’AHA vers le fournisseur et la réfutation exécutée sur la cible restent des articulations non résolues dans le parcours maintenu inspecté. Une proposition évoluant séparément ou un ensemble expérimental testé doit rester distinct du statut d’implémentation acceptée. [I09, I20]

Le rôle constructif des quantités partagées consiste donc à guider la récupération ou l’attention : des diagnostics semblables peuvent suggérer l’examen d’une branche. Un pont admissible doit encore identifier la relation, les unités natives, la transformation, les exceptions et un réfutateur possible. L’égalité numérique seule ne peut pas déterminer quelle relation sémantique se transfère. Cela préserve la découverte latérale comme objectif de recherche sans transformer une correspondance de coordonnées en preuve.

### 10.1 Une spirale de découverte à partir de preuves non résolues

Dans le programme de recherche Waters of Gnosis, une condition non résolue peut désigner une direction inexplorée autant qu’une limitation. Une incertitude non mesurée peut révéler une observation absente ; des preuves contradictoires peuvent distinguer des explications concurrentes ; une inadéquation gênante entre donneur et cible peut faire apparaître une relation méritant d’être formulée. L’objectif constructif est la découverte innovante et de nouveaux candidats AHA, en préservant l’incertitude originale plutôt qu’en la convertissant en confiance. Une valeur inconnue ne prouve pas que le candidat est faux, et un désaccord ne suffit pas à prouver qu’un côté ou l’autre a tort. Ni l’un ni l’autre ne prouve à lui seul la nouveauté. [I09, I12, I15]

La spirale proposée rend cet objectif opérationnel dans le vocabulaire original des eaux de la connaissance. Un **corridor** consigne une alternative ou une question bornée. Un **affluent** fournit une observation ciblée, une calibration, une réparation ou une source contrastante. Une **rivière** consigne une ligne d’investigation en développement au fil des itérations. Le **tressage** maintient reliés les relations complémentaires et les désaccords substantiels tout en préservant leur filiation distincte ; il ne les moyenne pas en un accord forcé. Une **terrasse** représente un appui provisoire dans un périmètre déclaré, et la **rupture ou réouverture** réexamine cet appui lorsque de nouvelles observations en fragilisent les conditions. Ce sont des fonctions d’investigation qui peuvent s’exprimer par les rôles existants de l’atelier et les cas AHA fournis ; cet article n’exige pas de nouveaux composants obligatoires et ne les identifie pas à un écoulement physique. [I12, I13, I15]

Une séquence bornée proposée consiste à conserver la condition non résolue et sa base probatoire ; à laisser l’utilisateur choisir une question, des sources permises et un budget d’exploration ; à formuler des relations alternatives ou des correspondances donneuses candidates ; à mettre à l’épreuve les hypothèses précises qui les distinguent ; puis à retourner un nouveau candidat, le désaccord préservé et la prochaine observation discriminante. Une exploration réussie peut révéler une relation jusque-là non formulée, alors même que le candidat original reste en attente. Elle peut au contraire établir qu’un corridor est peu étayé. Ce sont des résultats utiles différents. L’état d’exploration doit donc suivre les candidats de découverte séparément des résultats validés et de la permission d’agir. [I09, I12, I13, I20]

Il s’agit d’une intégration et d’un plan de test de classe P/H, non d’une boucle automatique de rétroaction actuelle. La règle ordinaire de refus JOINED reste inchangée. Un résultat en attente ne déclenche pas de nouveaux appels, n’autorise pas de nouveaux destinataires et ne transforme pas une carte structurelle fournie en preuve. L’utilisateur garde le contrôle sur la décision d’explorer, la branche à suivre et le moment d’arrêter ; chaque opération lourde de conséquences exige toujours l’autorité applicable qui lui est propre. Une évaluation appariée pourrait comparer une spirale guidée par les résidus à une clarification ordinaire sous les mêmes données et le même budget, en utilisant des évaluations séparées des nouvelles hypothèses utiles, des relations nouvellement étayées, du désaccord conservé et de la charge de révision. La seule nouveauté de formulation, l’augmentation du nombre de sorties ou de l’accord n’établiraient pas le bénéfice proposé. [I07, I13, I15, I20]

## 11 Opérateurs de perturbation et changement cognitif

Le terme perturbation devrait identifier un opérateur, les invariants préservés et une cible d’observation. Au moins six opérations différentes se présentent dans l’espace de conception :

| Famille d’opérateurs | Objet modifié | Relation préservée ou testée | Frontière probatoire actuelle |
|---|---|---|---|
| Normalisation du texte | Fins de ligne, espaces aux extrémités, représentation Unicode | Identité originale conservée séparément ; coordonnées normalisées reconstruites | Transformation implémentée ; préservation sémantique générale non prouvée |
| Enveloppement du contexte | Messages effectifs et contexte antérieur sélectionné | Liaisons exactes parent/tâche/source | Chemin implémenté ; effets au niveau des jetons non observés |
| Mise à l’épreuve du candidat | Assertions, objections ou alternatives fournies | Filiation de même racine et réponse explicite à la contestation | Structure locale d’atelier ; corroboration indépendante non impliquée |
| Perturbation numérique | Coefficients, entrées, graphe ou conditions initiales | Sensibilité, résidus, stabilité sous une norme spécifiée | Les réexécutions historiques manquent souvent de perturbation contrôlée ; cet article ne dérive que des conditions |
| Correspondance analogique | Interprétation du domaine et correspondance relationnelle | Relations déclarées, transformations d’unités, disanalogies | Contrôles structurels de cas fournis ; adéquation cible non établie |
| Correction ou révocation | Version, usage permis ou admissibilité des dépendances | Observation historique séparée de la permission présente | Des contrôles bornés existent ; propagation universelle à l’échelle du graphe non établie |

Cette taxonomie est une synthèse analytique des mécanismes et propositions inspectés, non une affirmation selon laquelle un orchestrateur unique invoque déjà les six. Chaque opérateur peut produire un nouveau candidat utile, un refus, un résidu, une demande de preuves ou un périmètre réduit. Le progrès cognitif ne peut pas être inféré de la seule ampleur du changement ou d’un désaccord réduit. Une réponse erronée stable reste erronée ; la diversité sans pertinence n’est pas une exploration utile. [I05, I11–I16]

Pour une expérience contrôlée proposée, soit \(T_\delta\) une perturbation déclarée et \(F\) le parcours borné d’évaluation. On ne peut étudier \(F(T_\delta x)-F(x)\) qu’après avoir spécifié la représentation de sortie, la norme, les δ admissibles, les contrôles appariés et les observations disponibles. Comparer des espaces de noms scalaires sans rapport rend cette différence indéfinie en tant que mesure. Cette formulation est un protocole de recherche, non une expérience cachée réalisée par l’architecture.

## 12 Atelier local et essaim distribué

### 12.1 Rôles et dépendance

L’atelier local Analyst→Challenge→Synthesis lie des artefacts antérieurs sélectionnés de même racine, des versions de sources et de contrôles, ainsi qu’une sélection explicite. La synthèse doit préserver les accords substantiels, les désaccords et les contestations non résolues plutôt que de traiter le consensus des rôles comme une vérité. Les boucles historiques effectuant trois ou sept appels à un même modèle avec des prompts différents montrent une diversité de prompts et un échantillonnage répété ; elles n’établissent pas une cognition distribuée indépendante. Des noms de rôles distincts, et même des modèles distincts, ne peuvent à eux seuls prouver l’indépendance des preuves. [I13]

Pour illustrer l’importance de cette distinction, supposons que des erreurs de même variance aient pour variance \(\sigma^2\) et pour corrélation commune par paires r, avec une matrice de covariance semi-définie positive admissible. Alors

\[
\operatorname{Var}(\bar\epsilon)
=\frac{\sigma^2}{m}[1+(m-1)r],\qquad
m_{eff}=\frac{m}{1+(m-1)r}.
\tag{26}
\]

La taille effective d’échantillon affichée suppose un dénominateur positif ; sa frontière singulière de variance nulle ne reçoit pas de valeur finie. Pour des poids généraux w et une covariance Σ, la variance vaut \(w^\top\Sigma w\). Ce sont des déductions explicatives, non des estimateurs de confiance implémentés. Un entraînement commun, l’exposition aux mêmes sources et la consultation d’une réponse antérieure peuvent créer une dépendance. Ni l’accord verbal ni les étiquettes de modèles ne mesurent r. Les gains de bancs d’essai rapportés pour le débat multiagent motivent des expériences contrôlées, mais n’impliquent pas que davantage d’agents ou de tours améliorent universellement les résultats. [I13]. [Du et al 2024](https://proceedings.mlr.press/v235/du24e.html).

N éléments de travail avec une concurrence c ne sont pas N travailleurs simultanés. Toutes les comparaisons de paires ordonnées coûtent \(N(N-1)\) avant les tours. Un événement utilisateur avec N enfants analytiques constitue un événement source et N tâches, non N+1 observations indépendantes. Un atelier qualifié a donc besoin du dénominateur : tâches tentées, échouées, périmées, annulées et non résolues, ainsi que sorties acceptées. Des contestations ciblées d’hypothèses distinctes peuvent être préférables à des échanges illimités de tous avec tous. Ce sont des conséquences de conception, non des affirmations mesurées de vitesse ou de qualité. [I13]

### 12.2 Transfert d’artefacts et interfaces de modèles entre pairs

Un transfert borné d’artefacts entre pairs existe sous la forme d’une liaison authentifiée avec rattachement exact archive/référence/offre, appairage accepté, autorisation courante, échéance originale, TLS et vérification sous la responsabilité du destinataire. Les références d’empreinte émises par le dispositif de conservation hors d’une archive ne sont pas des signatures. Un paquet dont les octets sont vérifiés peut encore contenir une affirmation fausse, et un rôle de vérificateur authentifié séparément n’implique pas une corroboration indépendante par modèle. [I14]

Des contrats d’expéditeur, de récepteur et de requête/statut/résultat de modèle entre pairs existent aussi. Le code source inspecté contient un envoi à tentative unique désactivé par défaut, une réception désactivée par défaut, une projection de l’autorisation courante et des points d’intégration natifs à la conservation. Les bornes incluent des trames canoniques de requête/statut/résultat d’au plus 65,536 octets, des fenêtres originales de tâches d’au plus 120,000 millisecondes, des limites de sortie déclarées d’au plus 4,096 jetons et un texte retourné d’au plus 32,768 octets UTF-8 ; l’enveloppe de résultat possède sa propre borne de trame. Le récepteur exige un authentificateur injecté. L’exécution exige un responsable natif injecté séparément qui vérifie la politique courante, l’horloge de confiance, la responsabilité des ressources et la réservation transactionnelle. L’ancienne admission peut conserver un reçu en attente sans ce responsable, tandis que l’admission structurée rejette l’admission sans responsable ; aucune issue d’admission ne fournit une autorité d’exécution. Un objet ayant la forme d’une autorisation dans une charge utile ne peut pas s’accorder lui-même une autorité. [I14]

Cependant, la liste d’autorisation du transport appairé maintenu inspectée pour cette étude achemine la réception, la vérification et l’annulation d’artefacts, non les tâches de modèles entre pairs. Aucune construction en production du récepteur de modèles ni invocation de l’expéditeur n’a été établie dans l’ensemble clos sélectionné. Les preuves étayent de véritables interfaces d’implémentation bornées, accompagnées d’articulations de bout en bout manquantes. Elles n’étayent pas un essaim cognitif qualifié à trois nœuds en fonctionnement. Un pilote à trois nœuds demeure proposé ou partiellement implémenté tant que les preuves de transport, de responsable, d’autorisation, de conservation et de consommation du résultat de chaque liaison ne sont pas établies. La connectivité et la permission ne sont pas transitives. [I14, I20]

La conservation des éléments Challenge externes et les consommateurs locaux de synthèse préservent les références exactes aux charges utiles tout en séparant les observations de livraison. Les droits courants d’utilisation et de partage sont revérifiés indépendamment de l’achèvement historique. L’expiration d’une autorisation d’exécution ne prouve pas que la tâche antérieure n’a pas été exécutée et ne règle pas automatiquement toute inspection historique autorisée séparément. Cette distinction est nécessaire à la fois pour une provenance exacte et une réutilisation bornée. [I14]

## 13 Télémétrie provenance et confiance

### 13.1 Trois domaines d’observation différents

La conservation sous contrôle, le TEL natif et l’observation de la charge des actions répondent à des questions différentes. Les événements de conservation hachent un tuple canonique comprenant l’identité de l’enregistrement, son type, l’acteur, l’heure, les détails et l’empreinte précédente. Une séquence de base de données ordonne les événements locaux mais n’est pas incluse dans cette empreinte. Des déclencheurs en ajout seul restreignent les opérations normales de mise à jour et de suppression sous le schéma ; un administrateur privilégié de la base ou de l’hôte reste une dépendance de confiance. La chaîne rend les altérations détectables relativement à une vue conservée de confiance, mais n’est pas un registre horodaté indépendamment, attesté mondialement ou cohérent face aux fautes byzantines. [I16]

Le TEL natif consigne un ordre déterministe des étapes et des liaisons d’artefacts. Le cœur produit 15 événements pré-audit et s’arrête avant Sophia/Atlas. L’achèvement vérifié de l’audit et de l’orientation externes produit 18 lignes de parcours, et une décision humaine ultérieure constitue une continuation distincte liant le parent scellé. Les étiquettes logiques telles que T+000001 sont des identifiants de séquence, non des secondes écoulées ni des horloges causales interhôtes. L’analyse d’ordre partiel de Lamport explique pourquoi la causalité distribuée ne peut pas être inférée de simples horodatages apparemment comparables. Aucune implémentation d’horloge de Lamport n’est affirmée ici. [I16]. [Lamport 1978](https://lamport.azurewebsites.net/pubs/time-clocks.pdf).

Le module terminal TAF-A inspecté authentifie une capture parent conservée et rapporte les octets logiques conservés de la réponse fournisseur. Son unité est l’octet ; une donnée manquante est UNAVAILABLE, non zéro. Quinze anciens termes diagnostiques et les agrégats d’action totale restent indisponibles. Il ne mesure ni l’énergie en joules, ni les FLOPs, ni la mémoire du dispositif, ni le coût des options futures, ni la charge éthique du système entier. Son profil de sérialisation diffère aussi du JSON natif à LF final, renforçant la nécessité d’énoncer le domaine de hachage. [I16]

### 13.2 Composer la provenance ne compose pas la vérité

Un graphe conceptuel de provenance peut utiliser des entités pour les octets et les évaluations, des activités pour les transformations et des agents pour les producteurs ou réviseurs responsables. Cela correspond au sujet de PROV-DM sans revendiquer une conformité d’implémentation. [PROV](https://www.w3.org/TR/prov-dm/).

Pour un résultat y, distinguons six prédicats :

\[
\operatorname{BytesMatch}(y),\quad
\operatorname{SenderAuthenticated}(y),\quad
\operatorname{LineageBound}(y),\quad
\operatorname{ProcedureObserved}(y),\quad
\operatorname{EvidenceAdequate}(y,q),\quad
\operatorname{UsePermitted}(y,p,r,t).
\tag{27}
\]

Le dernier prédicat dépend de la finalité p, du destinataire r et du temps t. Aucun de ces prédicats n’implique tous les suivants. Leur conjonction peut être nécessaire pour un usage particulier, mais ce n’est pas un théorème universel de vérité. L’intégrité des sources, l’interprétation et l’autorité d’action ont des responsables et des modes de défaillance différents. [I03, I10, I14, I16]

Des preuves répliquées ne constituent pas automatiquement un consensus sur un journal répliqué. Raft traite de l’accord sur l’état d’un journal sous un protocole spécifié, non de l’accord sur la vérité scientifique. De même, Certificate Transparency spécifie des preuves d’inclusion et de cohérence et traite des vues incohérentes ; une chaîne locale d’empreintes n’est pas pour autant un service de transparence attesté mondialement. Ce sont des classes de contraste, non des composants revendiqués. [Ongaro and Ousterhout 2014](https://www.usenix.org/conference/atc14/technical-sessions/presentation/ongaro), [RFC 9162](https://www.rfc-editor.org/rfc/rfc9162.html).

## 14 Grammaire partagée et reconstruction rétrospective

### 14.1 Communication par références avec résidus

La grammaire partagée envisagée permet une référence compacte à une structure préalablement établie, versionnée et permise. Un parcours défendable du destinataire consiste à résoudre la référence ; vérifier la définition et sa version ainsi que les permissions des dépendances ; comparer le domaine et les unités ; développer les exceptions et les résidus ; puis n’accepter que l’interprétation bornée étayée ou refuser la correspondance. Il s’agit d’un contrat de conception pour un contexte partagé, non d’une preuve d’expérience subjective partagée. [I15]

Le coût de communication doit inclure la distribution et la synchronisation de la bibliothèque partagée, les octets de référence, les résidus, la provenance, la recherche, le développement, la vérification et les corrections. Une formule courte n’est pas un résultat complet de compression. La théorie du codage de Shannon fournit un cadre formel de communication ; elle n’assimile pas les codes courts à la vérité sémantique ou à l’utilité cognitive. [Shannon 1948](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf).

Les mécanismes historiques retrouvés comprennent un dictionnaire versionné avec des liaisons aux éléments d’appui, des enregistrements de transformation préservant les domaines et les unités, et une reconstruction par copie d’octets et résidus avec comptabilisation explicite des coûts. Ils n’établissent pas l’apprentissage automatique actuel d’une grammaire, la récupération GUFT par plus proches voisins, le transfert sémantique sans perte ou la négociation inter-nœuds du développement des références. Une comparaison finie avec des antécédents fournis constitue un module terminal utile côté réception, non le constructeur de bibliothèque complet. Le module terminal de comparaison pure inspecté n’a ni appelant de production établi dans l’ensemble clos sélectionné ni émetteur d’autorité. [I15]

### 14.2 Rétrosynthèse comme reconstruction guidée par les dépendances

Ici, la rétrosynthèse consiste à remonter d’un résultat souhaité ou produit vers les transformations et les appuis nécessaires pour le justifier ou le reproduire. C’est une description analytique d’un parcours utile de provenance, non une affirmation selon laquelle un moteur général de raisonnement inverse est déjà implémenté. Soit \(f_y=\operatorname{pr}_y\circ f\) la projection de sortie de la transformation à valeurs tuples de l’équation (1), le contrat de preuve et de statut étant fixé séparément. Pour \(y=f_y(x,\kappa,\pi)\), définissons l’ensemble des prédécesseurs admissibles

\[
\operatorname{Pre}(y)=\{(x,\kappa,\pi):f_y(x,\kappa,\pi)=y
\text{ under the declared identity and status contract}\}.
\tag{28}
\]

Pour une normalisation plusieurs-à-un, Pre peut contenir plusieurs historiques d’octets. Une référence d’empreinte accompagnée d’un original indisponible ne peut pas restaurer ces historiques. Pour une inférence stochastique ou opaque, reproduire la sortie exacte peut en outre exiger un état d’exécution non observé. Le résultat rétrospectif honnête peut donc être « identité consignée, charge utile indisponible », « recalcul structurel disponible » ou « inférence d’exécution non reproductible », plutôt qu’une relecture intégrale inventée. [I04, I06, I15]

Pour une assertion q, soit \(\mathcal S(q)\) la famille contenant les ensembles alternatifs d’appui déclarés adéquats et non vides, selon une méthode et un périmètre choisis. L’adéquation est un jugement scientifique distinct au niveau des ensembles, non quelque chose que créent les contrôles de disponibilité et de permission ci-dessous. La finalité p, le destinataire r et le temps t étant explicites, une condition explicative d’utilisation présente est

\[
\operatorname{SupportUsable}(q,p,r,t)
=\bigvee_{S\in\mathcal S(q)}\ \bigwedge_{e\in S}
\left[\operatorname{Available}(e,t)\land
\operatorname{UsePermitted}(e,p,r,t)\land
\operatorname{MethodApplicable}(e,q)\right].
\tag{29}
\]

Une famille vide \(\mathcal S(q)=\varnothing\) donne false, et les membres vides sont exclus ; un théorème logique sans preuves empiriques exigerait sa propre justification déclarée plutôt qu’un appui accidentellement vrai par vacuité. L’équation (29) propose une sémantique des dépendances, non un évaluateur global implémenté. Elle montre pourquoi la perte d’une source ne réfute pas nécessairement q lorsque subsiste un appui indépendant adéquat, et pourquoi un enregistrement historique n’autorise pas automatiquement la réutilisation présente. Un moteur général de réouverture tenant compte des dépendances, un solveur d’ensembles minimaux de réparation et la propagation des révocations entre nœuds exigent encore une implémentation et une qualification. [I15, I20]

Le raisonnement rétrospectif peut néanmoins guider une sortie utile dès aujourd’hui : identifier le candidat exact et la version d’entrée, rendre visibles les contrôles réellement exécutés, préserver le désaccord, énumérer les preuves manquantes et formuler un prochain test borné. Un parcours qui retourne une demande de clarification mais n’exécute aucune réparation doit le dire. L’artefact devient un état d’atelier traçable plutôt qu’une affirmation que l’incertitude a disparu.

### 14.3 Réutilisation de la provenance et autonomie dans le travail partagé

L’hypothèse de recherche est qu’une réutilisation respectueuse des permissions d’un artefact étayé peut réduire les dérivations répétées à qualité acceptée et couverture comparables. Des origines, versions, cartes de dépendances et corrections identifiables peuvent aider les destinataires à évaluer ce qui peut être réutilisé. Des copies supplémentaires seules ne fournissent pas de preuves plus fortes ni de corroboration indépendante. La réutilisation reste soumise aux frontières d’autorité, de dépendance et de confidentialité des sections 12–15. [I13–I17]

Une comparaison proposée fixerait la même charge de tâches répétées, le même instantané des sources, les mêmes sorties requises, les mêmes conditions matérielles et d’exécution, les mêmes règles d’arrêt et le même horizon d’observation pour deux groupes. Le groupe de recalcul dérive à nouveau chaque résultat requis selon une politique déclarée. Le groupe de réutilisation résout un artefact antérieur, vérifie son identité, son appui, son applicabilité, sa fraîcheur et ses permissions, puis l’adapte avec des résidus consignés ou se replie sur le recalcul. Préenregistrer les critères d’acceptation et une marge de comparabilité de qualité ; utiliser une évaluation en aveugle lorsque c’est possible. Rapporter les sorties acceptées aux côtés des tâches tentées, rejetées, échouées, périmées, annulées et non résolues. Des économies à service équivalent exigent une qualité acceptée et une couverture comparables.

Pour chaque unité de ressource u, définissons la différence descriptive ΔC_u = C_recompute,u − C_reuse,u sur l’ensemble de cette charge de travail. Les deux totaux comprennent la production initiale attribuable, la récupération, la vérification, l’adaptation, le stockage et la réplication, le transport, la coordination, les tentatives échouées, les travaux de repli et les corrections ultérieures dans l’horizon déclaré. Comptabiliser chaque événement de ressource une seule fois, y compris le travail transféré aux pairs. Indiquer l’allocation des coûts de mise en place partagée et de stockage persistant ; distinguer les totaux à démarrage à froid des résultats avec cache chaud. Un ΔC_u positif désigne une économie uniquement dans l’unité et le périmètre mesurés, sous réserve de comparabilité de la qualité et de la couverture. [I15, I19, I20]

Rapporter le calcul en nombres d’opérations directement mesurés ou en secondes-dispositif caractérisées par le matériel, l’énergie en joules lorsqu’elle est instrumentée, le trafic en octets, l’occupation du stockage en octets-secondes, la latence écoulée en secondes et la révision humaine en personnes-minutes. Garder les dimensions séparées ; la latence écoulée n’est pas la somme du calcul parallèle. Les jetons, les appels et les octets de réponses conservées n’établissent ni des FLOPs, ni une énergie, ni des probabilités d’exactitude. Les mesures manquantes restent indisponibles. [I16]

L’autonomie pratique est un objectif de conception principal évalué séparément des économies de ressources : la capacité de quitter le système, de choisir un modèle ou un fournisseur, de conserver le contrôle local et de participer à une gouvernance coopérative responsable. Une étude devrait spécifier les capacités requises et évaluer si les participants peuvent les exercer, y compris les échecs et les obstacles. Les économies de ressources ne compensent pas la violation d’une exigence minimale déclarée en matière de droits, et les utilisateurs peuvent préférer une autonomie accrue malgré un coût supérieur. La décentralisation seule n’établit aucun de ces résultats. Il s’agit d’un engagement normatif de conception assorti de critères d’évaluation opérationnels, non d’un terme favorable ajouté à la différence de coûts. L’étude proposée n’a pas été exécutée ; aucun nouveau résultat d’efficacité ou d’autonomie n’est rapporté ici. [I19, I20]

## 15 Analyse de la sécurité de la confidentialité et des défaillances

Le modèle de menace comprend les instructions sources malveillantes, les artefacts mal formés, les affirmations d’identité forgées, les autorisations périmées, la livraison partielle, le rejeu, l’exécution en double, les erreurs de raisonnement corrélées, les noms trompeurs de métriques, la compromission d’un dépositaire privilégié et les copies non résolues hors du responsable local. Cet article évalue les frontières de conception, non la résistance aux attaques d’un produit installé.

| Défaillance ou menace | Frontière inspectée | Limitation résiduelle |
|---|---|---|
| Le texte source demande des actions privilégiées | Source traitée comme donnée ; acteur authentifié et autorité d’envoi distincte | Le cadrage du prompt seul ne prouve pas l’obéissance du modèle et n’élimine pas l’injection |
| Une charge utile modifiée réutilise une clé d’idempotence | Liaison exacte à la charge utile brute | Une issue antérieure incertaine exige toujours une réconciliation |
| Une réponse tronquée est dite complète | Longueurs et empreintes observées et conservées ; contrôles d’achèvement propres au fournisseur | L’exécution distante et l’accusé de réception local peuvent diverger |
| Une citation est prise pour une vérité | Reconstruction exacte des empans et empreintes ; statut de révision humaine | L’adéquation de la source, la vérité et l’implication sémantique restent distinctes |
| Les métriques compensent un échec de politique | Conditions Aperture non compensatoires | Les contrôles métier propres au profil peuvent être consultatifs |
| Un second rôle est compté comme preuve indépendante | Historique de même racine et identité explicite de contribution | La dépendance statistique n’est pas mesurée par les étiquettes |
| Une autorisation forgée autorise le travail d’un pair | Responsable authentifié injecté et contrôles de politique courante | Parcours de modèle de production de bout en bout non établi |
| Le journal local est qualifié de consensus immuable | Chaîne de hachage, schéma en ajout seul, inventaire scellé | L’hôte ou le dépositaire privilégié et l’observation externe restent des dépendances de confiance |
| Un ensemble raw-free est qualifié d’anonyme | Certains octets bruts exclus de l’entrée de révision | Les textes dérivés de source et de réponse peuvent rester identifiants |
| L’expiration de la charge utile est qualifiée d’effacement complet | Expiration des charges utiles à périmètre contrôlé et marqueurs de suppression | Les événements en ajout seul et les copies externes peuvent conserver du contenu |

[I03, I05–I10, I13–I17]

Ces contrôles n’établissent pas la confidentialité vis-à-vis d’un point de calcul autorisé ou d’un hôte local privilégié. Les chemins sélectionnés construisent des valeurs lisibles de source, de contexte et de requête et conservent des artefacts contenant du contenu ; TLS protège le transport entre points terminaux. Cette étude n’établit aucune garantie de calcul confidentiel ni de rétention distante vérifiée indépendamment et n’audite pas les protections de l’hôte sans rapport avec son périmètre. Le choix du parcours exige donc de décider que le destinataire et le périmètre des copies conservées sont appropriés aux données. [I06, I14, I17]

La dernière ligne est concrète. Certains BLOBs de conservation et fichiers dérivés peuvent expirer sous réserve de confirmation du dépositaire, d’une vérification des obligations de conservation légale et des évaluateurs actifs. Cependant, les événements de tentative en ajout seul peuvent contenir les octets originaux de requête, les événements de liaison contextuelle peuvent contenir les messages effectifs et les événements de validation de capture peuvent contenir le texte normalisé de réponse. La routine d’expiration inspectée ne supprime pas tous ces détails d’événements. Les exports, sauvegardes, fournisseurs et pairs ont des cycles de vie de copies distincts. Une affirmation d’effacement complet du contenu serait donc fausse pour le périmètre inspecté. [I17]

Les empreintes elles-mêmes peuvent permettre des rapprochements, en particulier pour des textes candidats de faible entropie. Un reçu raw-free constitue une frontière d’omission, non une désidentification. Un ensemble de révision peut préserver le contenu de source et de réponse tout en excluant les octets du corps fournisseur. L’analyse de confidentialité doit inventorier les copies porteuses de contenu et les responsables de l’autorité plutôt que de ne compter que les fichiers étiquetés bruts. Ces limites n’impliquent pas l’absence des contrôles existants de rôles, de rétention et d’envoi ; elles définissent ce que ces contrôles couvrent réellement. [I17]

Les valeurs par défaut à sûreté intégrée, le moindre privilège et la médiation complète restent des critères utiles : l’absence d’autorisation ne doit pas devenir une permission ; chaque usage doit être vérifié par le responsable compétent. Ils guident la révision sans prouver que tous les chemins d’implémentation les satisfont. [Saltzer and Schroeder 1975](https://web.mit.edu/Saltzer/www/publications/protection/Basic.html).

## 16 Programme de qualification de la recherche

Les prochaines preuves devraient fermer des articulations précises plutôt que maximiser le nombre d’étiquettes impressionnantes. Chaque proposition ci-dessous est de classe P et exige son propre périmètre autorisé ; aucune n’a été exécutée pour cet article.

1. **Expérience sur des représentations épinglées.** Utiliser une version permise du tokenizer, du gabarit et du moteur d’exécution ainsi que des jeux de test synthétiques comportant du texte multioctet, des variantes de normalisation et des tâches sensibles aux espaces. Conserver les octets exacts, les identifiants de jetons lorsqu’ils sont observables, les points de rejet et les contrats complets. Séparer la visibilité du tokenizer des calculs cachés du modèle.
2. **Calibration du filtrage.** Définir un producteur d’incertitude avec un événement cible et une population explicites. Évaluer la discrimination, la calibration, les compromis de refus et les cas défavorables sur des tâches tenues à l’écart. Comparer au parcours prudent actuel sans modifier un seuil uniquement pour augmenter le taux de réussite.
3. **Qualification numérique.** Épingler la topologie du graphe, la sémantique des poids, les versions des coefficients et les pas effectifs des appelants. Analyser le spectre ou une borne suffisante justifiée, conserver les mises à jour non écrêtées, comparer les raffinements du pas et rapporter les résidus de projection. Tester séparément si les densités prédisent un résultat cognitif utile.
4. **Test cible AHA.** Figer les graphes et correspondances donneurs et cibles avant d’observer les résultats cibles. Consigner les disanalogies, le comparateur, le réfutateur, le coût et la condition d’arrêt. Comparer le caractère structurellement révisable à la validité cible observée plutôt que de les traiter comme un même critère de résultat.
5. **Expérience de dépendance de l’atelier.** Comparer des conditions à passe unique, à modèle unique répété, à rôles diversifiés et à sources véritablement diversifiées sous des budgets appariés. Évaluer en aveugle lorsque c’est possible ; conserver les échecs et le désaccord. Ne pas inférer l’indépendance de différentes étiquettes de rôles.
6. **Qualification distribuée.** Établir, pour chaque liaison entre pairs, le point d’entrée installé, l’authentificateur, le responsable des ressources, l’autorisation courante, le transport borné, la réservation transactionnelle et l’observation du récepteur. Inclure les accusés de réception perdus, les autorisations périmées et l’expiration des charges utiles. Ne rapporter un pilote à trois nœuds qu’après qualification de toute sa population déclarée.
7. **Comptabilisation du cycle de vie et des copies.** Inventorier tous les responsables de contenus, vérifier le périmètre exact d’expiration et préserver des marqueurs de suppression véridiques. Tester les décisions de correction et d’utilisation courante face à des graphes d’appui alternatifs. Ne pas promettre le rappel de copies hors de la frontière d’application des contrôles.
8. **Évaluation des résultats et des coûts.** Définir le succès de la tâche avant l’inspection, comparer des références appariées, séparer l’appui factuel de l’utilisabilité et rapporter la charge de révision humaine, la latence, les octets et les coûts réels de ressources mesurés. Les mesures indisponibles d’énergie ou d’action totale restent indisponibles. Pour l’hypothèse de partage de la section 14.3, comparer la réutilisation respectueuse des permissions et le recalcul à qualité et couverture appariées, en incluant récupération, vérification, stockage, réplication et coordination. Évaluer la liberté pratique et le contrôle coopératif séparément des économies de ressources.

La séquence de révision indépendante devrait figer le manuscrit et son complément lisible par machine, évaluer la fidélité aux sources et aux chemins d’appels, évaluer les mathématiques et les unités, évaluer la sécurité, la confidentialité et la distribution, évaluer les assertions scientifiques, puis comparer chaque assertion machine à la prose. Les corrections substantielles exigent une nouvelle version et une nouvelle révision ciblée. Il s’agit de la gouvernance de publication de cet article, non d’une preuve que le système a effectué automatiquement ces révisions.

## 17 Discussion et conclusion

La plus petite unité porteuse de sens de Triadic Brain dépend de l’opération. Les octets rendent vérifiable l’identité du contenu ; les empans Unicode rendent les extraits localisables ; les enregistrements applicatifs explicitent les liaisons d’acteur et de tâche ; les assertions et cartes relationnelles rendent les interprétations proposées révisables ; les graphes d’événements et d’artefacts rendent les dérivations attribuables. Ces unités peuvent être composées sans prétendre que l’identité, la vérité et l’autorité sont une seule propriété.

La reconstruction des sources montre des mécanismes natifs concrets : tentatives durables, envoi borné, capture propre au fournisseur, liaison déterministe aux sources, filtres structurels, recalcul borné indépendant et sortie inspectable. Elle révèle aussi des limites nettes. L’incertitude prudente de la passerelle JOINED ordinaire impose une condition de refus ; une probabilité normalisée unique ne certifie pas l’exactitude ; un codec de forme d’onde ne mesure pas la cognition ; une analogie structurelle n’exécute pas son réfutateur ; un journal local ne fournit pas de consensus distribué ; et l’expiration bornée des charges utiles n’établit pas un effacement total.

Le programme GUFT et des eaux cognitives conserve une substance scientifique lorsque ses quantités gardent leurs définitions natives et que ses hypothèses conservent leurs réfutateurs. Le noyau réduit sur graphe, la proposition plus complète de champs, la télémétrie historique et les indicateurs UCM actuels sont des objets distincts. Leur relation est une question d’ingénierie et de recherche, non une égalité autorisée par la notation. L’exemple analytique à deux nœuds démontre l’importance pratique de l’examen des appelants effectifs et du comportement de projection, même lorsque les sorties restent bornées.

L’architecture résultante peut être comprise comme un atelier de connaissances révisables : préserver les observations et alternatives, rendre les transformations inspectables, exposer l’incertitude et maintenir les usages lourds de conséquences sous leur propre autorité. C’est l’analyse étayée de l’article et sa direction de recherche. Le gain sémantique démontré, la coopération active à trois nœuds, le transfert interdomaines calibré et le contrôle complet du cycle de vie des dépendances restent des preuves à obtenir.

## Références

Les dix-huit références scientifiques et normatives ont été ouvertes pour l’édition précédente le 3 novembre 2026. Les versions précises de normes sont citées pour le concept indiqué, non comme attestations de déploiement ou affirmations qu’aucune version suivante n’existe.

1. Yergeau, F. 2003. [UTF-8, a transformation format of ISO 10646. RFC 3629](https://www.rfc-editor.org/rfc/rfc3629.html).
2. Unicode Consortium. 2025. [Unicode Normalization Forms. UAX 15, revision 57, Unicode 17.0.0](https://www.unicode.org/reports/tr15/tr15-57.html).
3. Rundgren, A., Jordan, B., and Erdtman, S. 2020. [JSON Canonicalization Scheme. RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html).
4. NIST. 2015. [Secure Hash Standard. FIPS 180-4](https://csrc.nist.gov/pubs/fips/180-4/upd1/final).
5. Eddy, W., ed. 2022. [Transmission Control Protocol. RFC 9293](https://www.rfc-editor.org/rfc/rfc9293.html).
6. Fielding, R., Nottingham, M., and Reschke, J., eds. 2022. [HTTP/1.1. RFC 9112](https://www.rfc-editor.org/rfc/rfc9112.html).
7. Rescorla, E. 2018. [The Transport Layer Security Protocol Version 1.3. RFC 8446](https://www.rfc-editor.org/rfc/rfc8446.html).
8. Moreau, L., and Missier, P., eds. 2013. [PROV-DM The PROV Data Model. W3C Recommendation](https://www.w3.org/TR/prov-dm/).
9. Vaswani, A., et al. 2017. [Attention Is All You Need](https://arxiv.org/abs/1706.03762v7). Consulted arXiv version 7, revised 2 August 2023.
10. Gentner, D. 1983. [Structure-Mapping A Theoretical Framework for Analogy. Cognitive Science 7, 155–170](https://groups.psych.northwestern.edu/gentner/papers/Gentner83.2b.pdf).
11. Guo, C., Pleiss, G., Sun, Y., and Weinberger, K. Q. 2017. [On Calibration of Modern Neural Networks. PMLR 70, 1321–1330](https://proceedings.mlr.press/v70/guo17a.html).
12. Shannon, C. E. 1948. [A Mathematical Theory of Communication. Bell System Technical Journal 27, 379–423 and 623–656](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf).
13. Driscoll, T. A., and Braun, R. J. [Fundamentals of Numerical Computation, Absolute stability](https://fncbook.com/absstab-diffusion/). Author-maintained numerical-analysis text, chapter 11, section 11.3; accessed 3 November 2026.
14. Du, Y., Li, S., Torralba, A., Tenenbaum, J. B., and Mordatch, I. 2024. [Improving Factuality and Reasoning in Language Models through Multiagent Debate. PMLR 235, 11733–11763](https://proceedings.mlr.press/v235/du24e.html).
15. Lamport, L. 1978. [Time, Clocks, and the Ordering of Events in a Distributed System. Communications of the ACM 21, 558–565](https://lamport.azurewebsites.net/pubs/time-clocks.pdf).
16. Ongaro, D., and Ousterhout, J. 2014. [In Search of an Understandable Consensus Algorithm. USENIX ATC, 305–319](https://www.usenix.org/conference/atc14/technical-sessions/presentation/ongaro).
17. Laurie, B., Messeri, E., and Stradling, R. 2021. [Certificate Transparency Version 2.0. RFC 9162](https://www.rfc-editor.org/rfc/rfc9162.html).
18. Saltzer, J. H., and Schroeder, M. D. 1975. [The Protection of Information in Computer Systems, Basic Principles](https://web.mit.edu/Saltzer/www/publications/protection/Basic.html).

## Index des preuves sources

Les étiquettes suivantes décrivent les groupes de preuves privées sans exposer les emplacements des dépôts, les enregistrements opérationnels ni le code source. La cartographie de révision contrôlée séparément fournit les localisateurs exacts et les limites.

- **I01** Inventaire d’identité des sources, comparaison actuelle des sources acceptées et limites de périmètre.
- **I02** Canonisation, domaines Unicode/JSON acceptés et analyse syntaxique des données transmises.
- **I03** Entrée, passerelle authentifiée, tentatives durables, admission et contrôles effectifs.
- **I04** Exemple témoin construit d’octets, domaines exacts de sérialisation et calculs de coordonnées.
- **I05** Ancrage, passerelle sémantique déterministe, quarantaine, contrats de candidat et de carte d’assertions.
- **I06** Adaptateurs fournisseurs, transport borné, normalisation et conservation de l’achèvement.
- **I07** Axes UCM, projection des hypothèses, seuils et périmètre d’incertitude du parcours ordinaire.
- **I08** Forme d’onde de référence, recherche de contre-exemples, aperture et chemin ordinaire sans écriture PMR.
- **I09** Modèles AHA existants de cas fournis, moteur, enveloppe et périmètre d’audit indépendant.
- **I10** Recalcul Sophia, orientation Atlas, scellement et plafond de révision humaine.
- **I11** Espaces de noms GUFT réconciliés et producteurs et consommateurs historiques de bancs d’essai et de séries temporelles.
- **I12** Équations de recherche des eaux cognitives, noyaux réduits, substitutions effectives par les appelants et récursion.
- **I13** Filiation locale Analyst/Challenge/Synthesis et implémentations historiques multirôles.
- **I14** Transfert d’artefacts entre pairs, interfaces d’expéditeur et de récepteur de modèles, autorisations courantes et consommateurs Challenge externes.
- **I15** Frontières de conception de la grammaire partagée, de la comparaison, de la rétention et du cycle de vie des dépendances.
- **I16** Provenance de conservation/TEL et observation bornée de la charge des actions.
- **I17** Copies contenant du contenu, expiration délimitée et frontières d’effacement non résolues.
- **I18** Tests rédigés et rapports historiques de qualification rattachés aux sources, non réexécutés ici.
- **I19** Complément lisible par machine et contrat de cohérence rédigés pour cet article.
- **I20** Lacunes probatoires restantes et séparation des propositions du code source accepté.

## Annexe A Pseudocode du chemin d’appels

Le pseudocode suivant est explicatif et reconstruit à partir des composants responsables inspectés. Il ne s’agit ni de code source privé, ni d’une intégration exécutable, ni d’une spécification de protocole d’autorisation. Les chemins d’erreur sont abrégés ; chaque statut doit être conservé par son responsable effectif. [I03–I10]

```text
procedure observed_application_task(task_bytes, authenticated_application):
    attempt := custody.register_attempt(task_bytes, authenticated_application)
    admitted := custody.admit(attempt, effective_controls, runtime_bindings)
    if admitted is not admissible: return inspectable_status(attempt, admitted)

    if admitted.kind is NON_MODEL_EVENT:
        return record_event_without_model_candidate(admitted)

    release := require_exact_dispatch_authority(admitted.identity)
    claim := custody.claim_and_reserve(admitted, release, current_limits)
    transport_observation := bounded_provider_call(claim.provider_body)
    captured := custody.commit_and_recompute_normalization(transport_observation)

    if effective_controls.analysis_mode is CAPTURE_ONLY:
        return retained_capture_with_native_stages_not_executed(captured)
    if captured.state is not CAPTURED:
        return noncandidate_completion_projection(captured)

    native_grounding := build_from_already_normalized_source(admitted)
    semantic_capture := exact_substring_claim_proposal(captured.text, native_grounding)
    semantic_capture.uncertainty := 1.0  // this exact bridge contract
    bind_distinct_identities(provider_body, normalized_envelope, semantic_capture)
    native_artifacts := captured_candidate_core(semantic_capture, native_grounding)
    audit := separately_claimed_sophia_recomputation(native_artifacts.raw_free_bundle)
    posture := atlas_orientation(native_artifacts, audit)
    tel := finalize_only_returned_stages(native_artifacts, audit, posture)
    sealed := seal_exact_inventory(native_artifacts, audit, posture, tel)
    return inspectable_result(sealed, separate_human_decision_pending)
```

## Annexe B Complément lisible par machine

`CLAIM_LEDGER.json` attribue à chaque assertion source ou déduction majeure une classe de preuves, un périmètre, des dépendances, des limitations et un emplacement dans le manuscrit. `TRANSFORMATION_GRAPH.json` distingue les arêtes issues de sources observées, les déductions conditionnelles et les propositions. `BYTE_WITNESS.json` ne contient que des charges utiles construites non privées et des identités exactes d’octets. `QUANTITY_CATALOG.json` est un catalogue sélectionné qui préserve les alias de formules et d’estimateurs, les entrées, les unités, les producteurs, les consommateurs, les classes de preuves, les valeurs manquantes et l’écrêtage ou l’arrondi. L’omission de ce catalogue sélectionné n’implique pas l’indisponibilité. Les alias opaques d’estimateurs renvoient à des versions privées exactes ou à des identités mathématiques explicitement génériques. `COMPANION_SCHEMA.json` décrit le contrat syntaxique du registre d’assertions. `validate_companion.py` vérifie les invariants inter-fichiers d’identifiants, de dépendances, d’arêtes de graphe, de sections, d’exemple témoin et de manifeste sans modification ni utilisation du réseau ; ces contrôles procéduraux dépassent ce qu’exprime le schéma JSON. Aucune des deux validations n’établit la vérité scientifique. `MANIFEST.json` lie les fichiers candidats publics sans inclure sa propre empreinte. Ces fichiers sont de nouveaux artefacts explicatifs, non un état exporté du produit ou une API de production. [I19]

Le graphe est une carte sélectionnée de relations conditionnelles, non une séquence d’exécution ni un graphe exhaustif de flot de contrôle. Chaque arête déclare sa relation, ses preuves et sa condition ; les intégrations non établies de modèles entre pairs restent conceptuelles, et les nœuds de proposition ont des identifiants distincts des identifiants de référence. Le complément doit préserver trois invariants : aucun résultat de classe D n’est réétiqueté comme exécuté ; aucune quantité indisponible ne reçoit zéro ; et aucune arête d’identité ou de provenance n’est réétiquetée comme vérité ou autorité d’action. La cartographie privée de révision est exclue de l’ensemble des candidats publics. Les deux cycles complets de révision technique et les 31 constats clôturés appartiennent à la version 1 précédente figée. L’édition suivante ajoute les assertions C078 et C079 avec un périmètre explicite d’hypothèse et de conception normative ; sa révision des éléments concernés est consignée séparément. La publication demeure une action autorisée distincte.
