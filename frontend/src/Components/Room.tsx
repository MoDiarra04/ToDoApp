import React, { useState, ChangeEvent } from 'react';
import Typography from '@mui/material/Typography';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Stack from '@mui/material/Stack';
import { io, Socket } from 'socket.io-client';

const socket: Socket = io("http://localhost:5000");

function Room() {
  const [RoomCode, setRoomCode] = useState<string>('');
  const [error, setError] = useState<boolean>(false)

  const handleJoin = () => {
    if (!RoomCode) {
      setError(true)
    } else {
      //socket.emit('join_room', { room: 'room_name', user_id: });
    }
  }

  const handleCreate = async() => {
    try {
      const response = await fetch('http://127.0.0.1:5000/generate_code');
      if (!response.ok) throw new Error('Failed to fetch RoomCode');
      const data = await response.json();
      setRoomCode(data);
      console.log(data)
    } catch (error: any) {
      console.log(error.message);
    }
  }

  return (
    <>
      <Typography variant="h3" gutterBottom>
        Enter a Room
      </Typography>
      <TextField
        disabled
        id="outlined-disabled" // Username placeholder
        label="Username"
        defaultValue="Your Username"
      />
      <Box>
        <Stack
          direction={{ xs: 'column', sm: 'row' }}
          spacing={{ xs: 1, sm: 1, md: 1 }}
          sx={{ mt: 2 }}
        >
          <TextField id="outlined-basic" label="Room Code" variant="outlined" error={error}
            onChange={(e: ChangeEvent<HTMLInputElement>) => setRoomCode(e.target.value)} />
          <Button variant="contained" size="medium" color="secondary" onClick={handleJoin}>
            Join a Room
          </Button>
        </Stack>
      </Box>
      <Box sx={{ mt: 2 }}> {/* Adds space between buttons */}
        <Button variant="contained" size="large" color="secondary" onClick={handleCreate}>
          Create a Room
        </Button>
      </Box>
    </>
  );
}

export default Room;
