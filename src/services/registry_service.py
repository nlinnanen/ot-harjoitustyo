from typing import Generator, Optional
from entities.member import Member
from entities.user import User
from db import user_repository as default_user_repository
from db import member_repository as default_member_repository

class InvalidCredentialsError(Exception):
    """Poikkeus joka heitetään, kun käyttäjän kirjautumistiedot ovat virheelliset."""

def admin_required(func):
    """
    Decorator, joka tarkistaa, että käyttäjä on kirjautunut sisään
    ja että hänellä on ylläpitäjän oikeudet.
    """
    def wrapper(self, *args, **kwargs):
        if not self.user or not self.user.admin:
            raise PermissionError("Vain ylläpitäjät voivat suorittaa tämän toiminnon")
        return func(self, *args, **kwargs)
    return wrapper

def user_required(func):
    """
    Decorator, joka tarkistaa, että käyttäjä on kirjautunut sisään ennen toiminnon suorittamista.
    """
    def wrapper(self, *args, **kwargs):
        if not self.user:
            raise PermissionError(
                "Sinun täytyy olla kirjautuneena sisään suorittaaksesi tämän toiminnon"
            )
        return func(self, *args, **kwargs)
    return wrapper

class RegistryService():
    """
    Palvelu, joka tarjoaa rekisteröinnin hallinnan ja käyttäjien sekä jäsenten käsittelyn.
    """
    def __init__(self,
                 user_repository=default_user_repository,
                 member_repository=default_member_repository
                 ):
        """
        Luo uuden rekisteröintipalvelun käyttäen oletusarvoisia tietokannan repositorioita.
        """
        self.user_repository = user_repository
        self.member_repository = member_repository
        self.user: Optional[User] = None

    def log_in(self, email: str, password: str):
        """
        Kirjaa käyttäjän sisään järjestelmään.
        """
        user = self.user_repository.get_user_by_email(email)
        if not user or user.password != password:
            raise InvalidCredentialsError()

        self.user = user
        return user

    @user_required
    def log_out(self):
        """Kirjaa käyttäjän ulos järjestelmästä."""
        self.user = None

    @user_required
    def get_current_user(self):
        """Palauttaa kirjautuneen käyttäjän."""
        return self.user

    @user_required
    def get_all_members(self) -> "Generator[Member, None, None]":
        """Palauttaa generaattorin, joka iteroi kaikki jäsenet."""
        return self.member_repository.get_all_members()

    @user_required
    def get_member_by_id(self, member_id: int) -> Member:
        """Hakee jäsenen annetulla tunnisteella."""
        return self.member_repository.get_member_by_id(member_id)

    @user_required
    def update_current_member(self, **kwargs):
        """Päivittää kirjautuneen käyttäjän tietoihin liittyvän jäsenen tiedot."""
        if not self.user:
            raise PermissionError(
                "Sinun täytyy olla kirjautuneena sisään suorittaaksesi tämän toiminnon"
            )
        current_member = self.member_repository.get_member_by_user_id(self.user.id)
        self.member_repository.update_member(Member(**{**current_member.__dict__, **kwargs}))

    @admin_required
    def add_member(self, **kwargs):
        """Lisää uuden jäsenen tietokantaan."""
        return self.member_repository.add_member(Member(**kwargs))

    @admin_required
    def delete_member(self, member_id: int):
        """Poistaa jäsenen tietokannasta annetun tunnisteen perusteella."""
        self.member_repository.delete_member(member_id)

    @admin_required
    def add_user(self, email: str, password: str, admin: bool = False):
        """Lisää uuden käyttäjän tietokantaan."""
        return self.user_repository.add_user(User(email=email, password=password, admin=admin))

    @admin_required
    def update_member(self, member_id, **kwargs):
        """Päivittää jäsenen tiedot annetun tunnisteen perusteella."""
        member = self.member_repository.get_member_by_id(member_id)
        self.member_repository.update_member(Member(**{**member.__dict__, **kwargs}))
