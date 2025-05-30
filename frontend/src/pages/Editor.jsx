import { useState, useEffect } from "react";

import TextArea from "../components/TextArea/TextArea";
import SideBar from "../components/SideBar/SideBar";

import { API } from "../constants";


export default function Editor() {

    const [text, setText] = useState(""); // Initialize text state by fetch
    const [files, setFiles] = useState([]);

    // Fetch all files on mount
    useEffect(() => {
        fetchFiles();
    }, []);

    async function fetchFiles() {
        const res = await fetch(API + "documents/", {
            method: "GET",
            headers: { 'accept': 'application/json' },
        });
        if (res.ok) {
            const data = await res.json();
            setFiles(data);
        }
    }

    async function handleFile(file) {
        // 1. POST file name to server
        await fetch(API + "documents/", {
            method: "POST",
            headers: { 'accept': 'application/json' },
            body: JSON.stringify({ name: file.name }),
            credentials: "include",
        });
        // 2. GET all files and update state
        fetchFiles();
    }

    return (
        <div className="editor">
            <TextArea 
                value={text} 
                onChange={e => setText(e.target.value)}
            />
            <SideBar 
                files={files}
                onFileClick={file => console.log(file)}
                onDrop={handleFile}
            />
        </div>


    );
}