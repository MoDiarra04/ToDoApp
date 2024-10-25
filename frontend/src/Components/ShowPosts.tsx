import React, { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import TextField from '@mui/material/TextField';
import Button from '@mui/material/Button';
import Alert from '@mui/material/Alert';
import EditIcon from '@mui/icons-material/Edit';
import SaveIcon from '@mui/icons-material/Save';

interface Post {
  _id: string;
  title: string;
  content: string;
  author: string;
}

function ShowPosts() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [editingPostId, setEditingPostId] = useState<string | null>(null);
  const [editedTitle, setEditedTitle] = useState<string>('');
  const [editedContent, setEditedContent] = useState<string>('');

  // Fetch the posts from the backend when the component mounts
  useEffect(() => {
    const fetchPosts = async () => {
      try {
        const response = await fetch('http://127.0.0.1:5000/posts');
        if (!response.ok) {
          throw new Error('Failed to fetch posts');
        }
        const data = await response.json();
        setPosts(data); // Assuming response is an array of posts
      } catch (error: any) {
        setError(error.message);
      }
    };

    fetchPosts();
  }, []);

  // Function to start editing a post
  const handleEditClick = (post: Post) => {
    setEditingPostId(post._id);
    setEditedTitle(post.title);
    setEditedContent(post.content);
  };

  // Function to save the edited post
  const handleSaveClick = async () => {
    if (!editingPostId) return;

    const updatedPost = {
      title: editedTitle,
      content: editedContent,
      author: 'Modibo', // Optionally update the author if needed
    };

    try {
      const response = await fetch(`http://127.0.0.1:5000/post/${editingPostId}/update`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedPost),
      });

      if (!response.ok) {
        throw new Error('Failed to update post');
      }

      // Update the post in the local state after successful update
      setPosts(posts.map(post =>
        post._id === editingPostId ? { ...post, title: editedTitle, content: editedContent } : post
      ));

      setEditingPostId(null);
      setEditedTitle('');
      setEditedContent('');
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
            {editingPostId === post._id ? (
              <>
                <TextField
                  label="Title"
                  variant="outlined"
                  fullWidth
                  value={editedTitle}
                  onChange={(e) => setEditedTitle(e.target.value)}
                  sx={{ mb: 1 }}
                />
                <TextField
                  label="Content"
                  variant="outlined"
                  fullWidth
                  multiline
                  rows={4}
                  value={editedContent}
                  onChange={(e) => setEditedContent(e.target.value)}
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
                  onClick={() => setEditingPostId(null)}
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
                  variant="outlined"
                  startIcon={<EditIcon />}
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
