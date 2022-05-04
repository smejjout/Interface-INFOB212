"""Interface pour le projet du cours INFOB212"""
import argparse


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

    # exemple d'ajout d'option
    # parser_inscription.add_argument("--name", help="Votre Nom", type=str)

    parser.set_defaults(func=lambda x: parser.print_help())
    parser_inscription.set_defaults(func=inscription)
    parser_info.set_defaults(func=info)
    parser_desinscription.set_defaults(func=desinscription)
    parser_achat.set_defaults(func=achat)
    parser_compta.set_defaults(func=compta)

    # appelle automatiquement les différentes fonctions via `func`
    args = parser.parse_args()
    args.func(args)


def inscription(args: argparse.Namespace) -> None:
    """
    Gère l'incription d'un utilisateur à la base de donnée
    """


def info(args: argparse.Namespace) -> None:
    """
    Gère l'accès aux informations de l'utilisateur
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


if __name__ == "__main__":
    main()
