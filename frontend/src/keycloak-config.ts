// src/keycloak-config.ts

import Keycloak from 'keycloak-js';

// Define the Keycloak configuration options
const keycloakConfig: Keycloak.KeycloakConfig = {
  url: 'http://localhost:8080/auth', // URL of your Keycloak server
  realm: 'your-realm',               // Replace with your Keycloak realm name
  clientId: 'your-client-id',        // Replace with your Keycloak client ID
};

// Create a Keycloak instance using the configuration
const keycloak = new Keycloak(keycloakConfig);

export default keycloak;
