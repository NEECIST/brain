from .. import bp
from flask import render_template, request, redirect, url_for, current_app
from jeec_brain.finders.speakers_finder import SpeakersFinder
from jeec_brain.handlers.speakers_handler import SpeakersHandler
from jeec_brain.handlers.companies_handler import CompaniesHandler
from jeec_brain.apps.auth.wrappers import allowed_roles, allow_all_roles
from jeec_brain.values.api_error_value import APIErrorValue
from jeec_brain.schemas.admin_api.speakers.schemas import *
from flask_login import current_user
from jeec_brain.services.files.rename_image_service import RenameImageService


@bp.get("/speakers")
@allow_all_roles
def speakers_dashboard():
    speakers_list = SpeakersFinder.get_all()

    if len(speakers_list) == 0:
        error = "No results found"
        return render_template(
            "admin/speakers/speakers_dashboard.html",
            speakers=None,
            error=error,
            search=None,
            role=current_user.role.name,
        )

    return render_template(
        "admin/speakers/speakers_dashboard.html",
        speakers=speakers_list,
        error=None,
        search=None,
        role=current_user.role.name,
    )


@bp.post("/speakers")
@allow_all_roles
def search_speaker():
    name = request.form.get("name")
    speakers_list = SpeakersFinder.search_by_name(name)

    if len(speakers_list) == 0:
        error = "No results found"
        return render_template(
            "admin/speakers/speakers_dashboard.html",
            speakers=speakers_list,
            error=error,
            search=name,
        )

    return render_template(
        "admin/speakers/speakers_dashboard.html",
        speakers=speakers_list,
        error=None,
        search=name,
    )


@bp.get("/new-speaker")
@allowed_roles(["admin", "speakers_admin"])
def add_speaker_dashboard():
    return render_template("admin/speakers/add_speaker.html")


@bp.post("/new-speaker")
@allowed_roles(["admin", "speakers_admin"])
def create_speaker():
    name = request.form.get("name")
    company = request.form.get("company")
    company_link = request.form.get("company_link")
    position = request.form.get("position")
    country = request.form.get("country")
    bio = request.form.get("bio")
    linkedin_url = request.form.get("linkedin_url")
    youtube_url = request.form.get("youtube_url")
    website_url = request.form.get("website_url")
    spotlight = request.form.get("spotlight")

    if spotlight == "True":
        spotlight = True
    else:
        spotlight = False

    speaker = SpeakersHandler.create_speaker(
        name=name,
        company=company,
        company_link=company_link,
        position=position,
        country=country,
        bio=bio,
        linkedin_url=linkedin_url,
        youtube_url=youtube_url,
        website_url=website_url,
        spotlight=spotlight,
    )

    if speaker is None:
        return render_template(
            "admin/speakers/add_speaker.html", error="Failed to create speaker!"
        )

    if "speaker_image" in request.files:
        file = request.files["speaker_image"]
        if file.filename:
            result, msg = SpeakersHandler.upload_image(file, name)

            if result == False:
                SpeakersHandler.delete_speaker(speaker)
                return render_template("admin/speakers/add_speaker.html", error=msg)

    if speaker.company and "company_logo" in request.files:
        file = request.files["company_logo"]
        if file.filename:
            result, msg = SpeakersHandler.upload_company_logo(file, company)

            if result == False:
                SpeakersHandler.delete_speaker(speaker)
                return render_template("admin/speakers/add_speaker.html", error=msg)

    return redirect(url_for("admin_api.speakers_dashboard"))


@bp.get("/speaker/<string:speaker_external_id>")
@allowed_roles(["admin", "speakers_admin"])
def get_speaker(path: SpeakerPath):
    speaker = SpeakersFinder.get_from_external_id(path.speaker_external_id)

    image_path = SpeakersHandler.find_image(speaker.name)

    company_logo_path = None
    if speaker.company is not None:
        company_logo_path = SpeakersHandler.find_company_logo(speaker.company)

    return render_template(
        "admin/speakers/update_speaker.html",
        speaker=speaker,
        image=image_path,
        company_logo=company_logo_path,
        error=None,
    )


@bp.post("/speaker/<string:speaker_external_id>")
@allowed_roles(["admin", "speakers_admin"])
def update_speaker(path: SpeakerPath):

    speaker = SpeakersFinder.get_from_external_id(path.speaker_external_id)

    if speaker is None:
        return APIErrorValue("Couldnt find speaker").json(500)

    name = request.form.get("name")
    company = request.form.get("company")
    company_link = request.form.get("company_link")
    position = request.form.get("position")
    country = request.form.get("country")
    bio = request.form.get("bio")
    linkedin_url = request.form.get("linkedin_url")
    youtube_url = request.form.get("youtube_url")
    website_url = request.form.get("website_url")
    spotlight = request.form.get("spotlight")

    if spotlight == "True":
        spotlight = True
    else:
        spotlight = False

    image_path = SpeakersHandler.find_image(name)
    company_logo_path = SpeakersHandler.find_company_logo(company)

    old_speaker_name = speaker.name
    old_company_name = speaker.company

    updated_speaker = SpeakersHandler.update_speaker(
        speaker=speaker,
        name=name,
        company=company,
        company_link=company_link,
        position=position,
        country=country,
        bio=bio,
        linkedin_url=linkedin_url,
        youtube_url=youtube_url,
        website_url=website_url,
        spotlight=spotlight,
    )

    if updated_speaker is None:
        return render_template(
            "admin/speakers/update_speaker.html",
            speaker=speaker,
            image=image_path,
            company_logo=company_logo_path,
            error="Failed to update speaker!",
        )

    # Handle Speaker image ------------------------------------
    if old_speaker_name != name:
        RenameImageService("static/speakers", old_speaker_name, name).call()

    if "file" in request.files:
        file = request.files["file"]
        if file.filename:

            result, msg = SpeakersHandler.upload_image(file, name)

            if result == False:
                return render_template(
                    "admin/speakers/update_speaker.html",
                    speaker=updated_speaker,
                    image=image_path,
                    company_logo=company_logo_path,
                    error=msg,
                )

    # Handle Speaker's Company image ---------------------------
    if old_company_name != company:
        RenameImageService(
            "static/speakers/companies", old_company_name, company
        ).call()

    if updated_speaker.company and "company_logo" in request.files:
        file = request.files["company_logo"]
        if file.filename:
            result, msg = SpeakersHandler.upload_company_logo(file, company)

            if result == False:
                return render_template(
                    "admin/speakers/update_speaker.html",
                    speaker=updated_speaker,
                    image=image_path,
                    company_logo=company_logo_path,
                    error=msg,
                )

    return redirect(url_for("admin_api.speakers_dashboard"))


@bp.get("/speaker/<string:speaker_external_id>/delete")
@allowed_roles(["admin", "speakers_admin"])
def delete_speaker(path: SpeakerPath):
    speaker = SpeakersFinder.get_from_external_id(path.speaker_external_id)

    if speaker is None:
        return APIErrorValue("Couldnt find speaker").json(500)

    name = speaker.name
    company = speaker.company

    if SpeakersHandler.delete_speaker(speaker):
        return redirect(url_for("admin_api.speakers_dashboard"))

    else:
        image_path = SpeakersHandler.find_image(name)
        return render_template(
            "admin/speakers/update_speaker.html",
            speaker=speaker,
            image=image_path,
            company_logo=CompaniesHandler.find_image(company.name),
            error="Failed to delete speaker!",
        )
