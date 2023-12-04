import hashlib

import cloudinary
import cloudinary.uploader

from src.conf.config import settings


class CloudImage:
    cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True,
    )

    @staticmethod
    def generate_avatar_name(email: str) -> str:
        """
        The generate_avatar_name function takes an email address as a string and returns a unique avatar name.
            The function uses the hashlib library to create a SHA256 hash of the email address, then truncates it to 12 characters.
            It then prepends 'avatars/' to this string and returns it.

        :param email: str: Pass the email address of the user to the function
        :return: A string of 12 characters, which is the hash of the user's email
        :doc-author: Trelent
        """
        avatar_name = hashlib.sha256(email.encode("utf-8")).hexdigest()[:12]
        public_id = f"{settings.cloudinary_pics_folder}/{avatar_name}"
        return public_id

    @staticmethod
    def upload(public_id: str, file):
        """
        The upload function takes a public_id and file as arguments.
            The public_id is the name of the image that will be uploaded to Cloudinary.
            The file is an image that will be uploaded to Cloudinary.

        :param public_id: str: Specify the public id of the image
        :param file: Upload the file to cloudinary
        :return: A dictionary
        :doc-author: Trelent
        """
        r = cloudinary.uploader.upload(file, public_id=public_id, overwrite=True)
        return r

    @staticmethod
    def get_ulr_4_avatar(public_id: str, r):
        """
        The get_ulr_4_avatar function takes a public_id and an r dictionary as arguments.
        The function returns the src_url of the avatar image with a width of 250, height of 250, crop fill and version from r.

        :param public_id: str: Pass the public id of the image to be displayed
        :param r: Get the version of the image
        :return: The url of the image
        :doc-author: Trelent
        """
        src_url = cloudinary.CloudinaryImage(public_id).build_url(
            width=250, height=250, crop="fill", version=r.get("version")
        )
        return src_url
