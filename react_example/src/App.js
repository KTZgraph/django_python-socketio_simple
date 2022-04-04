import './App.css';
import TextEditor from './components/TextEditor'
import {
  BrowserRouter as Router,
  Routes, //zamiast Switch
  Route,
  Navigate, // zamiast Redirect,
} from "react-router-dom";
import { v4 as uuidV4 } from "uuid";

// zamiast uuid
const genRanHex = size => [...Array(size)].map(() => Math.floor(Math.random() * 16).toString(16)).join('');



function App() {
  return (
    <Router>
      <Routes>
        {/* przekierowuje do nowego dokumentu który tworzymy , unikalne id */}

        <Route
          path="/"
          exact
          // za długie domyslnie urle
          // bson.errors.InvalidId: '6ce08626-3e0b-45bd-a004-2127604689db' is not a valid ObjectId, it must be a 12-byte input or a 24-character hex string
          // element={<Navigate replace to={`/documents/${uuidV4().substring(0,24).toString('hex')}`} />}
          element={<Navigate replace to={`/documents/${genRanHex(24)}`} />}
        />
        <Route path="/documents/:id" element={<TextEditor />} />
      </Routes>
    </Router>
  );
}

export default App;
