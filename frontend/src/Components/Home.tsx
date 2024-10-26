import React, { useState, useEffect } from 'react';
import { io, Socket } from 'socket.io-client';

interface Post {
  _id: string;
  title: string;
  content: string;
  author: string;
  completed: boolean
}

const socket: Socket = io('http://localhost:5000');

const postList: React.FC = () => {
  const [posts, setPost] = useState<Post[]>([]);

  useEffect(() => {
    // WebSocket-Verbindung herstellen und auf Nachrichten reagieren
    socket.on('update_post', (updatedPost: Post) => {
      setPost(prevposts =>
        prevposts.map(post => post._id === updatedPost._id ? updatedPost : post)
      );
    });

    socket.on('delete_post', (data: { post_id: string }) => {
      setPost(prevposts =>
        prevposts.filter(post => post._id !== data.post_id)
      );
    });

    socket.on('mark_post', (data: { post_id: string; status: boolean }) => {
      setPost(prevposts =>
        prevposts.map(post => post._id === data.post_id ? { ...post, completed: data.status } : post)
      );
    });

    return () => {
      socket.off('update_post');
      socket.off('delete_post');
      socket.off('mark_post');
    };
  }, []);

  return (
    <div>
      <h1>post List</h1>
      <ul>
        {posts.map(post => (
          <li key={post._id}>
            {post.title} - {post.completed ? "Completed" : "Not Completed"}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default postList;
