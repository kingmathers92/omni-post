import { useState } from "react";
import axios from "axios";
import "./index.css";

function App() {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [scheduleTime, setScheduleTime] = useState("");
  const [platform, setPlatform] = useState("");
  const [message, setMessage] = useState("");

  const postContent = async () => {
    try {
      await axios.post("http://localhost:8000/api/post/", {
        title,
        content,
        platform,
      });
      setMessage(`Post to ${platform} successful`);
      clearForm();
    } catch (error) {
      setMessage(`Post to ${platform} failed`);
    }
  };

  const saveDraft = async () => {
    try {
      await axios.post("http://localhost:8000/api/save-draft/", {
        title,
        content,
      });
      setMessage("Draft saved successfully");
      clearForm();
    } catch (error) {
      setMessage("Saving draft failed");
    }
  };

  const schedulePost = async () => {
    try {
      await axios.post("http://localhost:8000/api/schedule-post/", {
        title,
        content,
        schedule_time: scheduleTime,
      });
      setMessage("Post scheduled successfully");
      clearForm();
    } catch (error) {
      setMessage("Scheduling post failed");
    }
  };

  const clearForm = () => {
    setTitle("");
    setContent("");
    setPlatform("");
    setScheduleTime("");
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1 className="app-title">OmniPost</h1>
      </header>
      <main className="app-main">
        <section className="form-section">
          <h2 className="text-xl font-semibold text-gray-700 mb-4">
            Create Post
          </h2>
          <div className="form-group">
            <input
              type="text"
              placeholder="Title"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="form-control"
            />
          </div>
          <div className="form-group">
            <textarea
              placeholder="Content"
              value={content}
              onChange={(e) => setContent(e.target.value)}
              className="form-control"
              rows="5"
            ></textarea>
          </div>
          <div className="form-group">
            <select
              value={platform}
              onChange={(e) => setPlatform(e.target.value)}
              className="form-control"
            >
              <option value="">Select Platform</option>
              <option value="medium">Medium</option>
              <option value="hashnode">Hashnode</option>
              <option value="devto">Dev.to</option>
            </select>
          </div>
          <div className="form-group">
            <button onClick={postContent} className="btn btn-primary">
              Post
            </button>
            <button onClick={saveDraft} className="btn btn-secondary ml-2">
              Save Draft
            </button>
          </div>
        </section>
        <section className="schedule-section">
          <h2 className="text-xl font-semibold text-gray-700 mb-4">
            Schedule Post
          </h2>
          <div className="form-group">
            <input
              type="datetime-local"
              value={scheduleTime}
              onChange={(e) => setScheduleTime(e.target.value)}
              className="form-control"
            />
          </div>
          <div className="form-group">
            <button onClick={schedulePost} className="btn btn-primary">
              Schedule Post
            </button>
          </div>
        </section>
      </main>
      <footer className="app-footer">
        {message && <div className="message">{message}</div>}
      </footer>
    </div>
  );
}

export default App;
