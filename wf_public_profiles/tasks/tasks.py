import requests

from sqlalchemy.orm import Session

from wf_public_profiles.config import settings
from wf_public_profiles.crud import public_profile
from wf_public_profiles.log import logger
from wf_public_profiles.schemas import PublicProfileCreate


def update_public_profiles(db: Session):
    logger.info("Attempting to update public profiles...")

    headers = {"Accept": "application/json"}

    hola_spirit_auth_url = f"https://app.holaspirit.com/oauth/v2/token?client_id={settings.HOLASPIRIT_CLIENT_ID}&grant_type=password&username={settings.HOLASPIRIT_USERNAME}&password={settings.HOLASPIRIT_PASSWORD}"
    auth_response = requests.get(hola_spirit_auth_url, headers=headers, timeout=20)
    access_token = auth_response.json()["access_token"]

    headers["Authorization"] = f"Bearer {access_token}"

    page = 1
    members = []
    while page is not None:
        hola_spirit_members_url = (
            f"https://app.holaspirit.com/api/organizations/{settings.HOLASPIRIT_ORGANIZATION_ID}/members"
        )
        members_response = requests.get(hola_spirit_members_url, params={"page": page}, headers=headers, timeout=20)

        members.extend(members_response.json()["data"])

        page = None
        pagination = members_response.json()["pagination"]
        if pagination is not None and "nextPage" in pagination and pagination["nextPage"] is not None:
            page = int(pagination["nextPage"])

    def lower_strip(s):
        s.lower().strip()

    ignore = list(map(lower_strip, settings.HOLASPIRIT_PUBLIC_PROFILES_IGNORE))

    try:
        logger.info("Removing existing public profiles")
        public_profile.remove_all(db=db)

        for member in members:
            if member["displayName"].lower().strip() in ignore or member["id"] in ignore:
                continue

            new_public_profile = PublicProfileCreate(holaspirit_id=member["id"], name=member["displayName"])

            if member["avatarUrl"]:
                new_public_profile.img_url = f"https://app.holaspirit.com/{member['avatarUrl']}"
            else:
                new_public_profile.img_url = f"{settings.APP_URL}/public_profiles/static/flower.png"

            for custom_field_key in member["customFields"]:
                custom_field = member["customFields"][custom_field_key]
                name = custom_field["name"].lower()
                if name.find("headline") >= 0 and custom_field["value"]:
                    new_public_profile.role = custom_field["value"][:120]
                elif name.find("public bio") >= 0 and custom_field["value"]:
                    new_public_profile.bio = custom_field["value"][:256]

            if new_public_profile.bio and new_public_profile.role:
                new_public_profile.role = " ".join([w[:25] for w in new_public_profile.role.split()])
                new_public_profile.bio = " ".join([w[:25] for w in new_public_profile.bio.split()])

                logger.info(f"Creating public profile for {new_public_profile.name}")
                public_profile.create(db=db, obj_in=new_public_profile)

        db.commit()
        logger.info("Public profiles updated")
    except Exception as e:
        logger.critical(e)
        db.rollback()
