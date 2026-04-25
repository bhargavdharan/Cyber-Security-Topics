import React, { useState } from 'react';
import api from '../services/api';

const QuizTaker = ({ questions, topicId, quizName }) => {
  const [currentQ, setCurrentQ] = useState(0);
  const [selected, setSelected] = useState('');
  const [score, setScore] = useState(0);
  const [showResult, setShowResult] = useState(false);
  const [answers, setAnswers] = useState([]);
  const [submitted, setSubmitted] = useState(false);

  const handleAnswer = (option) => {
    if (submitted) return;
    setSelected(option);
  };

  const handleSubmit = async () => {
    if (!selected || submitted) return;
    
    const isCorrect = selected === questions[currentQ].correct;
    const newScore = isCorrect ? score + 1 : score;
    
    setAnswers([...answers, { question: currentQ, selected, correct: isCorrect }]);
    setScore(newScore);
    setSubmitted(true);
  };

  const handleNext = () => {
    if (currentQ < questions.length - 1) {
      setCurrentQ(currentQ + 1);
      setSelected('');
      setSubmitted(false);
    } else {
      setShowResult(true);
      saveResult(score + (selected === questions[currentQ].correct ? 1 : 0));
    }
  };

  const saveResult = async (finalScore) => {
    try {
      await api.post('/topics/quiz', {
        topic_id: topicId,
        quiz_name: quizName,
        score: finalScore,
        total_questions: questions.length,
        answers_json: JSON.stringify(answers)
      });
    } catch (err) {
      console.error('Failed to save quiz result:', err);
    }
  };

  const restart = () => {
    setCurrentQ(0);
    setSelected('');
    setScore(0);
    setShowResult(false);
    setAnswers([]);
    setSubmitted(false);
  };

  if (showResult) {
    const percentage = Math.round((score / questions.length) * 100);
    return (
      <div className="card text-center p-4">
        <h4>Quiz Complete!</h4>
        <div className="display-4 my-3">{score}/{questions.length}</div>
        <div className="progress mb-3" style={{ height: '20px' }}>
          <div 
            className={`progress-bar ${percentage >= 70 ? 'bg-success' : percentage >= 50 ? 'bg-warning' : 'bg-danger'}`}
            style={{ width: `${percentage}%` }}
          >
            {percentage}%
          </div>
        </div>
        <button className="btn btn-primary" onClick={restart}>Retake Quiz</button>
      </div>
    );
  }

  const q = questions[currentQ];

  return (
    <div className="card">
      <div className="card-header d-flex justify-content-between">
        <span>Question {currentQ + 1} of {questions.length}</span>
        <span>Score: {score}</span>
      </div>
      <div className="card-body">
        <h5 className="mb-4">{q.question}</h5>
        
        {q.options.map((opt, i) => (
          <div 
            key={i}
            className={`quiz-option ${selected === opt ? 'selected' : ''} ${submitted ? (opt === q.correct ? 'correct' : selected === opt ? 'incorrect' : '') : ''}`}
            onClick={() => handleAnswer(opt)}
          >
            <strong>{String.fromCharCode(65 + i)}.</strong> {opt}
          </div>
        ))}
        
        {submitted && (
          <div className={`alert ${selected === q.correct ? 'alert-success' : 'alert-danger'} mt-3`}>
            {selected === q.correct ? 'Correct!' : `Incorrect. The correct answer is ${q.correct}.`}
            <p className="mb-0 mt-2"><strong>Explanation:</strong> {q.explanation}</p>
          </div>
        )}
      </div>
      <div className="card-footer">
        {!submitted ? (
          <button 
            className="btn btn-primary w-100"
            onClick={handleSubmit}
            disabled={!selected}
          >
            Submit Answer
          </button>
        ) : (
          <button className="btn btn-primary w-100" onClick={handleNext}>
            {currentQ < questions.length - 1 ? 'Next Question' : 'See Results'}
          </button>
        )}
      </div>
    </div>
  );
};

export default QuizTaker;
