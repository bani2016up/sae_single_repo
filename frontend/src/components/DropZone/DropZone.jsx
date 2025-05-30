import { useState, useRef } from "react";
import documentUploadIcon from "../../assets/document-upload.svg";
import "./DropZone.css";

export default function DropZone({ onDrop, children }) {
    const [isDragging, setIsDragging] = useState(false);
    const inputRef = useRef();

    function handleDragOver(e) {
        e.preventDefault();
        setIsDragging(true);
    }

    function handleDragLeave(e) {
        e.preventDefault();
        setIsDragging(false);
    }

    function handleDrop(e) {
        e.preventDefault();
        setIsDragging(false);
        if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
            onDrop(e.dataTransfer.files[0]);
            e.dataTransfer.clearData();
        }
    }

    function handleFileChange(e) {
        if (e.target.files && e.target.files.length > 0) {
            onDrop(e.target.files[0]);
        }
    }

    return (
        <div
            className={`dropzone${isDragging ? " dragging" : ""}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => inputRef.current.click()}
        >
            <img className="img-dropezone"src={documentUploadIcon} alt="Upload Icon" />
            <input
                ref={inputRef}
                type="file"
                style={{ display: "none" }}
                onChange={handleFileChange}
            />
        </div>
    );
}