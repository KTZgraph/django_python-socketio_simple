import './App.css';
import TextEditor from './components/TextEditor'
import {
  BrowserRouter as Router,
  Routes, //zamiast Switch
  Route,
  Navigate, // zamiast Redirect,
} from "react-router-dom";
import { v4 as uuidV4 } from "uuid";


function App() {
  return (
    <Router>
      <Routes>
        {/* przekierowuje do nowego dokumentu który tworzymy , unikalne id */}

        <Route
          path="/"
          exact
          element={<Navigate replace to={`/documents/${uuidV4()}`} />}
        />
        <Route path="/documents/:id" element={<TextEditor />} />
      </Routes>
    </Router>
  );
}

export default App;
