## Changelog

### [Unreleased]

#### Ajouts
- Suivi cumulé des réservations par club et compétition (`competition.bookings`).
- Normalisation des types numériques lors du chargement des JSON (points, nombre de places).

#### Modifications
- `purchase_places`: validation de la limite totale de 12 places par club/compétition, messages d'erreur clairs.
- `book`: calcul et passage au template de `already_booked` et `remaining_quota`.
- `booking.html`: affichage du quota restant, limitation dynamique de l'input, désactivation du bouton si quota 0.

#### Référence
- Dépôt d'origine: https://github.com/Sedrickgael/Python_Testing


