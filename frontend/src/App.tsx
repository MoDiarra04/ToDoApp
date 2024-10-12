import React from 'react'
import ButtonAppBar from './AppBar'
import AddPost from './AddPost'
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import { BrowserRouter } from "react-router-dom";

function App() {

  const Theme = createTheme({
    palette: {
      primary: {
        main: "#191414",
      },
      secondary: {
        main: "#00bfff",
      },
    },
    typography: {
      fontSize: 16,
      fontFamily:'Bradley Hand'
    },
  });

  return (
    <BrowserRouter>
      <ThemeProvider theme={Theme}>
        <CssBaseline />
        <div className="App">
          <ButtonAppBar />
        </div>
        <AddPost/>
      </ThemeProvider>
    </BrowserRouter>
  )
}

export default App