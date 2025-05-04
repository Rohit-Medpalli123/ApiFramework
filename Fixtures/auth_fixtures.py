"""
Authentication Fixtures Module

Provides pytest fixtures for managing authentication details.
Supports environment-specific credential management.
"""

import pytest
from typing import Dict, Any
from Conf import api_example_conf as conf
from Core.api_player import APIPlayer


class CredentialManager:
    """Manages environment-specific credentials."""
    
    def __init__(self, env: str):
        """
        Initialize with environment.
        
        Args:
            env: Environment name (staging/production/development)
        """
        self.env = env
        self._credentials_map = {
            'staging': {
                'username': conf.staging_user,
                'password': conf.staging_password
            },
            'production': {
                'username': conf.prod_user,
                'password': conf.prod_password
            },
            'development': {
                'username': conf.dev_user,
                'password': conf.dev_password
            }
        }
    
    def get_credentials(self) -> Dict[str, str]:
        """
        Get credentials for current environment.
        
        Returns:
            Dict[str, str]: Username and password
        """
        return self._credentials_map.get(
            self.env,
            {
                'username': conf.user_name,
                'password': conf.password
            }
        )


class AuthProvider:
    """Provides authentication details for API tests."""
    
    def __init__(self, api_player: APIPlayer):
        """
        Initialize with API player.
        
        Args:
            api_player: Configured API player instance
        """
        self.api_player = api_player
    
    def get_auth_details(self, credentials: Dict[str, str]) -> Dict[str, Any]:
        """
        Get authentication details.
        
        Args:
            credentials: Username and password
            
        Returns:
            Dict[str, Any]: Authentication details
        """
        return self.api_player.set_auth_details(
            credentials['username'],
            credentials['password']
        )


@pytest.fixture(scope='function')
def credential_manager(request: pytest.FixtureRequest) -> CredentialManager:
    """
    Provides credential manager for current environment.
    
    Args:
        request: Pytest request object
        
    Returns:
        CredentialManager: Configured credential manager
    """
    env = request.config.getoption("--env", default="staging")
    return CredentialManager(env)


@pytest.fixture(scope='function')
def auth_provider(api_player_fixture: APIPlayer) -> AuthProvider:
    """
    Provides authentication provider.
    
    Args:
        api_player_fixture: Configured API player instance
        
    Returns:
        AuthProvider: Configured authentication provider
    """
    return AuthProvider(api_player_fixture)


@pytest.fixture(scope='function')
def auth_details(
    credential_manager: CredentialManager,
    auth_provider: AuthProvider
) -> Dict[str, Any]:
    """
    Provides authentication details for API tests.
    
    Args:
        credential_manager: Credential manager instance
        auth_provider: Authentication provider instance
        
    Returns:
        Dict[str, Any]: Authentication details
    """
    credentials = credential_manager.get_credentials()
    return auth_provider.get_auth_details(credentials)
