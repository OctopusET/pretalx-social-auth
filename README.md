# pretalx Social Auth plugin

This is a plugin for [pretalx](https://github.com/pretalx/pretalx) that integrates with [Python Social Auth](https://github.com/python-social-auth/social-core), allowing users to log in with third-party services (SSO/OAuth/OIDC).

Based on [social_django](https://github.com/python-social-auth/social-app-django), with deprecated features removed and pretalx-specific settings added.

Requires pretalx 2025.1.0 or later (which includes the auth plugin signals from [PR #1931](https://github.com/pretalx/pretalx/pull/1931)).

## Screenshots

![Screenshots of pretalx orga login screen and CFP account step with extra providers](img/login_screenshots.png)

## Configuration

In your `pretalx.cfg` file, add the auth backends you need as a comma-separated list under `[authentication]`. Then add the backend-specific settings to the `[plugin:pretalx_social_auth]` section.

You can find backend names and required settings in the [python-social-auth documentation](https://python-social-auth.readthedocs.io/en/latest/backends/index.html).

### Example: GitHub OAuth

```ini
[authentication]
additional_auth_backends=social_core.backends.github.GithubOAuth2

[plugin:pretalx_social_auth]
SOCIAL_AUTH_GITHUB_KEY=your-github-client-id
SOCIAL_AUTH_GITHUB_SECRET=your-github-client-secret
```

### Example: Microsoft + OpenID

```ini
[authentication]
additional_auth_backends=social_core.backends.microsoft.MicrosoftOAuth2,social_core.backends.open_id.OpenIdAuth

[plugin:pretalx_social_auth]
SOCIAL_AUTH_MICROSOFT_GRAPH_KEY=xxxxx-xxxxx-xxxxx-xxxxx-xxxxxxxxxx
SOCIAL_AUTH_MICROSOFT_GRAPH_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Example: Keycloak OIDC

```ini
[authentication]
additional_auth_backends=social_core.backends.keycloak.KeycloakOAuth2

[plugin:pretalx_social_auth]
SOCIAL_AUTH_KEYCLOAK_KEY=your-client-id
SOCIAL_AUTH_KEYCLOAK_SECRET=your-client-secret
SOCIAL_AUTH_KEYCLOAK_PUBLIC_KEY=your-realm-public-key
SOCIAL_AUTH_KEYCLOAK_AUTHORIZATION_URL=https://keycloak.example.com/realms/your-realm/protocol/openid-connect/auth
SOCIAL_AUTH_KEYCLOAK_ACCESS_TOKEN_URL=https://keycloak.example.com/realms/your-realm/protocol/openid-connect/token
```

### Supported providers

Any backend supported by [python-social-auth](https://python-social-auth.readthedocs.io/en/latest/backends/index.html) should work. Common ones include:

- GitHub, GitLab, Bitbucket
- Google, Microsoft/Azure AD
- Keycloak, Auth0, Okta
- Discord, Slack
- Apple, Facebook, Twitter/X, LinkedIn
- Generic OpenID Connect, SAML

### Settings reference

The following settings can be set in `[plugin:pretalx_social_auth]`:

- **Backend credentials**: `SOCIAL_AUTH_<BACKEND>_KEY` and `SOCIAL_AUTH_<BACKEND>_SECRET` for each provider.
- **`BACKEND_NAME_MAPPING`**: Override display names for providers on login buttons (default names are provided for common backends).
- **`LOGIN_REDIRECT_URL`**: Where to redirect after successful login (default: `/`).
- **`DISCONNECT_REDIRECT_URL`**: Where to redirect after disconnecting a provider (default: `/`).
- **`LOGIN_ERROR_URL`**: Where to redirect on auth errors (default: `/`).

### Limitations

- Provider configuration is **instance-wide** (not per-event). API keys are set in `pretalx.cfg`, not in the database. This means care should be taken with custom event domains, as some providers (e.g., Microsoft) require different redirect URIs per domain.

## Development setup

1. Make sure that you have a working [pretalx development setup](https://docs.pretalx.org/en/latest/developer/setup.html).

2. Clone this repository, eg to `local/pretalx-social-auth`.

3. Activate the virtual environment you use for pretalx development.

4. Run `pip install -e .` within this directory to register this application with pretalx's plugin registry.

5. Run `make` within this directory to compile translations.

6. Restart your local pretalx server. This plugin should show up in the plugin list shown on startup in the console.
   You can now use the plugin from this repository for your events by enabling it in the 'plugins' tab in the settings.

This plugin has CI set up to enforce a few code style rules. To check locally, you need these packages installed::

    pip install flake8 flake8-bugbear isort black djhtml

To check your plugin for rule violations, run::

    black --check .
    isort -c .
    djhtml -c .
    flake8 .

You can auto-fix some of these issues by running::

    isort .
    black .
    djhtml .
