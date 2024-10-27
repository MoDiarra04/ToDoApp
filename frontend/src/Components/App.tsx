import React from 'react';
import ButtonAppBar from './AppBar';
import AddPost from './AddPost';
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { BrowserRouter } from "react-router-dom";
import ShowPosts from './ShowPost';
import Room from './Room';
import Box from '@mui/material/Box';

function App() {

  const Theme = createTheme({
    palette: {
      primary: {
        main: "#191414",
      },
      secondary: {
        main: "#6B2D5F",
      },
    },
    typography: {
      fontSize: 16,
      fontFamily: 'Bradley Hand'
    },
  });

  return (
    <BrowserRouter>
      <ThemeProvider theme={Theme}>
        <CssBaseline />
        <div className="App">
          <ButtonAppBar />
        </div>
        <Box 
          display="flex"
          flexDirection={{ xs: 'column', md: 'row' }} // Stacks on small screens, row on medium and up
          justifyContent="left"
          alignItems="flex-start"
          sx={{ mt: 2 }}
        >
          <AddPost />
          <Box sx={{ ml: { lg: 50 , md: 4, xs: 2 }, mt: { xs: 2, md: 0 } }}> {/* Adjusts margin based on screen size */}
            <Room />
          </Box>
        </Box>
        <Box sx={{ mt: 2 }}>
          <ShowPosts />
        </Box>
      </ThemeProvider>
    </BrowserRouter>
  );
}

export default App;
