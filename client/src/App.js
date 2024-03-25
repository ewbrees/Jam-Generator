import React from 'react';
import { BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import HomePage from './HomePage'
import OutputPage from './OutputPage';
import QuizPage from './QuizPage';
import Login from './Login';
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />  
        <Route path="/home" element={<HomePage />} />  
        <Route path="/output-page" element={<OutputPage />} />
        <Route path="/quiz-page" element={<QuizPage />} />
      </Routes>
    </Router>
  );
}
export default App;