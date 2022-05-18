"""Interface pour le projet du cours INFOB212"""
import argparse
from datetime import datetime
import re

import mysql.connector
from mysql.connector import errorcode

try:
    with open(".client_id", "r", encoding="utf8") as _client_id_fd:
        CLIENT_ID = _client_id_fd.read()
except FileNotFoundError:
    CLIENT_ID = str()
try:
    cnx = mysql.connector.connect(
        user="admin",
        password="password",
        host="127.0.0.1",
        database="northwind",
        auth_plugin="mysql_native_password",
    )
    cursor = cnx.cursor()
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
    exit(2)


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

    # Desinscription
    parser_desinscription.add_argument(
        "-y", "--yes", help="Désactive la demande de confirmation", action="store_true"
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
    sur_place_ou_a_emporter = parser_achat.add_mutually_exclusive_group(required=True)
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
    parser_critique.set_defaults(func=critique)

    # appelle automatiquement les différentes fonctions via `func`
    args = parser.parse_args()
    args.func(args)
    cursor.close()
    cnx.close()


def inscription(args: argparse.Namespace) -> None:
    """
    Gère l'incription d'un utilisateur à la base de donnée
    """
    add_client = (
        "INSERT INTO CLIENT"
        "(adr_rue, adr_ville, telephone1, telephone2)"
        "VALUES (%s, %s, %s, %s)"
    )
    data_client = (
        args.rue,
        args.ville,
        args.phone,
        args.phone2 if args.phone2 else "NULL",
    )
    cursor.execute(add_client, data_client)
    with open(".client_id", "w", encoding="utf8") as client_id_fd_w:
        client_id_fd_w.write(str(cursor.lastrowid))
    cnx.commit()


def info(args: argparse.Namespace) -> None:
    """
    Gère l'accès aux informations de l'utilisateur.
    """
    if not CLIENT_ID:
        print("Veuillez d'abord vous inscrire SVP")
        exit(2)

    update_client = (
        "UPDATE CLIENT "
        "SET adr_rue=%s, adr_ville=%s, telephone1=%s, telephone2=%s "
        "WHERE num_id=%s;"
    )
    data_client = (
        args.rue,
        args.ville,
        args.phone,
        args.phone2 if args.phone2 else "NULL",
        CLIENT_ID,
    )
    cursor.execute(update_client, data_client)
    select_client = (
        "SELECT num_id, adr_rue, adr_ville, telephone1, telephone2 FROM CLIENT "
        "WHERE num_id = %s;"
    )
    cursor.execute(select_client, [CLIENT_ID])
    for num_id, adr_rue, adr_ville, telephone1, telephone2 in cursor:
        print(
            (
                f"Client {num_id} habite à {adr_rue}, {adr_ville}."
                f" Il peut être appelé via {telephone1}"
            )
            + (f" ou {telephone2}" if telephone2 != "NULL" else "")
        )
    cnx.commit()


def desinscription(args: argparse.Namespace) -> None:
    """
    Gère la désincription d'un utilisateur à la base de donnée
    """
    if not CLIENT_ID:
        print("Veuillez d'abord vous inscrire SVP")
        exit(2)

    confirmation = "y" if args.yes else ""
    while confirmation != "y":
        confirmation = input(
            (
                "Ceci va effacer toute vos information personelles,"
                " êtes-vous sûr de vouloir continuer?[y/n]\t"
            )
        ).lower()
        if confirmation == "n":
            exit(2)
        else:
            print("Entrez 'y' ou 'n', SVP")
    update_client = (
        "UPDATE CLIENT "
        "SET adr_rue='', adr_ville='', telephone1='', telephone2=NULL "
        "WHERE num_id=%s;"
    )
    data_client = (CLIENT_ID,)
    cursor.execute(update_client, data_client)
    cnx.commit()
    print("Les données du client ont bien été effacées")


def achat(args: argparse.Namespace) -> None:
    """
    Gère les achats
    """
    # COMMANDE
    add_commande = (
        "INSERT INTO COMMANDE "
        f"(type, date, {'SUR_PLACE' if args.sur_place else 'A_EMPORTE'}, resto_id) "
        "VALUES (%s, %s, %s, %s)"
    )
    data_commande = (
        "test" if args.sur_place else "A_EMPORTE",
        datetime.now().date(),
        "1",
        args.resto,
    )
    cursor.execute(add_commande, data_commande)
    num_com = cursor.lastrowid
    if args.societe:
        # A_EMPORTE
        add_a_emporter = "INSERT INTO A_EMPORTE (num_com) VALUES (%s)"
        data_a_emporter = (num_com,)
        cursor.execute(add_a_emporter, data_a_emporter)

        # prends livreur aléatoire de la societe
        select_livreur = (
            "SELECT nlivreur FROM LIVREUR "
            "WHERE societe = %s "
            "ORDER BY RAND() "
            "LIMIT 1"
        )
        data_livreur = (args.societe,)
        for result in cursor.execute(select_livreur, data_livreur, multi=True):
            if result.with_rows:
                nlivreur = result.fetchone()[0]
                # LIVRAISONS
                add_livraison = (
                    "INSERT INTO LIVRAISONS (num_com, nlivreur, num_id) "
                    "VALUES (%s, %s, %s)"
                )
                data_livraison = (num_com, nlivreur, CLIENT_ID)
                cursor.execute(add_livraison, data_livraison)
            else:
                print("Livreur introuvable")
                exit(2)
    else:
        # SUR_PLACE
        add_sur_place = "INSERT INTO SUR_PLACE (num_com, num_id) VALUES (%s, %s)"
        data_sur_place = (num_com, CLIENT_ID)
        cursor.execute(add_sur_place, data_sur_place)

    if args.burger:
        # trouve num_produit pour la combinaison donnée
        for burger in args.burger:
            qte_prod = args.burger.count(burger)
            # enleve toute les occurences de l'élement pour ne pas réitérer dessus
            for burger_bis in args.burger:
                if burger_bis == burger:
                    args.burger.remove(burger)
            viande, crudite, pain = burger
            select_burger = (
                "SELECT num_produit FROM BURGER "
                "WHERE viande=%s AND crudite=%s AND pain=%s"
            )
            data_burger = (viande, crudite, pain)
            for result in cursor.execute(select_burger, data_burger, multi=True):
                if result.with_rows:
                    try:
                        num_produit = cursor.fetchone()[0]
                    except TypeError:
                        print("Burger introuvable")
                        exit(2)
                    # DETAIL
                    add_detail = (
                        "INSERT INTO DETAIL "
                        "(num_com, num_produit, qte_prod) "
                        "VALUES (%s, %s, %s)"
                    )
                    data_detail = (num_com, num_produit, qte_prod)
                    cursor.execute(add_detail, data_detail)
    if args.boisson:
        for boisson in args.boisson:
            qte_prod = args.boisson.count(boisson)
            # enleve toute les occurences de l'élement pour ne pas réitérer dessus
            for boisson_bis in args.boisson:
                if boisson_bis == boisson:
                    args.boisson.remove(boisson)
            taille, type = boisson
            select_boisson = (
                "SELECT num_produit FROM BOISSON WHERE taille=%s AND type_boisson=%s"
            )
            data_boisson = (taille, type)
            for result in cursor.execute(select_boisson, data_boisson, multi=True):
                if result.with_rows:
                    try:
                        num_produit = cursor.fetchone()[0]
                    except TypeError:
                        print("Boisson introuvable")
                        exit(2)
                    # DETAIL
                    add_detail = (
                        "INSERT INTO DETAIL "
                        "(num_com, num_produit, qte_prod) "
                        "VALUES (%s, %s, %s)"
                    )
                    data_detail = (num_com, num_produit, qte_prod)
                    cursor.execute(add_detail, data_detail)
    if args.accompagnement:
        for accompagnement in args.accompagnement:
            qte_prod = args.accompagnement.count(accompagnement)
            # enleve toute les occurences de l'élement pour ne pas réitérer dessus
            for accompagnement_bis in args.accompagnement:
                if accompagnement_bis == accompagnement:
                    args.accompagnement.remove(accompagnement)
            select_accompagnement = (
                "SELECT num_produit FROM ACCOMPAGNEMENT WHERE type=%s"
            )
            data_accompagnement = (accompagnement,)
            for result in cursor.execute(
                select_accompagnement, data_accompagnement, multi=True
            ):
                if result.with_rows:
                    try:
                        num_produit = cursor.fetchone()[0]
                    except TypeError:
                        print("Accompagnement introuvable")
                        exit(2)
                    # DETAIL
                    add_detail = (
                        "INSERT INTO DETAIL "
                        "(num_com, num_produit, qte_prod) "
                        "VALUES (%s, %s, %s)"
                    )
                    data_detail = (num_com, num_produit, qte_prod)
                    cursor.execute(add_detail, data_detail)

    cnx.commit()


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
