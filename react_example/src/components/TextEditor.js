import React, { useCallback, useEffect, useState } from "react";
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

  // połaczenie z serwerem
  useEffect(() => {
    // połączenie z serwerem
    const s = io("http://localhost:8000");
    setSocket(s);

    // disconnect jak już nie potrzebujemy socketa
    return () => {
      s.disconnect();
    };
  }, []);












  
  // detekecja zmian z Quill
  useEffect(() => {
    // na początku uruchomienia są nullami
    if(socket == null || quill == null) return;

    const handler = (delta, oldDelta, source) => {
      // source - czy user zrobil zmiany, czy quill library
      if (source !== "user") return; //gdy zmiany NIE przez usera

      // wysyłanie zmian do serwera - wysyłanie wiadomosci z klienta do serwerra
      // 'send_changes' zdarzenie z pythona
      socket.emit("send_changes", delta);
    };

    // 'text-change' zdarzenie z dokumentacji
    quill.on("text-change", handler);

    // usuwanie event listenera jeśli go już dłużej nie potrzebujemy
    return () => {
      // 'text-change'zdarzenie z bilioteki
      quill.off("text-change", handler);
    };
  }, [socket, quill]);














  // edytor
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
