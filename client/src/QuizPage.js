
import PlaylistForm from "./form";
import Navbar from './Navbar';
import './QuizPage.css';

function QuizPage() {
  return (
    <div className="Quiz-header">
      <Navbar />
      <h1 className="Main-text">
        <PlaylistForm />
      </h1>
    </div>
  );
}

export default QuizPage;