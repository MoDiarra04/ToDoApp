import React, { useState,useEffect, FormEvent, ChangeEvent } from 'react';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';
import Typography from '@mui/material/Typography';
import Button from '@mui/material/Button';
import AddIcon from '@mui/icons-material/Add';
import Alert from '@mui/material/Alert';
import CheckIcon from '@mui/icons-material/Check';

function AddPost() {
  const [title, setTitle] = useState<string>('');
  const [content, setContent] = useState<string>('');
  const [status, setStatus] = useState<boolean>(false)

  const handleSubmit = async () => {
    const postData = {
      title: title,
      content: content,
      author: "Modibo",  // Standard-Autor, ändern nach implementieren von Login
    };

    const url = "http://127.0.0.1:5000/post/new";
    const options = {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(postData),
    };
    const response = await fetch(url, options);
    const data = await response.json()
    if (response.status === 201) {
      setStatus(true)
    } else {
      setStatus(false)
    }
    console.log(data.message)
  }
  // Effekt, um den Alert nach 3 Sekunden zu verbergen
  useEffect(() => {
    if (status === true) {
      const timer = setTimeout(() => {
        setStatus(false);
      }, 3000); // Der Alert verschwindet nach 3 Sekunden

      return () => clearTimeout(timer); // Timer bereinigen, wenn der Effekt erneut aufgerufen wird
    }
  }, [status]);
  return (
    <>
      <Typography variant="h3" gutterBottom>
        Create a new Post
      </Typography>
      <Box
        component="form"
        sx={{ '& > :not(style)': { m: 1, width: '25ch' } }}
        noValidate
        autoComplete="off"
      >
        <TextField id="outlined-basic" label="Title" variant="outlined"
          type="text"
          value={title}
          onChange={(e: ChangeEvent<HTMLInputElement>) => setTitle(e.target.value)}
          required
        />
      </Box>
      <Box
        component="form"
        sx={{ '& .MuiTextField-root': { m: 1, width: '25ch' } }}
        noValidate
        autoComplete="off"
      >
        <div>
          <TextField
            id="outlined-multiline-static"
            label="Content"
            multiline
            rows={4}
            value={content}
            onChange={(e: ChangeEvent<HTMLTextAreaElement>) => setContent(e.target.value)}
            required
          />
        </div>
      </Box>
      <Box sx={{ m: 1 }}>
        <Button variant="contained" endIcon={<AddIcon />} onClick={handleSubmit} color="secondary">
          Post
        </Button>
      </Box>
      {(() => {
        if (status === true) {
          return (
            <Box sx={{ m: 1 }}>
              <Alert icon={<CheckIcon fontSize="inherit" />} severity="success">
                Post has been created
              </Alert>
            </Box>
          );
        }
        return status; // Wenn Status nicht 201 ist, wird nichts zurückgegeben
      })()}
    </>
  );
}

export default AddPost;
