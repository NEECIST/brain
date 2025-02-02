from flask import session, redirect
import os
import jwt
from config import Config
from flask_login import login_user, logout_user, current_user
from jeec_brain.apps.auth import fenix_client

# handlers
from jeec_brain.apps.auth.handlers.tecnico_client_handler import TecnicoClientHandler
from jeec_brain.handlers.users_handler import UsersHandler
from jeec_brain.handlers.students_handler import StudentsHandler

# services
from jeec_brain.apps.auth.services.encrypt_token_service import EncryptTokenService
from jeec_brain.services.users.generate_credentials_service import (
    GenerateCredentialsService,
)

# finders
from jeec_brain.finders.students_finder import StudentsFinder
from jeec_brain.finders.companies_finder import CompaniesFinder
from jeec_brain.finders.users_finder import UsersFinder

from jeec_brain.models.enums.roles_enum import RolesEnum

import logging

logger = logging.getLogger(__name__)


class AuthHandler(object):
    @staticmethod
    def redirect_to_fenix_login():
        url = TecnicoClientHandler.get_authentication_url(fenix_client)
        return redirect(url, code=302)

    @staticmethod
    def login_student(fenix_auth_code):
        if fenix_auth_code is not None:
            user = TecnicoClientHandler.get_user(fenix_client, fenix_auth_code)
            person = TecnicoClientHandler.get_person(fenix_client, user)

            banned_ids = StudentsFinder.get_banned_students_ist_id()
            if person["username"] in banned_ids:
                return None, None

            student = StudentsFinder.get_from_ist_id(person["username"])
            if student is None:
                course = None
                for role in person["roles"]:
                    if role["type"] == "STUDENT":
                        for registration in role["registrations"]:
                            if registration["acronym"]:
                                course = registration["acronym"]
                                entry_year = get_year(registration["academicTerms"])
                                break
                    if role["type"] == "ALUMNI":
                        for registration in role["concludedRegistrations"]:
                            if registration["acronym"]:
                                course = registration["acronym"]
                                entry_year = get_year(registration["academicTerms"])
                                break

                if not course:
                    return None, None

                if person["email"]:
                    email = person["email"]
                elif person["institutionalEmail"]:
                    email = person["institutionalEmail"]
                else:
                    return None, None

                student = StudentsHandler.create_student(
                    Config.ROCKET_CHAT_ENABLE,
                    person["name"],
                    person["username"],
                    email,
                    course,
                    entry_year,
                    person["photo"]["data"],
                    person["photo"]["type"],
                )
                if student is None:
                    return None, None

            _jwt = jwt.encode(
                {"user_id": person["username"]}, Config.JWT_SECRET, algorithm="HS256"
            )
            encrypted_jwt = EncryptTokenService(_jwt).call()

            return student, encrypted_jwt

        else:
            return None, None

    @staticmethod
    def login_company(username, password):
        user = UsersFinder.get_user_from_credentials(username, password)

        if user is None:
            logger.warning(
                f"User tried to authenticate with credentials: {username}:{password}"
            )
            return False

        company_user = UsersFinder.get_company_user_from_user(user)
        if company_user is None:
            logger.warning(
                f"User tried to authenticate with credentials: {username}:{password}"
            )
            return False

        if user.role.name != "company" or company_user.company is None:
            logger.warning(
                f"""User without company role, tried to login as company! username: {username}"""
            )
            return False

        login_user(user)
        return True, None

    @staticmethod
    def login_admin_dashboard(username, password):
        user = UsersFinder.get_user_from_credentials(username, password)

        if user is None:
            logger.warning(
                f"User tried to authenticate with credentials: {username}:{password}"
            )
            return False

        if user.role.name in [
            "admin",
            "companies_admin",
            "speakers_admin",
            "teams_admin",
            "activities_admin",
            "viewer",
        ]:
            login_user(user)
            return True
        return False

    @staticmethod
    def logout_user():
        logout_user()


def get_year(academicTerms):
    if len(academicTerms) == 0:
        return ""

    terms = [academicTerm[11:].replace(" ", "") for academicTerm in academicTerms]
    terms.sort()
    return terms[0]
