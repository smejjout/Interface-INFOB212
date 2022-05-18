"""Interface pour le projet du cours INFOB212"""
import argparse
import re


# Pour une interface graphique facile voir Gooey
# https://github.com/chriskiehl/Gooey
# @Gooey
def main() -> None:
    """
    Fonction Principale;
    c'est elle qui appelle toute les autres et définis les différentes commandes
    """
    # __doc__ est la chaine de caractère toute en haut du fichier
    parser = argparse.ArgumentParser(description=__doc__)

    subparsers = parser.add_subparsers()
    # on peut accéder à la docstring d'une fonction grâce à l'attribut __doc__
    parser_inscription = subparsers.add_parser("inscription", help=inscription.__doc__)
    parser_info = subparsers.add_parser("info", help=info.__doc__)
    parser_desinscription = subparsers.add_parser(
        "desinscription", help=desinscription.__doc__
    )
    parser_achat = subparsers.add_parser("achat", help=achat.__doc__)
    parser_compta = subparsers.add_parser("compta", help=compta.__doc__)
    parser_critique = subparsers.add_parser("critique", help=critique.__doc__)

    def phone_number(arg: str) -> str:
        """Validateur pour numéro de téléphone"""
        if not re.match(
            (
                r"^([\+][0-9]{1,3}[ \.\-])?([\(]{1}[0-9]{1,6}[\)])?([0-9 \.\-\/]{3,20})"
                r"((x|ext|extension)[ ]?[0-9]{1,4})?$"
            ),
            arg,
        ):
            raise argparse.ArgumentTypeError("Not a valid phone number")
        return arg

    # Inscription
    parser_inscription.add_argument(
        "--rue", help="La rue de votre adresse", required=True
    )
    parser_inscription.add_argument(
        "--ville", help="La ville oú vous habitez", required=True
    )
    parser_inscription.add_argument(
        "--phone", help="Votre numéro de téléphone", type=phone_number, required=True
    )
    parser_inscription.add_argument(
        "--phone2",
        help="Votre numéro de téléphone secondaire si vous en avez un",
        type=phone_number,
    )

    # Info
    parser_info.add_argument("--rue", help="La rue de votre adresse")
    parser_info.add_argument("--ville", help="La ville oú vous habitez")
    parser_info.add_argument(
        "--phone", help="Votre numéro de téléphone", type=phone_number
    )
    parser_info.add_argument(
        "--phone2",
        help="Votre numéro de téléphone secondaire si vous en avez un",
        type=phone_number,
    )

    # Comptabilité
    parser_compta.add_argument(
        "--annee",
        help="Année pour laquelle consulter le rapport (format YYYY)",
        type=int,
    )

    # Achat
    # TODO add choices for hard coded types in db
    # MAYBE add validators
    # |-> use the database to validate, if so, write files to disk as cache
    parser_achat.add_argument(
        "--resto",
        "--restaurant",
        help="Utiliser l'identifiant",
        type=int,
        required=True,
    )
    sur_place_ou_a_emporter = parser_achat.add_mutually_exclusive_group()
    sur_place_ou_a_emporter.add_argument(
        "--sur-place", action="store_true", help="Activer si sur place"
    )
    sur_place_ou_a_emporter.add_argument(
        "--societe",
        help="Societe de livraison (seulement si à emporter)",
        choices=("uber", "deliveroo", "takeaway"),
    )
    parser_achat.add_argument(
        "--burger",
        metavar="",
        help=(
            "VIANDE{angus, beef, chicken} "
            "CRUDITES{lettuce, carrots} "
            'PAIN{"normal bun", "special"}'
        ),
        nargs=3,
        action="append",
    )
    parser_achat.add_argument(
        "--boisson",
        nargs=2,
        help="TAILLE(in cL) TYPE{coca, fanta, eau}",
        metavar="",
        action="append",
    )
    parser_achat.add_argument(
        "--accompagnement",
        metavar="TYPE",
        action="append",
        choices=("frites", "wings", "rings"),
    )

    # Critique
    parser_critique.add_argument(
        "--note", type=int, help="Note que vous souhaitez donner", required=True
    )
    parser_critique.add_argument(
        "--livreur",
        type=int,
        help="Identifiant du livreur que vous souhaitez donner",
        required=True,
    )

    parser.set_defaults(func=lambda x: parser.print_help())
    parser_inscription.set_defaults(func=inscription)
    parser_info.set_defaults(func=info)
    parser_desinscription.set_defaults(func=desinscription)
    parser_achat.set_defaults(func=achat)
    parser_compta.set_defaults(func=compta)

    # appelle automatiquement les différentes fonctions via `func`
    args = parser.parse_args()
    print(args)
    args.func(args)


def inscription(args: argparse.Namespace) -> None:
    """
    Gère l'incription d'un utilisateur à la base de donnée
    """


def info(args: argparse.Namespace) -> None:
    """
    Gère l'accès aux informations de l'utilisateur.
    """


def desinscription(args: argparse.Namespace) -> None:
    """
    Gère la désincription d'un utilisateur à la base de donnée
    """


def achat(args: argparse.Namespace) -> None:
    """
    Gère les achats
    """


def compta(args: argparse.Namespace) -> None:
    """
    Gère les fonctions de comptabilité
    """
    print(args.annee)


def critique(args: argparse.Namespace) -> None:
    """
    Gère les critiques
    """


if __name__ == "__main__":
    main()
