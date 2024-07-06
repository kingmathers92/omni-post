import { useState } from "react";
import axios from "axios";

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
    <div className="min-h-screen bg-gray-100 flex flex-col items-center py-10">
      <header className="mb-10">
        <h1 className="text-4xl font-bold text-gray-800">OmniPost</h1>
      </header>
      <main className="bg-white shadow-md rounded-lg p-8 w-full max-w-2xl">
        <section className="mb-8">
          <h2 className="text-2xl font-semibold text-gray-700 mb-4">
            Create Post
          </h2>
          <div className="space-y-4">
            <div>
              <input
                type="text"
                placeholder="Title"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg"
              />
            </div>
            <div>
              <textarea
                placeholder="Content"
                value={content}
                onChange={(e) => setContent(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg"
              ></textarea>
            </div>
            <div>
              <select
                value={platform}
                onChange={(e) => setPlatform(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg"
              >
                <option value="">Select Platform</option>
                <option value="medium">Medium</option>
                <option value="hashnode">Hashnode</option>
                <option value="devto">Dev.to</option>
              </select>
            </div>
            <div className="flex space-x-4">
              <button
                onClick={postContent}
                className="px-4 py-2 bg-blue-600 text-white rounded-lg"
              >
                Post
              </button>
              <button
                onClick={saveDraft}
                className="px-4 py-2 bg-gray-600 text-white rounded-lg"
              >
                Save Draft
              </button>
            </div>
          </div>
        </section>
        <section>
          <h2 className="text-2xl font-semibold text-gray-700 mb-4">
            Schedule Post
          </h2>
          <div className="space-y-4">
            <div>
              <input
                type="datetime-local"
                value={scheduleTime}
                onChange={(e) => setScheduleTime(e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-lg"
              />
            </div>
            <div>
              <button
                onClick={schedulePost}
                className="w-full px-4 py-2 bg-blue-600 text-white rounded-lg"
              >
                Schedule Post
              </button>
            </div>
          </div>
        </section>
      </main>
      {message && (
        <footer className="mt-8 p-4 bg-red-100 text-red-700 border border-red-300 rounded-lg">
          {message}
        </footer>
      )}
    </div>
  );
}

export default App;
