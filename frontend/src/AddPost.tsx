import React, { useState, FormEvent, ChangeEvent } from 'react';

function AddPost() {
  const [title, setTitle] = useState<string>('');
  const [content, setContent] = useState<string>('');

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();

    const postData = {
      title: title,
      content: content,
      author: "Modibo",  // Standard-Autor
    };

    try {
      const url = "http://127.0.0.1:5000/post/new";
      const options = {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(postData),
      };
      const response = await fetch(url, options);
      
      if (response.ok) {
        console.log("Post erfolgreich erstellt!");
      } else {
        console.log('Fehler beim Erstellen des Posts');
      }
    } catch (error) {
      console.error('Fehler:', error);
    }
  };

  return (
    <div>
      <h1>Neuen Post erstellen</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Title</label>
          <input
            type="text"
            value={title}
            onChange={(e: ChangeEvent<HTMLInputElement>) => setTitle(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Content</label>
          <textarea
            value={content}
            onChange={(e: ChangeEvent<HTMLTextAreaElement>) => setContent(e.target.value)}
            required
          />
        </div>
        <button type="submit">Post erstellen</button>
      </form>
    </div>
  );
}

export default AddPost;
