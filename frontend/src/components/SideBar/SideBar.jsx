import saeLogo from '../../assets/sae-logo.svg';
import "./SideBar.css";


import DropZone from '../DropZone/DropZone';
import FileList from '../FileList/FileList';




export default function SideBar({ files, onFileClick, onDrop }) {
    return (
        <div className="sidebar">
            <img className='img-sidebar' src={saeLogo} alt="SAE logo" />
            <FileList files={files} onFileClick={onFileClick} />
            <div className="divider"></div>
            <DropZone onDrop={onDrop} />
        </div>
    );
}