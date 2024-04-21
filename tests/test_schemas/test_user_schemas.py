from builtins import str
import pytest
from pydantic import ValidationError
from datetime import datetime
from app.schemas.user_schemas import UserBase, UserCreate, UserUpdate, UserResponse, UserListResponse, LoginRequest

import pytest
from app.schemas.user_schemas import UserBase


def test_user_base_valid(user_base_data):
    # Ensure user_base_data contains the required keys
    assert "email" in user_base_data

    # Create a UserBase instance with the provided data
    user = UserBase(**user_base_data)

    # Assert that the created instance matches the provided data
    #assert user.nickname == user_base_data["nickname"]
    assert user.email == user_base_data["email"]


# Parametrized tests for nickname and email validation
@pytest.mark.parametrize("nickname", ["test_user", "test-user", "testuser123", "123test"])
def test_user_base_nickname_valid(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    user = UserBase(**user_base_data)
    assert user.nickname == nickname


@pytest.mark.parametrize("nickname", ["test user", "test?user", "", "us"])
def test_user_base_nickname_invalid(nickname, user_base_data):
    user_base_data["nickname"] = nickname
    with pytest.raises(ValueError):
        UserBase(**user_base_data)


# Parametrized tests for URL validation
@pytest.mark.parametrize("url", ["http://valid.com/profile.jpg", "https://valid.com/profile.png", None])
def test_user_base_url_valid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    user = UserBase(**user_base_data)
    assert user.profile_picture_url == url


@pytest.mark.parametrize("url", ["ftp://invalid.com/profile.jpg", "http//invalid", "https//invalid"])
def test_user_base_url_invalid(url, user_base_data):
    user_base_data["profile_picture_url"] = url
    with pytest.raises(ValueError):
        UserBase(**user_base_data)


# Tests for invalid email
def test_user_base_invalid_email(user_base_data_invalid):
    with pytest.raises(ValidationError) as exc_info:
        UserBase(**user_base_data_invalid)

    assert "value is not a valid email address" in str(exc_info.value)
    assert "john.doe.example.com" in str(exc_info.value)


# Sample user data with valid attributes
user_base_data = {
    'email': 'john.doe@example.com',
    'nickname': 'johndoe123',
    'first_name': 'John',
    'last_name': 'Doe',
    'bio': 'I am a software engineer with over 5 years of experience.',
    'profile_picture_url': 'https://example.com/profile_pictures/john_doe.jpg',
    'linkedin_profile_url': 'https://linkedin.com/in/johndoe',
    'github_profile_url': 'https://github.com/johndoe',
}

# Sample user data with invalid email (assuming email validation raises ValidationError)
user_base_data_invalid = {
    'nickname': 'johndoe123',
    'first_name': 'John',
    'last_name': 'Doe',
    'bio': 'I am a software engineer with over 5 years of experience.',
    'profile_picture_url': 'https://example.com/profile_pictures/john_doe.jpg',
    'linkedin_profile_url': 'https://linkedin.com/in/johndoe',
    'github_profile_url': 'https://github.com/johndoe',
    'email': 'invalid_email',  # This email is invalid
}
