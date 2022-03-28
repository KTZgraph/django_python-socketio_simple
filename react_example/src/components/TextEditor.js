import { useCallback, useEffect, useState } from "react";
import Quill from "quill";
import "quill/dist/quill.snow.css";
import { io } from "socket.io-client";

const TOOLBAR_OPTIONS = [
  [{ header: [1, 2, 3, 4, 5, 6, false] }],
  [{ font: [] }],
  [{ list: "ordered" }, { list: "bullet" }],
  ["bold", "italic", "underline"],
  [{ color: [] }, { background: [] }],
  [{ script: "sub" }, { script: "super" }],
  [{ align: [] }],
  ["image", "blockquote", "code-block"],
  ["clean"],
];

export default function TextEditor() {
  const [socket, setSocket] = useState();
  const [quill, setQuill] = useState();
  useEffect(() => {
    const s = io("http://127.0.0.1:8000/");
    setSocket(s);

    return () => {
      s.disconnect();
    };
  }, []);

  // odbieranie danych zmienionych w dokumencie
  useEffect(() => {
    // bez sprawdzania typów - dwa == bo na poczatku są undefined
    if (socket == null || quill == null) return;

    // delta to tylko mały fragment dokumentu który się zmienił
    const handler = (delta) => {
      quill.updateContents(delta);
    };
    socket.on("my_event", handler);
    socket.emit("my_event", {'data': 'Trolololo'});


    return () => {
      quill.off("my_event", handler);
    };
  }, [socket, quill]);

  const wrapperRef = useCallback((wrapper) => {
    if (wrapper == null) return;

    wrapper.innerHTML = "";
    const editor = document.createElement("div");
    wrapper.append(editor);
    const q = new Quill(editor, {
      theme: "snow",
      modules: { toolbar: TOOLBAR_OPTIONS },
    });
    setQuill(q);
  }, []);
  return <div className="container" ref={wrapperRef}></div>;
}
