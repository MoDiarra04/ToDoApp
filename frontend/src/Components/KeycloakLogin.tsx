// src/KeycloakLogin.tsx

import React from 'react';
import { useKeycloak } from '@react-keycloak/web';
import Button from '@mui/material/Button';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';

const KeycloakLogin: React.FC = () => {
  // useKeycloak hook gives access to the Keycloak instance and authentication state
  const { keycloak } = useKeycloak();

  // Check if the user is authenticated
  const isLoggedIn = keycloak.authenticated;

  // Render different buttons and information based on authentication status
  return (
    <Box sx={{ m: 3 }}>
      <Typography variant="h4" gutterBottom>
        Welcome to the Keycloak Authentication Page
      </Typography>

      {isLoggedIn ? (
        // If the user is logged in, show their username and a logout button
        <>
          <Typography variant="h6">
            You are logged in as: {keycloak.tokenParsed?.preferred_username}
          </Typography>
          <Button
            variant="contained"
            color="secondary"
            onClick={() => keycloak.logout()} // Keycloak logout function
            sx={{ mt: 2 }}
          >
            Logout
          </Button>
        </>
      ) : (
        // If the user is not logged in, show a login button
        <>
          <Typography variant="h6">You are not logged in</Typography>
          <Button
            variant="contained"
            color="primary"
            onClick={() => keycloak.login()} // Keycloak login function
            sx={{ mt: 2 }}
          >
            Login
          </Button>
        </>
      )}
    </Box>
  );
};

export default KeycloakLogin;
