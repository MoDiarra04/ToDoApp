import React, { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Alert from '@mui/material/Alert';
import EditIcon from '@mui/icons-material/Edit';
import SaveIcon from '@mui/icons-material/Save';
import { io, Socket } from 'socket.io-client';

const socket: Socket = io("http://localhost:5000");

interface Post {
  _id: string;
  title: string;
  content: string;
  author: string;
}

function ShowPosts() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [editingPost, setEditingPost] = useState<{ post_id: string | null; title: string; content: string }>({
    post_id: null,
    title: '',
    content: '',
  });

  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/posts');
        if (!response.ok) throw new Error('Failed to fetch posts');
        const data = await response.json();
        setPosts(data);
      } catch (error: any) {
        setError(error.message);
      }
    };

    fetchPosts();
  }, []);

  useEffect(() => {
    // WebSocket-Verbindung herstellen und auf Nachrichten reagieren
    socket.on('new_post', (post) => {
      setPosts(prevTodos => [...prevTodos, post]);
    });

    socket.on('update_post', (updatedPost: Post) => {
      setPosts(prevposts =>
        prevposts.map(post => post._id === updatedPost._id ? updatedPost : post)
      );
    });

    socket.on('delete_post', (data: { post_id: string }) => {
      setPosts(prevposts =>
        prevposts.filter(post => post._id !== data.post_id)
      );
    });

    return () => {
      socket.off('new_post');
      socket.off('update_post');
      socket.off('delete_post');
    };
  }, []);

  const handleEditClick = (post: Post) => {
    setEditingPost({ post_id: post._id, title: post.title, content: post.content });
  };

  //hier unterscheiden zwischen http-request oder Echtzeit-Request über SocketIO mit if else
  const handleSaveClick = async () => {
    if (!editingPost.post_id) return;

    const updatedPost = {
        title: editingPost.title,
        content: editingPost.content,
        author: 'Modibo',
    };

    try {
        const response = await fetch(`http://127.0.0.1:5000/post/${editingPost.post_id}/update`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(updatedPost),
        });

        const data = await response.json();

        if (response.status === 200) {
            // Update the posts state if the update was successful
            setPosts(posts.map(post =>
                post._id === editingPost.post_id ? { ...post, ...updatedPost } : post
            ));
            
            // Close the editing view by resetting the editingPost state
            setEditingPost({ post_id: null, title: '', content: '' });
            console.log(data.message);
        } else {
            // Handle error scenario without changing the original message handling
            console.log(data.message);
        }
        
    } catch (error: any) {
        setError(error.message);
    }
};


  return (
    <Box sx={{ m: 2 }}>
      <Typography variant="h4" gutterBottom>
        All Posts
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {posts.length === 0 && !error ? (
        <Typography>No posts available.</Typography>
      ) : (
        posts.map((post) => (
          <Paper key={post._id} sx={{ p: 2, mb: 2 }}>
            {editingPost.post_id === post._id ? (
              <>
                <TextField
                  label="Title"
                  variant="outlined"
                  fullWidth
                  value={editingPost.title}
                  onChange={(e) => setEditingPost({ ...editingPost, title: e.target.value })}
                  sx={{ mb: 1 }}
                />
                <TextField
                  label="Content"
                  variant="outlined"
                  fullWidth
                  multiline
                  rows={4}
                  value={editingPost.content}
                  onChange={(e) => setEditingPost({ ...editingPost, content: e.target.value })}
                  sx={{ mb: 1 }}
                />
                <Button
                  variant="contained"
                  startIcon={<SaveIcon />}
                  onClick={handleSaveClick}
                  color="primary"
                  sx={{ mr: 1 }}
                >
                  Save
                </Button>
                <Button
                  variant="outlined"
                  onClick={() => setEditingPost({ post_id: null, title: '', content: '' })}
                  color="secondary"
                >
                  Cancel
                </Button>
              </>
            ) : (
              <>
                <Typography variant="h6">{post.title}</Typography>
                <Typography variant="body2" color="textSecondary">
                  By {post.author}
                </Typography>
                <Typography variant="body1" sx={{ mt: 1 }}>
                  {post.content}
                </Typography>
                <Button
                  variant="contained"
                  startIcon={<EditIcon />}
                  color="secondary"
                  onClick={() => handleEditClick(post)}
                  sx={{ mt: 1 }}
                >
                  Edit
                </Button>
              </>
            )}
          </Paper>
        ))
      )}
    </Box>
  );
}

export default ShowPosts;
