import File from "../File/File";
import "./FileList.css";

export default function FileList({ files, onFileClick }) {
    return (
        <div className="file-list">
            {files.map((file) => (
                <File
                    key={file.id || file.name}
                    name={file.name}
                    handleClick={() => onFileClick(file)}
                />
            ))}
        </div>
    );
}