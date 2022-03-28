import Quill from "quill";
import "quill/dist/quill.snow.css";
import { useCallback, useEffect, useState } from "react";
import { io } from "socket.io-client";
import { useParams } from "react-router-dom";

const SAVE_INTERVAL_MS = 2000;
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
  const { id: documentId } = useParams();
  const [socket, setSocket] = useState();
  const [quill, setQuill] = useState();

  useEffect(() => {
    const s = io("http://localhost:8000");
    setSocket(s);

    return () => {
      s.disconnect();
    };
  }, []);

  // zapisywanie dokuemntu w bazie - wywolanie po stronie klienta
  useEffect(() => {
    if (socket == null || quill == null) return;

    // co kilka sekund zapisujemy dokuemnt
    const interval = setInterval(() => {
      socket.emit("save_document", quill.getContents());
    }, SAVE_INTERVAL_MS);

    return () => {
      clearInterval(interval);
    };
  }, [socket, quill]);

  // żeby użytkownicy byli w tym sammy pokoju i mogli edytować ten sam dokuemnt
  useEffect(() => {
    if (socket == null || quill == null) return;

    // nasłuchiwanie eventu
    // once wyczysci event po zakończeniu nasłuchiwania
    socket.once("load_document", (document) => {
      quill.setContents(document);
      quill.enable();
    });

    // przekazanie do servera id Dokumenut
    socket.emit("get_document", documentId);
  }, [socket, quill, documentId]);

  // odbieranie danych zmienionych w dokumencie
  useEffect(() => {
    // bez sprawdzania typów - dwa == bo na poczatku są undefined
    if (socket == null || quill == null) return;

    // delta to tylko mały fragment dokumentu który się zmienił
    const handler = (delta) => {
      quill.updateContents(delta);
    };
    socket.on("receive_changes", handler);

    return () => {
      quill.off("receive_changes", handler);
    };
  }, [socket, quill]);

  // wysyłanie danych z dokumentu
  useEffect(() => {
    // bez sprawdzania typów - dwa == bo na poczatku są undefined
    if (socket == null || quill == null) return;

    // delta to tylko mały fragment dokumentu który się zmienił
    const handler = (delta, oldDelta, source) => {
      if (source !== "user") return;
      socket.emit("send_changes", delta);
    };

    // text-change nie ma na serwerze
    quill.on("text-change", handler);

    return () => {
      // text-change nie ma na serwerze
      quill.off("text-change", handler);
    };
  }, [socket, quill]);

  const wrapperRef = useCallback((wrapper) => {
    if (wrapper === null) return;

    wrapper.innerHTML = "";
    const editor = document.createElement("div");
    wrapper.append(editor);

    const q = new Quill(editor, {
      theme: "snow",
      modules: { toolbar: TOOLBAR_OPTIONS },
    });
    q.disable();
    q.setText("Loading...");
    setQuill(q);
  }, []);

  return <div className="container" ref={wrapperRef}></div>;
}